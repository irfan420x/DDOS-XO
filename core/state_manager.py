# Path: core/state_manager.py
from typing import Dict, Any

class StateManager:
    """
    LUNA-ULTRA State Manager: Tracks the current state and mode of the system.
    """
    def __init__(self):
        self.state = "idle"
        self.mode = "idle"
        self.last_action = None

    def set_state(self, state: str):
        self.state = state

    def get_state(self) -> str:
        return self.state

    def set_mode(self, mode: str):
        self.mode = mode

    def get_mode(self) -> str:
        return self.mode

    def set_last_action(self, action: str):
        self.last_action = action

    def get_last_action(self) -> str:
        return self.last_action
