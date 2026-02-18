# Path: agents/screen_agent.py
from typing import Dict, Any
from vision.screen_capture import ScreenCapture
from vision.ocr_engine import OCREngine

class ScreenAgent:
    """
    LUNA-ULTRA Screen Agent: Handles vision-related tasks.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.capture = ScreenCapture(config.get('vision', {}))
        self.ocr = OCREngine(config.get('vision', {}))

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if action == "capture_and_ocr":
            path = params.get('path', "logs/screenshot.png")
            if self.capture.capture(path):
                text = self.ocr.extract_text(path)
                return {"success": True, "text": text, "path": path}
            return {"success": False, "error": "Capture failed"}
        return {"error": f"Action {action} not supported"}
