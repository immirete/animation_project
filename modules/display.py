# animation_project/modules/display.py

import curses
import time
import random
import numpy as np
import simpleaudio as sa
from pydub import AudioSegment
import asyncio

from modules import face
from modules import audio
from modules import sentiment
from modules.face_renderer_pygame import init_pygame, cleanup_pygame, update_matrix_from_patterns, draw_frame, handle_events, tick_clock

class DisplayManager:
    def __init__(self, mode='terminal'):
        self.mode = mode
        if mode == 'matrix':
            if not init_pygame():
                print("No se pudo inicializar Pygame, usando modo terminal")
                self.mode = 'terminal'

    async def draw_face(self, stdscr, eye_pattern, mouth_pattern):
        if self.mode == 'terminal' and stdscr:
            face.draw_face(stdscr, eye_pattern, mouth_pattern)
            return True
        elif self.mode == 'matrix':
            update_matrix_from_patterns(eye_pattern, mouth_pattern)
            draw_frame()
            return handle_events()
        return True

    async def animation_terminal(self, stdscr, text):
        """Muestra animación en el modo seleccionado"""
        if self.mode == 'terminal' and not stdscr:
            return  # Necesitamos stdscr para modo terminal

        phrases = sentiment.split_into_phrases(text)

        for phrase in phrases:
            phrase = phrase.strip()

            text_sentiment = await sentiment.analyze_sentiment(phrase)
            eye_pattern_key = sentiment.select_eye_pattern_for_sentiment(text_sentiment)
            current_eye_pattern = face.face_patterns_eyes[eye_pattern_key]

            audio_file_mp3 = "output_audio.mp3"
            audio.generate_tts_audio(phrase, audio_file_mp3)
            audio_file_wav_roboto = audio.aplicar_filtro_roboto(audio_file_mp3)

            wave_obj = sa.WaveObject.from_wave_file(audio_file_wav_roboto)
            play_obj = wave_obj.play()
            filtered_audio = AudioSegment.from_wav(audio_file_wav_roboto)
            audio_fragments = filtered_audio[::100]

            next_blink_time = time.time() + random.uniform(1, 3)
            blinking = False

            for fragment in audio_fragments:
                now = time.time()
                magnitudes = audio.extract_frequencies(fragment)
                current_mouth_pattern = face.face_patterns_mouth["normal"]

                if not blinking and now >= next_blink_time:
                    blinking = True
                    if not await self.draw_face(stdscr, face.face_patterns_eyes["blink"], face.face_patterns_mouth["normal"]):
                        play_obj.stop()
                        return
                    await asyncio.sleep(0.25)
                    next_blink_time = now + random.uniform(1, 3)
                    blinking = False

                if audio.detect_s_sound(magnitudes):
                    current_mouth_pattern = face.face_patterns_mouth["s_sound"]
                else:
                    volume = np.linalg.norm(np.array(fragment.get_array_of_samples()))
                    if volume < 5000:
                        current_mouth_pattern = face.face_patterns_mouth["normal"]
                    elif volume < 15000:
                        current_mouth_pattern = face.face_patterns_mouth["talking_1"]
                    else:
                        current_mouth_pattern = face.face_patterns_mouth["talking_2"]

                if not await self.draw_face(stdscr, current_eye_pattern, current_mouth_pattern):
                    play_obj.stop()
                    return
                await asyncio.sleep(0.1)

            play_obj.wait_done()

        if self.mode == 'matrix':
            cleanup_pygame()