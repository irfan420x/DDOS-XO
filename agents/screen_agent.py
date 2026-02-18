# Path: agents/screen_agent.py
import os
import time
from typing import Dict, Any, Optional
from vision.screen_capture import ScreenCapture
from vision.ocr_engine import OCREngine

class ScreenAgent:
    """
    LUNA-ULTRA Screen Agent: Handles on-demand screen awareness and capture with permission gating.
    """
    def __init__(self, config: Dict[str, Any], permission_engine: Any):
        self.config = config
        self.permission_engine = permission_engine
        self.capture_engine = ScreenCapture(config.get('vision', {}))
        self.ocr_engine = OCREngine(config.get('vision', {}))
        self.last_capture_path = None

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes screen-related actions.
        """
        if action == "capture":
            return await self.capture_screen()
        elif action == "capture_and_ocr":
            return await self.capture_and_ocr(params.get('path'))
        elif action == "get_last_capture":
            return {"success": True, "path": self.last_capture_path}
        return {"error": f"Action {action} not supported"}

    async def capture_screen(self, path: Optional[str] = None) -> Dict[str, Any]:
        """
        Captures the screen if permission is granted.
        """
        if not self.permission_engine.check_permission("screen_capture", "Taking a screenshot for analysis"):
            return {"success": False, "error": "Permission Denied: Screen capture blocked."}

        try:
            if not path:
                timestamp = int(time.time())
                path = f"vision/capture_{timestamp}.png"
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            result = self.capture_engine.capture(path)
            if result:
                self.last_capture_path = path
                return {
                    "success": True, 
                    "path": path, 
                    "message": "Screen captured successfully."
                }
            else:
                return {"success": False, "error": "Capture failed."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def capture_and_ocr(self, path: Optional[str] = None) -> Dict[str, Any]:
        """
        Captures the screen and extracts text using OCR.
        """
        capture_result = await self.capture_screen(path)
        if not capture_result["success"]:
            return capture_result
            
        img_path = capture_result["path"]
        try:
            text = self.ocr_engine.extract_text(img_path)
            return {
                "success": True,
                "path": img_path,
                "text": text
            }
        except Exception as e:
            return {"success": False, "error": f"OCR failed: {str(e)}", "path": img_path}
