# animation_project/modules/sentiment.py

from textblob import TextBlob
from googletrans import Translator
from nrclex import NRCLex

async def analyze_sentiment(text):
    """Analyzes sentiment and emotion of text using NRCLex and TextBlob."""

    # Translate text to English
    try:
        translation = await translate_text(text)
    except Exception as e:
        print(f"Translation Error: {e}")
        translation = text  # Use original text if translation fails

    # Detect emotions with NRCLex
    emotion = NRCLex(translation).raw_emotion_scores
    primary_emotion = max(emotion, key=emotion.get, default="neutral")

    # Analyze sentiment with TextBlob
    polarity = TextBlob(translation).sentiment.polarity

    # Adjust emotion based on sentiment if NRCLex is "neutral"
    if primary_emotion not in ["joy", "sadness", "anger", "surprise"]:
        primary_emotion = "joy" if polarity > 0 else "sadness" if polarity < 0 else "neutral"

    # Map emotions to Spanish (English emotion names are used internally)
    emotion_mapping = {"joy": "happy", "sadness": "sad", "anger": "angry", "surprise": "surprised", "neutral": "normal"}
    return emotion_mapping.get(primary_emotion, "neutral")

def select_eye_pattern_for_sentiment(sentiment):
    """Selects eye pattern based on sentiment (keys from face_patterns_eyes)."""
    if sentiment == "happy":
        return "happy" # Key for face_patterns_eyes
    elif sentiment == "sad":
        return "sad" # Key for face_patterns_eyes
    elif sentiment == "surprised":
        return "surprised" # Key for face_patterns_eyes
    elif sentiment == "angry":
        return "angry" # Key for face_patterns_eyes
    elif sentiment == "neutral":
        return "normal" # Key for face_patterns_eyes
    else:
        return "normal" # Default to normal

async def translate_text(text):
    translator = Translator()
    translation = await translator.translate(text, src="es", dest="en")
    return translation.text

def split_into_phrases(text):
    """Splits text into phrases based on sentence-ending punctuation."""
    phrases = []
    current_phrase = ""
    for i, char in enumerate(text):
        current_phrase += char
        if char in ['.', '!', '?']:
            # Check if it's an ellipsis ("...") to avoid splitting
            if char == '.' and text[i-2:i+1] == "..":
                continue  # Skip splitting if part of "..."
            phrases.append(current_phrase.strip())  # Store phrase
            current_phrase = ""
    if current_phrase: # Add the last phrase if any
        phrases.append(current_phrase.strip())
    return phrases