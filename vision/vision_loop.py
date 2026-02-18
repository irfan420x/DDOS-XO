# Path: vision/vision_loop.py
import asyncio
import logging
import time
from typing import Any
from vision.screen_capture import ScreenCapture
from vision.ocr_engine import OCREngine

class VisionLoop:
    """
    LUNA-ULTRA Vision Loop: Periodically monitors the screen and reacts to changes.
    """
    def __init__(self, controller: Any):
        self.controller = controller
        self.config = controller.config.get("vision", {})
        self.enabled = self.config.get("loop_enabled", True)
        self.interval = self.config.get("loop_interval", 10) # Seconds
        self.screen_capture = ScreenCapture(self.config)
        self.ocr_engine = OCREngine(self.config)
        self.running = False
        self.last_screen_text = ""

    async def start(self):
        if not self.enabled: return
        self.running = True
        logging.info(f"VisionLoop: Started with interval {self.interval}s")
        while self.running:
            try:
                await self.monitor_step()
            except Exception as e:
                logging.error(f"VisionLoop: Error during monitoring: {e}")
            await asyncio.sleep(self.interval)

    async def stop(self):
        self.running = False
        logging.info("VisionLoop: Stopped.")

    async def monitor_step(self):
        # 1. Capture Screen
        screenshot_path = self.screen_capture.capture()
        if not screenshot_path: return

        # 2. Extract Text
        current_text = self.ocr_engine.extract_text(screenshot_path)
        
        # 3. Detect Critical Changes (Errors, Alerts)
        critical_keywords = ["error", "failed", "critical", "warning", "access denied", "success"]
        found_keywords = [kw for kw in critical_keywords if kw in current_text.lower()]
        
        if found_keywords and current_text != self.last_screen_text:
            msg = f"VisionLoop detected critical screen content: {', '.join(found_keywords)}"
            logging.info(msg)
            
            # Notify User via GUI and Telegram
            if hasattr(self.controller, 'gui') and self.controller.gui:
                self.controller.gui.update_activity(f"👁️ Vision Alert: {msg}")
            
            if self.controller.telegram.enabled:
                await self.controller.telegram.send_notification(msg)
                
            self.last_screen_text = current_text
