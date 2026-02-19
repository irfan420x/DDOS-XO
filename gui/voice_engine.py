# Path: gui/voice_engine.py
import os
import logging
import threading
import time
import queue
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from gtts import gTTS
import pygame
from typing import Optional, Callable, Dict, Any

class VoiceEngine:
    """
    LUNA-ULTRA Voice Engine v2.0: Voice-First Intelligent Interaction.
    Handles natural TTS and STT with task-aware awareness.
    """
    def __init__(self, config: dict):
        self.config = config
        self.enabled = config.get('gui', {}).get('voice_mode', False)
        self.current_lang = config.get('gui', {}).get('voice_lang', 'en')
        self.wake_word = "luna"
        
        self.temp_dir = "logs/voice"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
            
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        self.is_listening = False
        self.is_speaking = False
        
        try:
            pygame.mixer.init()
        except Exception as e:
            logging.error(f"VoiceEngine: Failed to initialize pygame mixer: {e}")

    def toggle(self, state: bool):
        self.enabled = state
        logging.info(f"VoiceEngine: Voice mode set to {self.enabled}")
        if self.enabled:
            self.start_listening_thread()

    def speak(self, text: str, task_context: Optional[Dict[str, Any]] = None):
        """
        Speaks the given text. If task_context is provided, it can adjust the tone.
        """
        if not self.enabled or not text:
            return
            
        # Task-aware voice enhancement
        if task_context:
            status = task_context.get("status", "").lower()
            if status == "success":
                text = f"Great news! {text}"
            elif status == "failed":
                text = f"I'm sorry, but I encountered an issue. {text}"
        
        threading.Thread(target=self._speak_task, args=(text,), daemon=True).start()

    def announce_task_start(self, task_name: str):
        """Announces the start of a task in a human-like way."""
        phrases = [
            f"Alright, I'm starting the {task_name} now.",
            f"Got it. I'll begin working on {task_name} immediately.",
            f"I understand. Let me handle the {task_name} for you."
        ]
        import random
        self.speak(random.choice(phrases))

    def announce_task_status(self, task_name: str, status: str, reason: str = ""):
        """Announces the completion status of a task."""
        if status.lower() == "success":
            self.speak(f"The {task_name} has been completed successfully.")
        elif status.lower() == "failed":
            msg = f"The {task_name} failed."
            if reason:
                msg += f" The reason was: {reason}"
            self.speak(msg)
        elif status.lower() == "partial":
            self.speak(f"The {task_name} was partially completed.")

    def _speak_task(self, text: str):
        self.is_speaking = True
        try:
            # Clean text for TTS
            clean_text = text.replace("*", "").replace("#", "").replace("`", "")
            
            filename = f"voice_{int(time.time())}.mp3"
            filepath = os.path.join(self.temp_dir, filename)
            
            # Use gTTS for natural-sounding voice
            tts = gTTS(text=clean_text, lang=self.current_lang, slow=False)
            tts.save(filepath)

            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        except Exception as e:
            logging.error(f"VoiceEngine Speak Error: {e}")
        finally:
            self.is_speaking = False

    def start_listening_thread(self):
        if not self.is_listening:
            threading.Thread(target=self._listen_loop, daemon=True).start()

    def _listen_loop(self):
        self.is_listening = True
        logging.info("VoiceEngine: Listening for wake word 'LUNA'...")
        
        while self.enabled:
            if self.is_speaking:
                time.sleep(0.5)
                continue
                
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                text = self.recognizer.recognize_google(audio).lower()
                logging.info(f"VoiceEngine Heard: {text}")
                
                if self.wake_word in text:
                    logging.info("VoiceEngine: Wake word detected!")
                    if hasattr(self, 'on_wake_word'):
                        self.on_wake_word()
                        
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                logging.debug(f"VoiceEngine Listen Error: {e}")
                time.sleep(1)
        
        self.is_listening = False
