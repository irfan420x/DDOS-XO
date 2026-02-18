# Path: core/state_manager.py
import json
import os
import logging
from typing import Dict, Any, Optional

class StateManager:
    """
    LUNA-ULTRA State Manager: Handles session persistence, checkpointing, and system mode tracking.
    """
    def __init__(self, state_file: str = "memory/session_state.json"):
        self.state_file = state_file
        self.state = "idle"
        self.mode = "idle"
        self.last_action = None
        self.current_state = self.load_state()

    def load_state(self) -> Dict[str, Any]:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"StateManager: Failed to load state: {e}")
        return {
            "current_task": None,
            "completed_steps": [],
            "pending_steps": [],
            "context": {},
            "last_updated": None
        }

    def save_state(self):
        try:
            if not os.path.exists(os.path.dirname(self.state_file)):
                os.makedirs(os.path.dirname(self.state_file))
            with open(self.state_file, 'w') as f:
                json.dump(self.current_state, f, indent=4)
        except Exception as e:
            logging.error(f"StateManager: Failed to save state: {e}")

    def update_task(self, task: str, plan: list):
        self.current_state["current_task"] = task
        self.current_state["pending_steps"] = plan
        self.current_state["completed_steps"] = []
        self.save_state()

    def complete_step(self, step_result: Dict[str, Any]):
        if self.current_state["pending_steps"]:
            step = self.current_state["pending_steps"].pop(0)
            self.current_state["completed_steps"].append({
                "step": step,
                "result": step_result
            })
            self.save_state()

    def get_resume_data(self) -> Optional[Dict[str, Any]]:
        if self.current_state.get("current_task") and self.current_state.get("pending_steps"):
            return self.current_state
        return None

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
