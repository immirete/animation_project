# animation_project/modules/audio.py

from pydub import AudioSegment
from gtts import gTTS
import numpy as np
from scipy.fft import fft

def extract_frequencies(audio):
    """Extracts main frequencies from audio fragment using FFT."""
    samples = np.array(audio.get_array_of_samples())
    # Apply FFT to audio
    fft_result = fft(samples)
    # Frequency magnitudes
    magnitudes = np.abs(fft_result)
    return magnitudes

def detect_s_sound(magnitudes, threshold=4000000):
    """Detects if 'S' sound is present in high frequencies."""
    # Threshold to detect peak in high frequencies ('S' range)
    high_frequencies = magnitudes[1000:]  # Extract high frequencies
    if high_frequencies.size == 0:
        return False
    peak = np.max(high_frequencies)
    return peak > threshold  # If peak exceeds threshold, 'S' sound detected

def generate_tts_audio(texto, archivo_salida):
    """Generates audio file with gTTS."""
    tts = gTTS(texto, lang='es')  # Use Spanish (es)
    tts.save(archivo_salida)  # Saves audio file


def change_pitch(audio, semitones):
    """Cambia el tono (pitch) del audio en la cantidad de semitonos especificada."""
    new_sample_rate = int(audio.frame_rate * (2 ** (semitones / 12.0)))
    return audio._spawn(audio.raw_data, overrides={"frame_rate": new_sample_rate}).set_frame_rate(44100)

def add_reverb(audio, intensity):
    """Simula un efecto de reverberación simple (no tan avanzado como un IR)."""
    echo = audio - 10  # Baja el volumen del eco
    delay = 40  # Milisegundos
    reverb = echo.overlay(audio, position=delay)
    return reverb if intensity > 0 else audio


def aplicar_filtro_roboto(archivo_audio_mp3):
    """Applies a robotic filter to the audio using sample rate reduction, reverb, and ring modulation."""
    # Load the MP3 audio file
    audio = AudioSegment.from_mp3(archivo_audio_mp3)

    # 1. Reduce frame rate (sample rate) for a digitalized sound
    audio = audio.set_frame_rate(8000)  # Lower sample rate (example: 8000 Hz - try different values)
    audio = change_pitch(audio, semitones=1)  # Baja el tono

    audio = add_reverb(audio, 0.5)  # Más reverb para eco melancólico

    # 2. Add Reverb for a sense of space and artificiality
    # Experiment with 'reverberance' and 'room_scale' parameters


    # 3. Ring Modulation for an alien/metallic sound
    def ring_modulation(audio_segment, frequency): # Frequency of the modulator in Hz
        samples = np.array(audio_segment.get_array_of_samples()).astype(np.float32) / 2**15 # Normalize to -1 to 1
        sample_rate = audio_segment.frame_rate
        duration = len(audio_segment) / sample_rate
        time_array = np.linspace(0, duration, len(samples), endpoint=False)
        modulator = np.sin(2 * np.pi * frequency * time_array) # Sinusoidal modulator
        modulated_signal = samples * modulator # Ring modulation (multiplication)

        modulated_signal = (modulated_signal * 2**15).astype(np.int16) # Scale back to int16
        modulated_audio = AudioSegment(modulated_signal.tobytes(), frame_rate=sample_rate, sample_width=2, channels=audio_segment.channels)
        return modulated_audio

    audio = ring_modulation(audio, frequency=400) # Apply ring modulation, experiment with frequency

    # Export the modified audio as WAV (simpleaudio works best with WAV)
    archivo_salida_roboto = "output_roboto.wav"
    audio.export(archivo_salida_roboto, format="wav")
    return archivo_salida_roboto