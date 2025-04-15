# transcription_module.py

import cv2
import face_recognition
import numpy as np
from collections import deque
import speech_recognition as sr
import sounddevice as sd
import time # Import time for small delays if needed

# --- Configurations (you can move them here or pass them as arguments) ---
EYE_AR_THRESH = 0.30 # Renamed from UMBRAL_OJOS
MIN_EYE_DISTANCE = 40 # Not used in the original code, but kept just in case
FRAME_HISTORY = 8   # Renamed from HISTORIAL_FRAMES
FS = 16000
CHUNK_SIZE = 1024
# ------------------------------------------------------------------------

# --- Global variables needed for callback and processing ---
# Using globals is simpler here due to the sounddevice callback
audio_buffer = np.array([], dtype=np.int16)
recording = False       # Renamed from grabando
transcription_result = None # To store the transcription result
quit_flag = False       # To signal exit via 'q' or voice command
# --------------------------------------------------------------------

recognizer = sr.Recognizer()

def eye_aspect_ratio(points):
    """Calculates the Eye Aspect Ratio (EAR) for a given set of eye landmark points."""
    # Ensure points are a NumPy array for easier calculations
    points = np.array(points)
    # Vertical distances (based on common dlib/face_recognition indices)
    # Distance between points 1 and 5, and 2 and 4
    A = np.linalg.norm(points[1] - points[5])
    B = np.linalg.norm(points[2] - points[4])
    # Horizontal distance (between points 0 and 3)
    C = np.linalg.norm(points[0] - points[3])
    # Calculate EAR
    ear = (A + B) / (2.0 * max(C, 1)) # Avoid division by zero
    return ear

def process_audio():
    """Processes the audio buffer, performs speech recognition, and returns the text."""
    global audio_buffer, transcription_result, quit_flag # Access global variables
    detected_text = None
    if len(audio_buffer) > FS * 0.8: # Process if there's enough audio (e.g., > 0.8 seconds)
        print("\033[94m[INFO] Processing audio...\033[0m")
        try:
            # Ensure data is suitable for AudioData
            # Format is (bytes, sample_rate, sample_width)
            # sounddevice gives int16, which is 2 bytes wide
            audio_data = sr.AudioData(audio_buffer.tobytes(), FS, 2)
            # Recognize speech using Google Speech Recognition (requires internet)
            # Using Spanish as per original code
            text = recognizer.recognize_google(audio_data, language="es-ES")
            print(f"\033[92m[TRANSCRIPTION] {text}\033[0m")
            # Check for the Spanish exit command
            if "salir" in text.lower():
                 print("\033[93m[INFO] 'salir' command detected.\033[0m")
                 quit_flag = True # Signal exit via voice command
                 detected_text = None # Don't return "salir" as a query
            else:
                 detected_text = text # Store the valid text
        except sr.UnknownValueError:
            print("\033[90m[Audio not recognized]\033[0m")
        except sr.RequestError as e:
            print(f"\033[91m[API Error] Could not connect to Google Speech Recognition; {e}\033[0m")
        except Exception as e:
            print(f"\033[91m[Unexpected audio processing error] {str(e)}\033[0m")

        # Clear the buffer regardless of the recognition result
        audio_buffer = np.array([], dtype=np.int16)

    return detected_text # Returns the text or None

def audio_callback(indata, frames, time, status):
    """This function is called by sounddevice for each audio block."""
    global audio_buffer, recording # Access global variables
    if status:
        print(f"\033[91m[Audio Stream Error] {status}\033[0m")
    # Only record if the 'recording' flag is active
    if recording:
        # Assuming 'indata' is mono or we want the first channel
        # If it's stereo and you want to mix or just one channel, adjust this
        audio_buffer = np.concatenate((audio_buffer, indata[:, 0]))

def start_transcription_and_get_text():
    """
    Initializes gaze detection and transcription.
    Returns the transcribed text when the user looks away,
    or None if the user exits ('q' or "salir" command).
    """
    global audio_buffer, recording, transcription_result, quit_flag # Reset states
    audio_buffer = np.array([], dtype=np.int16)
    recording = False
    transcription_result = None
    quit_flag = False

    print("\033[96m[INFO] Initializing camera and gaze detection...\033[0m")
    cap = cv2.VideoCapture(1) # Or the correct index for your camera
    if not cap.isOpened():
        print("\033[91m[ERROR] Could not open camera.\033[0m")
        return None
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    gaze_history = deque(maxlen=FRAME_HISTORY) # Renamed from historial_mirada

    stream = sd.InputStream(
        samplerate=FS,
        channels=1, # Mono
        dtype='int16', # int16 data type
        blocksize=CHUNK_SIZE,
        callback=audio_callback # Use the renamed callback
    )

    text_to_return = None # Variable to store the text to be returned

    try:
        stream.start()
        print("\033[96m[INFO] Listening... Look at the camera to enable recording.\033[0m")
        print("\033[96m[INFO] When you look away, the last thing you said will be processed.\033[0m")
        print("\033[96m[INFO] Press 'q' in the video window to exit.\033[0m")

        # --- Main Loop ---
        while True:
            ret, frame = cap.read()
            if not ret:
                print("\033[91m[ERROR] Could not read frame from camera.\033[0m")
                break

            frame = cv2.flip(frame, 1) # Flip horizontally
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # face_recognition uses RGB

            # Face detection and landmarks
            # Using "hog" model (faster, less accurate) vs "cnn" (slower, more accurate, needs dlib with CUDA)
            face_locations = face_recognition.face_locations(rgb_frame, model="hog")
            face_landmarks_list = face_recognition.face_landmarks(rgb_frame, face_locations=face_locations)

            currently_looking = False # Assume not looking by default
            if face_landmarks_list:
                # Use only the first detected face
                landmarks = face_landmarks_list[0]
                left_eye_pts = landmarks.get('left_eye') # Renamed from ojo_izq
                right_eye_pts = landmarks.get('right_eye') # Renamed from ojo_der

                if left_eye_pts and right_eye_pts:
                    # Calculate EAR for each eye
                    ear_left = eye_aspect_ratio(left_eye_pts) # Renamed from ear_izq
                    ear_right = eye_aspect_ratio(right_eye_pts) # Renamed from ear_der

                    # Average EAR or similar logic to determine if eyes are open
                    ear_avg = (ear_left + ear_right) / 2.0

                    # Determine looking based on eyes being open (EAR > threshold)
                    # You might need more sophisticated gaze detection (e.g., pupil tracking)
                    # For now, assume open eyes (EAR > threshold) means "looking"
                    if ear_avg > EYE_AR_THRESH:
                         currently_looking = True

                    # Draw landmarks for debugging (optional)
                    for point in left_eye_pts: cv2.circle(frame, point, 1, (0, 255, 0), -1)
                    for point in right_eye_pts: cv2.circle(frame, point, 1, (0, 255, 0), -1)
                    cv2.putText(frame, f"EAR: {ear_avg:.2f}", (frame.shape[1] - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            gaze_history.append(currently_looking)
            # Consider looking if most recent frames indicate it (e.g., > 70%)
            persistently_looking = sum(gaze_history) > FRAME_HISTORY * 0.7

            # --- Update recording state ---
            # If looking persistently, enable recording
            if persistently_looking:
                if not recording: # Start recording only when transitioning to looking
                    print("\033[92m[INFO] Looking detected. Audio recording enabled.\033[0m")
                    recording = True
            else:
                # If stops looking and we were recording, stop and process audio
                if recording: # Process only when transitioning away from looking
                    print("\033[93m[INFO] Looked away. Stopping recording and processing.\033[0m")
                    recording = False # Stop recording first
                    # Give a very short break to ensure the last chunk enters the callback if needed
                    # time.sleep(0.1) # Might not be necessary, test this
                    processed_text = process_audio() # Process the buffered audio
                    if processed_text:
                        text_to_return = processed_text
                        break # Exit the while loop with the valid transcribed text
                    if quit_flag: # If "salir" was detected in process_audio
                        break # Exit the while loop

            # --- Visualization ---
            color = (0, 255, 0) if persistently_looking else (0, 0, 255)
            status_text = "LOOKING (Recording)" if persistently_looking else ("NOT LOOKING" + (" (Processing...)" if not recording and len(audio_buffer) > 0 else ""))
            cv2.putText(frame, status_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.imshow('Gaze Detection + Transcription', frame) # Window title in English

            # --- Exit condition ---
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\033[93m[INFO] 'q' key pressed. Exiting...\033[0m")
                quit_flag = True # Signal exit
                break
            # If quit_flag was activated by voice ("salir") or by 'q'
            if quit_flag:
                 break
        # --- End of Main Loop ---

    except Exception as e:
        print(f"\033[91m[CRITICAL Error in main loop] {str(e)}\033[0m")
        import traceback
        traceback.print_exc() # Prints the full traceback for debugging
    finally:
        # --- Cleanup ---
        print("\033[94m[INFO] Stopping audio stream and releasing camera...\033[0m")
        if 'stream' in locals() and stream is not None:
            stream.stop()
            stream.close()
        if 'cap' in locals() and cap is not None:
            cap.release()
        cv2.destroyAllWindows()
        # Wait a bit for windows to close cleanly, especially on some OS
        for i in range(4): cv2.waitKey(1)

    # --- Return result ---
    if quit_flag:
        print("\033[93m[INFO] Transcription cancelled by user.\033[0m")
        return None
    elif text_to_return:
        print(f"\033[92m[INFO] Transcribed text obtained: '{text_to_return}'\033[0m")
        return text_to_return
    else:
        # This case might happen if the loop exits unexpectedly or audio processing failed without setting quit_flag
        print("\033[90m[INFO] No valid transcribed text obtained.\033[0m")
        return None

# You can add this to test the module directly
# if __name__ == "__main__":
#     print("Starting transcription module test...")
#     text = start_transcription_and_get_text()
#     if text:
#         print(f"\nFinal text received: {text}")
#     else:
#         print("\nNo text received.")
#     print("Test finished.")