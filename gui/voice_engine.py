# Path: gui/voice_engine.py
import os
import logging
import threading
from gtts import gTTS
import pygame
import time

class VoiceEngine:
    """
    LUNA-ULTRA Voice Engine: Handles text-to-speech output.
    """
    def __init__(self, config: dict):
        self.config = config
        self.enabled = config.get('gui', {}).get('voice_mode', True)
        self.current_lang = config.get('gui', {}).get('voice_lang', 'en')
        self.available_langs = {
            'English': 'en',
            'Bengali': 'bn',
            'Hindi': 'hi',
            'Spanish': 'es',
            'French': 'fr'
        }
        self.temp_dir = "logs/voice"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        
        try:
            pygame.mixer.init()
        except Exception as e:
            logging.error(f"VoiceEngine: Failed to initialize pygame mixer: {e}")

    def toggle(self, state: bool):
        self.enabled = state
        logging.info(f"VoiceEngine: Voice mode set to {self.enabled}")

    def set_language(self, lang_name: str):
        if lang_name in self.available_langs:
            self.current_lang = self.available_langs[lang_name]
            logging.info(f"VoiceEngine: Language set to {lang_name} ({self.current_lang})")

    def speak(self, text: str):
        if not self.enabled:
            return
        threading.Thread(target=self._speak_task, args=(text,), daemon=True).start()

    def _speak_task(self, text: str):
        try:
            for f in os.listdir(self.temp_dir):
                if f.endswith(".mp3"):
                    try:
                        os.remove(os.path.join(self.temp_dir, f))
                    except:
                        pass

            filename = f"voice_{int(time.time())}.mp3"
            filepath = os.path.join(self.temp_dir, filename)
            
            clean_text = text.replace("*", "").replace("#", "").replace("`", "")
            
            # Use gTTS with current language
            tts = gTTS(text=clean_text, lang=self.current_lang)
            tts.save(filepath)

            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        except Exception as e:
            logging.error(f"VoiceEngine Error: {e}")
