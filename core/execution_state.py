# Path: core/execution_state.py
import logging
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime


class ExecutionStateManager:
    """
    Execution State Manager for Agent Mode.
    Persists execution state to enable resumption after crashes or token limit errors.
    """
    
    STATE_FILE = "agent_execution_state.json"
    STATE_DIR = "data"
    
    def __init__(self):
        self.state_file_path = os.path.join(self.STATE_DIR, self.STATE_FILE)
        self.current_state: Optional[Dict[str, Any]] = None
        
        # Ensure state directory exists
        os.makedirs(self.STATE_DIR, exist_ok=True)
        
        # Load existing state if available
        self._load_state()
        
        logging.info("ExecutionStateManager: Initialized.")
    
    def initialize_execution(self, goal: str, plan: Dict[str, Any]):
        """
        Initialize a new execution state.
        """
        self.current_state = {
            "goal": goal,
            "plan": plan,
            "current_step": 0,
            "completed_steps": [],
            "remaining_steps": list(range(len(plan.get("steps", [])))),
            "retry_count": 0,
            "status": "running",
            "started_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "errors": [],
            "results": []
        }
        
        self._save_state()
        logging.info(f"ExecutionStateManager: Initialized execution for goal: {goal}")
    
    def update_current_step(self, step_index: int):
        """
        Update the current step being executed.
        """
        if not self.current_state:
            logging.warning("ExecutionStateManager: No active execution to update.")
            return
        
        self.current_state["current_step"] = step_index
        self.current_state["last_updated"] = datetime.now().isoformat()
        self._save_state()
        
        logging.info(f"ExecutionStateManager: Updated current step to {step_index}")
    
    def mark_step_complete(self, step_index: int, success: bool, result: Optional[Dict[str, Any]] = None):
        """
        Mark a step as complete and update state.
        """
        if not self.current_state:
            logging.warning("ExecutionStateManager: No active execution to update.")
            return
        
        # Add to completed steps
        if step_index not in self.current_state["completed_steps"]:
            self.current_state["completed_steps"].append(step_index)
        
        # Remove from remaining steps
        if step_index in self.current_state["remaining_steps"]:
            self.current_state["remaining_steps"].remove(step_index)
        
        # Store result
        if result:
            self.current_state["results"].append({
                "step_index": step_index,
                "success": success,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })
        
        # Update retry count
        if not success:
            self.current_state["retry_count"] += 1
        else:
            self.current_state["retry_count"] = 0  # Reset on success
        
        self.current_state["last_updated"] = datetime.now().isoformat()
        self._save_state()
        
        logging.info(f"ExecutionStateManager: Step {step_index} marked as {'complete' if success else 'failed'}")
    
    def mark_execution_complete(self, success: bool):
        """
        Mark the entire execution as complete.
        """
        if not self.current_state:
            logging.warning("ExecutionStateManager: No active execution to complete.")
            return
        
        self.current_state["status"] = "completed" if success else "failed"
        self.current_state["completed_at"] = datetime.now().isoformat()
        self.current_state["last_updated"] = datetime.now().isoformat()
        self._save_state()
        
        logging.info(f"ExecutionStateManager: Execution marked as {self.current_state['status']}")
    
    def add_error(self, error: str, step_index: Optional[int] = None):
        """
        Add an error to the execution state.
        """
        if not self.current_state:
            logging.warning("ExecutionStateManager: No active execution to add error to.")
            return
        
        error_entry = {
            "error": error,
            "step_index": step_index,
            "timestamp": datetime.now().isoformat()
        }
        
        self.current_state["errors"].append(error_entry)
        self.current_state["last_updated"] = datetime.now().isoformat()
        self._save_state()
        
        logging.error(f"ExecutionStateManager: Error added: {error}")
    
    def has_active_execution(self) -> bool:
        """
        Check if there is an active execution that can be resumed.
        """
        if not self.current_state:
            return False
        
        return self.current_state.get("status") == "running"
    
    def get_state(self) -> Optional[Dict[str, Any]]:
        """
        Get the current execution state.
        """
        return self.current_state
    
    def clear_state(self):
        """
        Clear the current execution state.
        """
        self.current_state = None
        
        # Remove state file
        if os.path.exists(self.state_file_path):
            os.remove(self.state_file_path)
            logging.info("ExecutionStateManager: State file removed.")
        
        logging.info("ExecutionStateManager: State cleared.")
    
    def _save_state(self):
        """
        Save current state to file.
        """
        if not self.current_state:
            return
        
        try:
            with open(self.state_file_path, 'w') as f:
                json.dump(self.current_state, f, indent=2)
            logging.debug("ExecutionStateManager: State saved to file.")
        except Exception as e:
            logging.error(f"ExecutionStateManager: Failed to save state: {e}")
    
    def _load_state(self):
        """
        Load state from file if it exists.
        """
        if not os.path.exists(self.state_file_path):
            logging.debug("ExecutionStateManager: No existing state file found.")
            return
        
        try:
            with open(self.state_file_path, 'r') as f:
                self.current_state = json.load(f)
            logging.info("ExecutionStateManager: State loaded from file.")
        except Exception as e:
            logging.error(f"ExecutionStateManager: Failed to load state: {e}")
            self.current_state = None
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """
        Get a summary of execution progress.
        """
        if not self.current_state:
            return {
                "active": False,
                "message": "No active execution."
            }
        
        total_steps = len(self.current_state.get("plan", {}).get("steps", []))
        completed = len(self.current_state.get("completed_steps", []))
        current = self.current_state.get("current_step", 0)
        
        return {
            "active": True,
            "goal": self.current_state.get("goal"),
            "status": self.current_state.get("status"),
            "total_steps": total_steps,
            "completed_steps": completed,
            "current_step": current,
            "progress_percentage": (completed / total_steps * 100) if total_steps > 0 else 0,
            "retry_count": self.current_state.get("retry_count", 0),
            "started_at": self.current_state.get("started_at"),
            "last_updated": self.current_state.get("last_updated"),
            "errors_count": len(self.current_state.get("errors", []))
        }
