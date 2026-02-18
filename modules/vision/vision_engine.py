# Path: modules/vision/vision_engine.py

import cv2
import pytesseract
import mss
import numpy as np
from PIL import Image
from loguru import logger

class VisionEngine:
    def __init__(self, config):
        self.config = config
        self.sct = mss.mss()

    def capture_screen(self) -> np.ndarray:
        screenshot = self.sct.grab(self.sct.monitors[1])
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    def perform_ocr(self, image: np.ndarray = None) -> str:
        if image is None:
            image = self.capture_screen()
        
        try:
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            logger.error(f"OCR Error: {e}")
            return ""

    def detect_objects(self, image: np.ndarray = None):
        # Placeholder for YOLO/Object detection
        logger.info("Object detection triggered (Placeholder)")
        return []
