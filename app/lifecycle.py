# Path: app/lifecycle.py
import sys
from typing import Any

class LifecycleManager:
    """
    Manages the application lifecycle (startup, shutdown, always-on).
    """
    def __init__(self, controller: Any):
        self.controller = controller
        self.is_running = True

    async def shutdown(self):
        """
        Gracefully shuts down the system.
        """
        print("🌙 LUNA-ULTRA: Shutting down systems...")
        # Save memory, close connections, etc.
        self.controller.memory_manager.save_memory()
        self.is_running = False
        print("🌙 LUNA-ULTRA: Shutdown complete. Goodbye, IRFAN.")
        sys.exit(0)
