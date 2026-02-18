# Path: vision/screen_capture.py
import os
from typing import Optional

class ScreenCapture:
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.enabled = self.config.get('enabled', False)

    def capture(self, save_path: str = "logs/screenshot.png") -> bool:
        if not self.enabled:
            return False
        
        try:
            # Using standard linux tool for screenshot
            os.system(f"import -window root {save_path}")
            return True
        except Exception as e:
            print(f"Screen capture error: {str(e)}")
            return False
