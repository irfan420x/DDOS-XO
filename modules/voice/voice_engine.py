# Path: modules/voice/voice_engine.py

import pyttsx3
import speech_recognition as sr
from loguru import logger

class VoiceEngine:
    def __init__(self, config):
        self.config = config
        self.tts_engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self._setup_voice()

    def _setup_voice(self):
        voices = self.tts_engine.getProperty('voices')
        # Prefer a specific voice if configured
        self.tts_engine.setProperty('rate', 175)
        self.tts_engine.setProperty('volume', 1.0)

    def speak(self, text: str):
        logger.info(f"Speaking: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self) -> str:
        with sr.Microphone() as source:
            logger.info("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio)
                logger.info(f"Recognized: {text}")
                return text
            except sr.UnknownValueError:
                return ""
            except Exception as e:
                logger.error(f"Voice Recognition Error: {e}")
                return ""
