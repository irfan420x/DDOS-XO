# Path: vision/screen_capture.py
import os
from typing import Dict, Any

class ScreenCapture:
    """
    LUNA-ULTRA Screen Capture: On-demand screen capture.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get('enabled', False)

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
