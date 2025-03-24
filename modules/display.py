# animation_project/modules/display.py

import curses
import time
import random
import numpy as np
import simpleaudio as sa
from pydub import AudioSegment
import asyncio


from modules import face    # Import face module
from modules import audio   # Import audio module
from modules import sentiment # Import sentiment module

async def animation_terminal(stdscr, text):
    """Displays an animated face in the terminal, changing emotions based on sentence sentiment."""

    # Hides the cursor
    curses.curs_set(0)

    # Split text into sentences
    phrases = sentiment.split_into_phrases(text)

    # Process each phrase separately
    for phrase in phrases:
        phrase = phrase.strip()  # Remove extra spaces

        # Analyze the sentiment of the phrase
        text_sentiment = await sentiment.analyze_sentiment(phrase)
        eye_pattern_key = sentiment.select_eye_pattern_for_sentiment(text_sentiment)
        current_eye_pattern = face.face_patterns_eyes[eye_pattern_key]

        # Generate and filter speech audio
        audio_file_mp3 = "output_audio.mp3"
        audio.generate_tts_audio(phrase, audio_file_mp3)
        audio_file_wav_roboto = audio.aplicar_filtro_roboto(audio_file_mp3)

        wave_obj = sa.WaveObject.from_wave_file(audio_file_wav_roboto)
        play_obj = wave_obj.play()
        filtered_audio = AudioSegment.from_wav(audio_file_wav_roboto)
        audio_fragments = filtered_audio[::100]  # Split into 100ms chunks

        next_blink_time = time.time() + random.uniform(1, 3)
        blinking = False

        # Synchronize face animation with speech
        for fragment in audio_fragments:
            now = time.time()
            magnitudes = audio.extract_frequencies(fragment)
            current_mouth_pattern = face.face_patterns_mouth["normal"]

            # Blink control
            if not blinking and now >= next_blink_time:
                blinking = True
                face.draw_face(stdscr, face.face_patterns_eyes["blink"], face.face_patterns_mouth["normal"])
                time.sleep(0.25)
                next_blink_time = now + random.uniform(1, 3)
                blinking = False

            # Adjust mouth movement based on volume
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

            # 🔄 Draw face with updated emotion & mouth
            face.draw_face(stdscr, current_eye_pattern, current_mouth_pattern)
            time.sleep(0.1)

        play_obj.wait_done()  # Wait for audio to finish before moving to next phrase
       
