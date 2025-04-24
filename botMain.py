# main_integrated_gtts.py

import pygame
import cv2
import face_recognition
import numpy as np
from collections import deque
import speech_recognition as sr
import sounddevice as sd
# import simpleaudio as sa # Alternativa para reproducir si prefieres
import threading
import queue
import random
import time
import asyncio
import os # Para manejar archivos temporales de audio

# --- Tus Módulos ---
from modules import face_renderer_pygame
from modules import face as face_patterns
from modules import chatgpt
from modules import sentiment
from modules import audio as audio_effects # Renombrado para claridad

# --- Configuración ---
# (Igual que en main_integrated.py: Pygame, Mirada, Audio Input)
EYE_AR_THRESH = 0.3
FRAME_HISTORY = 8
VIDEO_SOURCE = 1
FACE_DET_MODEL = "hog"
PROCESS_FRAME_RESIZE_FACTOR = 0.5
FS = 16000
CHUNK_DURATION_MS = 100
CHUNK_SAMPLES = int(FS * CHUNK_DURATION_MS / 1000)
AUDIO_BUFFER_SECONDS = 15
MAX_BUFFER_SIZE = FS * AUDIO_BUFFER_SECONDS
SILENCE_THRESHOLD_PROCESS = 500

# Configuración específica gTTS y Efectos
TEMP_AUDIO_DIR = "temp_audio" # Directorio para archivos de audio temporales
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True) # Crear directorio si no existe
OUTPUT_FILENAME_BASE = os.path.join(TEMP_AUDIO_DIR, "response") # Base para nombres de archivo
APPLY_ROBOT_EFFECT = False # Poner en True para activar tu efecto robot

# Animación
BLINK_INTERVAL_MS = 4000
TALKING_ANIM_SPEED_MS = 150

# --- Inicialización ---
# (Igual que en main_integrated.py: Pygame, Cámara, Mirada, Audio Input Recognizer)
if not face_renderer_pygame.init_pygame(): exit()
pygame_initialized = True
cap = cv2.VideoCapture(VIDEO_SOURCE)
if not cap.isOpened(): print(f"Error cámara {VIDEO_SOURCE}"); pygame.quit(); exit()
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Cámara {VIDEO_SOURCE} ({frame_width}x{frame_height})")
gaze_history = deque(maxlen=FRAME_HISTORY)
is_looking = False; was_looking = False
recognizer = sr.Recognizer(); recognizer.dynamic_energy_threshold = True
audio_buffer_lock = threading.Lock()
audio_buffer = np.array([], dtype=np.int16)
recording_enabled = False

# Colas y Eventos
audio_process_queue = queue.Queue()
chatgpt_task_queue = queue.Queue()
response_queue = queue.Queue() # Contendrá tuplas: (texto_respuesta, archivo_audio_final)
# tts_queue ya no se usa directamente para hablar
status_queue = queue.Queue()
stop_event = threading.Event()

# Estado de Animación y Reproducción
current_eye_key = "normal"; current_mouth_key = "normal"
is_playing_audio = False # Flag para indicar si se está reproduciendo audio
last_blink_time = time.time() * 1000
last_mouth_anim_time = time.time() * 1000
blink_state = False; mouth_anim_frame = 0
current_playback_thread = None # Para manejar el hilo de reproducción

# --- Funciones Auxiliares ---
def eye_aspect_ratio(points):
    points = np.array(points)
    A = np.linalg.norm(points[1] - points[5]); B = np.linalg.norm(points[2] - points[4])
    C = np.linalg.norm(points[0] - points[3]); ear = (A + B) / (2.0 * max(C, 1e-6))
    return ear

def play_audio_file(filepath):
    """Reproduce un archivo de audio WAV usando sounddevice."""
    global is_playing_audio
    try:
        # Leer archivo WAV
        samplerate, data = sd.read(filepath, dtype='int16')
        print(f"[Audio Playback] Reproduciendo {filepath} ({len(data)/samplerate:.2f}s)...")
        is_playing_audio = True # INICIO reproducción
        status_queue.put("Speaking...")
        sd.play(data, samplerate)
        sd.wait() # Espera a que termine la reproducción (bloquea este hilo)
        print("[Audio Playback] Reproducción finalizada.")
    except Exception as e:
        print(f"[Error] Reproduciendo {filepath}: {e}")
    finally:
        is_playing_audio = False # FIN reproducción (incluso si hay error)
        # Limpiar archivo temporal
        try:
            if os.path.exists(filepath): os.remove(filepath)
            # Limpiar también el .mp3 si existe
            mp3_path = filepath.replace("_effect.wav", ".mp3").replace("_raw.wav", ".mp3")
            if os.path.exists(mp3_path): os.remove(mp3_path)

        except OSError as e_rem:
             print(f"[Warning] No se pudo borrar archivo temporal {filepath}: {e_rem}")
        # El estado volverá a Listening/Looking Away en el bucle principal

# --- Hilos ---

def audio_callback(indata, frames, time, status):
    """Callback Sounddevice Input."""
    global audio_buffer
    if status: print(f"[Audio Error] {status}"); return
    if recording_enabled:
        with audio_buffer_lock:
            current_len = len(audio_buffer)
            space_left = MAX_BUFFER_SIZE - current_len
            if space_left > 0:
                samples_to_add = min(len(indata), space_left)
                mono_indata = indata[:, 0] if indata.shape[1] > 1 else indata.flatten()
                audio_buffer = np.concatenate((audio_buffer, mono_indata[:samples_to_add]))

def audio_processor_worker():
    """Espera audio, transcribe -> chatgpt_task_queue."""
    # (Idéntico a la versión anterior, solo cambia la cola de salida)
    while not stop_event.is_set():
        try:
            audio_to_process = audio_process_queue.get(timeout=1.0)
            if audio_to_process is None: continue
            print("[Processor] Audio recibido.")
            status_queue.put("Processing Speech...")
            if np.max(np.abs(audio_to_process)) < SILENCE_THRESHOLD_PROCESS:
                print("[Processor] Silencio."); status_queue.put("Listening..." if is_looking else "Looking Away")
                audio_process_queue.task_done(); continue
            try:
                audio_data_sr = sr.AudioData(audio_to_process.tobytes(), FS, 2)
                print("[Processor] Reconociendo...")
                text = recognizer.recognize_google(audio_data_sr, language="es-ES")
                print(f"[Processor] Texto: '{text}'")
                if text: chatgpt_task_queue.put(text) # <<< Cambio aquí
                else: status_queue.put("Listening..." if is_looking else "Looking Away")
            except sr.UnknownValueError: print("[Processor] No entendido."); status_queue.put("Listening..." if is_looking else "Looking Away")
            except sr.RequestError as e: print(f"[Processor] SR API Error: {e}"); status_queue.put("SR API Error"); time.sleep(2); status_queue.put("Listening..." if is_looking else "Looking Away")
            except Exception as e: print(f"[Processor] Error: {e}"); status_queue.put("Processing Error"); time.sleep(2); status_queue.put("Listening..." if is_looking else "Looking Away")
            audio_process_queue.task_done()
        except queue.Empty: continue
    print("Audio processor worker finished.")

def response_processing_worker():
    """Espera texto de ChatGPT, genera audio con gTTS/efectos, -> response_queue."""
    while not stop_event.is_set():
        try:
            text_for_gpt = chatgpt_task_queue.get(timeout=1.0)
            print(f"[Resp Proc] Texto para ChatGPT: '{text_for_gpt}'")
            status_queue.put("Thinking...")
            # No hay frase de relleno aquí, se genera el audio completo

            response_text = ""
            final_audio_path = None
            try:
                # 1. Obtener respuesta de ChatGPT
                # *** LLAMADA A TU MODULO CHATGPT ***
                response_text = chatgpt.get_chatgpt_response(text_for_gpt)
                print(f"[Resp Proc] Respuesta ChatGPT: '{response_text[:60]}...'")

                # 2. Generar audio base con gTTS (tu módulo audio)
                timestamp = int(time.time() * 1000)
                base_mp3_path = f"{OUTPUT_FILENAME_BASE}_{timestamp}_raw.mp3"
                print(f"[Resp Proc] Generando TTS en {base_mp3_path}...")
                # *** LLAMADA A TU MODULO AUDIO (gTTS) ***
                audio_effects.generate_tts_audio(response_text, base_mp3_path)

                # 3. Aplicar efectos (tu módulo audio)
                if APPLY_ROBOT_EFFECT:
                    print("[Resp Proc] Aplicando efecto robot...")
                    # *** LLAMADA A TU MODULO AUDIO (Efectos) ***
                    final_audio_path = audio_effects.aplicar_filtro_roboto(base_mp3_path)
                    # Borrar el mp3 base si se generó el WAV con efecto
                    if os.path.exists(base_mp3_path): os.remove(base_mp3_path)
                else:
                    # Si no hay efectos, necesitamos convertir MP3 a WAV para sounddevice
                    print("[Resp Proc] Convirtiendo MP3 a WAV...")
                    final_audio_path = base_mp3_path.replace(".mp3", ".wav")
                    try:
                         from pydub import AudioSegment # Asegurar importación
                         audio_segment = AudioSegment.from_mp3(base_mp3_path)
                         audio_segment.export(final_audio_path, format="wav")
                         if os.path.exists(base_mp3_path): os.remove(base_mp3_path) # Borrar mp3
                    except Exception as e_conv:
                         print(f"[Error] Conversión MP3 a WAV fallida: {e_conv}")
                         final_audio_path = None # No se pudo generar archivo reproducible


                # 4. Poner resultado (texto y path del audio) en la cola final
                if final_audio_path and os.path.exists(final_audio_path):
                    response_queue.put((response_text, final_audio_path))
                else:
                    print("[Resp Proc] No se generó archivo de audio final.")
                    # Poner solo texto o un indicador de error?
                    response_queue.put((response_text, None)) # Poner None como path si falló

            except Exception as e:
                error_msg = f"ChatGPT/Audio Gen Error: {e}"
                print(f"[Error] {error_msg}")
                response_queue.put((error_msg, None)) # Enviar error como texto, sin audio

            chatgpt_task_queue.task_done()

        except queue.Empty: continue
    print("Response processing worker finished.")


# --- Bucle Principal ---
def main():
    global is_looking, was_looking, recording_enabled, audio_buffer
    global current_eye_key, current_mouth_key, is_playing_audio, current_playback_thread
    global last_blink_time, last_mouth_anim_time, blink_state, mouth_anim_frame

    running = True
    current_status = "Initializing..."

    # Iniciar stream de audio input
    try:
        stream = sd.InputStream(samplerate=FS, channels=1, dtype='int16',
                                blocksize=CHUNK_SAMPLES, callback=audio_callback)
        stream.start()
    except Exception as e: print(f"Error input stream: {e}"); return

    # Iniciar hilos
    processor_thread = threading.Thread(target=audio_processor_worker, daemon=True)
    response_thread = threading.Thread(target=response_processing_worker, daemon=True) # Nuevo hilo
    processor_thread.start()
    response_thread.start()

    status_queue.put("Listening...")

    while running:
        # Eventos Pygame
        if not face_renderer_pygame.handle_events(): running = False; break
        currently_looking = False # <--- AÑADE ESTA LÍNEA

        # Video y Mirada (igual que antes)
        ret, frame = cap.read()
        if not ret: time.sleep(0.05); continue
        # ... (resto de tu lógica de detección de mirada igual que antes) ...
        gaze_history.append(currently_looking)
        was_looking = is_looking
        is_looking = sum(gaze_history) > (FRAME_HISTORY * 0.6)
        recording_enabled = is_looking
        if not is_looking and was_looking:
            with audio_buffer_lock:
                if len(audio_buffer) > FS * 0.5: audio_process_queue.put(audio_buffer.copy())
                audio_buffer = np.array([], dtype=np.int16)
        elif is_looking and not was_looking:
            with audio_buffer_lock: audio_buffer = np.array([], dtype=np.int16)

        # Actualizar Estado (igual, pero proteger 'Speaking...')
        new_status = None
        try:
            while not status_queue.empty(): new_status = status_queue.get_nowait(); status_queue.task_done()
            if new_status:
                if not (current_status == "Speaking..." and new_status != "Speaking..."):
                     current_status = new_status
                elif current_status == "Speaking..." and not is_playing_audio: # Si dice Speaking pero ya no reproduce
                     current_status = new_status # Permitir cambio

        except queue.Empty:
             if not is_playing_audio and current_status not in ["Processing Speech...", "Thinking...", "SR API Error", "Processing Error", "ChatGPT/Audio Gen Error"]:
                  expected_status = "Listening..." if is_looking else "Looking Away"
                  if current_status != expected_status: current_status = expected_status

        # Procesar Respuesta Final (Texto + Audio Path)
        try:
            response_text, audio_path = response_queue.get_nowait()
            print(f"[Main] Respuesta final recibida. Audio: {audio_path}")

            # 1. Analizar sentimiento para ojos
            try:
                sentiment_result = asyncio.run(sentiment.analyze_sentiment(response_text))
                current_eye_key = sentiment.select_eye_pattern_for_sentiment(sentiment_result)
                print(f"[Main] Ojos -> {current_eye_key}")
            except Exception as e_sent: print(f"[Error] Sentimiento: {e_sent}"); current_eye_key = "normal"

            # 2. Reproducir audio (si existe) en un hilo separado
            if audio_path and os.path.exists(audio_path):
                # Detener hilo anterior si aún corre (poco probable pero seguro)
                if current_playback_thread and current_playback_thread.is_alive():
                    print("[Warning] Deteniendo reproducción anterior...")
                    # sd.stop() # Detener reproducción actual globalmente
                    current_playback_thread.join(timeout=0.5) # Esperar un poco

                # Iniciar nuevo hilo de reproducción
                current_playback_thread = threading.Thread(target=play_audio_file, args=(audio_path,), daemon=True)
                current_playback_thread.start()
            else:
                print("[Main] No hay archivo de audio para reproducir.")
                 # Si no hay audio, resetear estado
                current_status = "Listening..." if is_looking else "Looking Away"

            response_queue.task_done()
        except queue.Empty:
            pass

        # Lógica de Animación Facial (igual, pero usa is_playing_audio)
        current_time_ms = time.time() * 1000
        if not is_playing_audio and current_time_ms - last_blink_time > BLINK_INTERVAL_MS:
            blink_state = True; last_blink_time = current_time_ms
        if blink_state:
            final_eye_pattern = face_patterns.face_patterns_eyes.get("blink", face_patterns.face_patterns_eyes["normal"])
            if current_time_ms - last_blink_time > 150: blink_state = False; last_blink_time = current_time_ms
        else: final_eye_pattern = face_patterns.face_patterns_eyes.get(current_eye_key, face_patterns.face_patterns_eyes["normal"])

        if is_playing_audio: # Animar boca si está reproduciendo audio
            if current_time_ms - last_mouth_anim_time > TALKING_ANIM_SPEED_MS:
                mouth_anim_frame = 1 - mouth_anim_frame; last_mouth_anim_time = current_time_ms
            mouth_key = "talking_1" if mouth_anim_frame == 0 else "talking_2"
            final_mouth_pattern = face_patterns.face_patterns_mouth.get(mouth_key, face_patterns.face_patterns_mouth["normal"])
        else: final_mouth_pattern = face_patterns.face_patterns_mouth.get("normal", face_patterns.face_patterns_mouth["normal"])

        # Renderizar con tu Módulo
        face_renderer_pygame.update_matrix_from_patterns(final_eye_pattern, final_mouth_pattern)
        face_renderer_pygame.draw_frame()
        face_renderer_pygame.tick_clock(30)

    # --- Limpieza ---
    print("Saliendo...")
    stop_event.set()
    if stream: stream.stop(); stream.close()
    cap.release()
    # Detener reproducción si estaba en curso
    if is_playing_audio: sd.stop()
    print("Esperando hilos...")
    processor_thread.join(timeout=1.5)
    response_thread.join(timeout=1.5)
    if current_playback_thread and current_playback_thread.is_alive(): current_playback_thread.join(timeout=1.0)
    if pygame_initialized: face_renderer_pygame.cleanup_pygame()
    print("✅ Programa terminado.")
    # Limpieza final de archivos temporales (por si acaso)
    try:
        for f in os.listdir(TEMP_AUDIO_DIR): os.remove(os.path.join(TEMP_AUDIO_DIR, f))
        os.rmdir(TEMP_AUDIO_DIR)
    except Exception as e_clean: print(f"Error limpiando {TEMP_AUDIO_DIR}: {e_clean}")


if __name__ == "__main__":
    main()