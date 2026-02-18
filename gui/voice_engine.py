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
        self.temp_dir = "logs/voice"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        
        # Initialize pygame mixer for audio playback
        try:
            pygame.mixer.init()
        except Exception as e:
            logging.error(f"VoiceEngine: Failed to initialize pygame mixer: {e}")

    def toggle(self, state: bool):
        self.enabled = state
        logging.info(f"VoiceEngine: Voice mode set to {self.enabled}")

    def speak(self, text: str):
        if not self.enabled:
            return

        # Run in a separate thread to not block the GUI
        threading.Thread(target=self._speak_task, args=(text,), daemon=True).start()

    def _speak_task(self, text: str):
        try:
            # Clean up old voice files
            for f in os.listdir(self.temp_dir):
                if f.endswith(".mp3"):
                    try:
                        os.remove(os.path.join(self.temp_dir, f))
                    except:
                        pass

            # Generate speech
            filename = f"voice_{int(time.time())}.mp3"
            filepath = os.path.join(self.temp_dir, filename)
            
            # Remove markdown-like syntax for better speech
            clean_text = text.replace("*", "").replace("#", "").replace("`", "")
            
            tts = gTTS(text=clean_text, lang='en')
            tts.save(filepath)

            # Play audio
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        except Exception as e:
            logging.error(f"VoiceEngine Error: {e}")
