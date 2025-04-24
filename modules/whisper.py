import argparse
import queue
import sys
import sounddevice as sd
import numpy as np
import whisper
import torch # Whisper usa torch

# --- Argumentos de línea de comandos (opcional) ---
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-m", "--model", type=str, default="base",
    help="Whisper model name (e.g., tiny, base, small, medium, large)")
parser.add_argument(
    "-d", "--device", type=str, default=None,
    help="audio device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, default=16000,
    help="sampling rate of audio device")
parser.add_argument(
    "-t", "--threshold", type=float, default=0.02,
    help="RMS energy threshold for detecting silence")
parser.add_argument(
    "-s", "--silence_duration", type=float, default=1.0,
    help="seconds of silence required to trigger transcription")
parser.add_argument(
    "-c", "--chunk_duration", type=float, default=0.3,
    help="duration of audio chunks in seconds")
parser.add_argument(
    "--language", type=str, default="es",
    help="language for transcription (e.g., 'en', 'es', 'fr')")

args = parser.parse_args(remaining)

# --- Configuración ---
SAMPLE_RATE = args.samplerate
CHUNK_DURATION = args.chunk_duration # Duración de cada bloque leído del micro (segundos)
BLOCK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION) # Tamaño del bloque en muestras
SILENCE_THRESHOLD = args.threshold # Umbral de energía RMS para considerar silencio
SILENCE_BLOCKS_NEEDED = int(args.silence_duration / CHUNK_DURATION) # Cuántos bloques seguidos de silencio
MODEL_NAME = args.model
LANGUAGE = args.language

# --- Inicialización ---
print(f"Loading Whisper model '{MODEL_NAME}'...")
# Considerar usar device="cuda" o device="mps" si tienes GPU compatible con torch
model = whisper.load_model(MODEL_NAME)
print("Model loaded.")

audio_queue = queue.Queue() # Cola para pasar audio del callback al hilo principal
temp_audio_buffer = [] # Buffer temporal para acumular audio de la frase actual
silent_block_count = 0 # Contador de bloques silenciosos consecutivos
is_speaking = False # Flag para saber si se detectó voz

# --- Función Callback de SoundDevice ---
# Se ejecuta en un hilo separado cada vez que hay un nuevo bloque de audio
def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    # Poner los datos en la cola para procesarlos en el hilo principal
    audio_queue.put(indata.copy())

# --- Bucle Principal ---
try:
    print("Starting audio stream...")
    # Abre el stream de audio
    with sd.InputStream(samplerate=SAMPLE_RATE,
                        blocksize=BLOCK_SIZE,
                        device=args.device,
                        channels=1,
                        dtype='float32',
                        callback=audio_callback):

        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("Listening...")
        print("#" * 80)

        while True:
            # Obtener datos de audio de la cola
            audio_chunk = audio_queue.get()

            # Calcular la energía (RMS) del bloque actual
            rms = np.sqrt(np.mean(audio_chunk**2))
            # print(f"RMS: {rms:.4f}") # Descomentar para depurar umbral

            is_currently_silent = rms < SILENCE_THRESHOLD

            if is_currently_silent:
                silent_block_count += 1
                # print(f"Silent blocks: {silent_block_count}/{SILENCE_BLOCKS_NEEDED}") # Debug
            else:
                silent_block_count = 0 # Resetear contador si hay sonido
                if not is_speaking:
                    print("Speech detected...", end="", flush=True)
                is_speaking = True

            # Acumular siempre el audio si estamos hablando o si acabamos de detectar silencio
            # (para no perder el final de la frase)
            if is_speaking or len(temp_audio_buffer) > 0:
                 temp_audio_buffer.append(audio_chunk)

            # Comprobar si hemos tenido suficiente silencio DESPUÉS de haber hablado
            if is_speaking and silent_block_count >= SILENCE_BLOCKS_NEEDED:
                print(" Silence detected, transcribing...")

                # Concatenar los bloques de audio acumulados
                full_audio_np = np.concatenate(temp_audio_buffer)

                # Limpiar buffer y flags para la siguiente frase *antes* de transcribir
                temp_audio_buffer = []
                silent_block_count = 0
                is_speaking = False

                # Asegurarse de que el audio es float32
                full_audio_float32 = full_audio_np.flatten().astype(np.float32)

                # --- Transcripción ---
                # Convertir a tensor si usas GPU, si no, NumPy está bien
                # audio_tensor = torch.from_numpy(full_audio_float32)

                result = model.transcribe(full_audio_float32,
                                          language=LANGUAGE,
                                          fp16=False) # fp16=True si usas GPU compatible

                transcription = result['text'].strip()
                if transcription: # Solo imprimir si hay texto
                    print(f"\n>>> {transcription}\n")
                else:
                    print("\n(No text detected or empty transcription)\n")

                # Volver a indicar que estamos escuchando
                print("Listening...")


except KeyboardInterrupt:
    print("\nStopping recording.")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    print("Stream stopped.")