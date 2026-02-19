# Path: core/task_queue.py
import asyncio
import logging
from typing import Dict, Any, List, Optional

class TaskQueue:
    """
    LUNA-ULTRA Task Queue System: Manages sequential task execution and status.
    """
    def __init__(self, controller):
        self.controller = controller
        self.queue: asyncio.Queue = asyncio.Queue()
        self.history: List[Dict[str, Any]] = []
        self.current_task: Optional[Dict[str, Any]] = None
        self.running = False

    async def add_task(self, task_name: str, func: Any, params: Dict[str, Any] = None) -> str:
        """Adds a task to the queue and returns its ID."""
        task_id = f"task_{len(self.history) + 1}"
        task = {
            "id": task_id,
            "name": task_name,
            "func": func,
            "params": params or {},
            "status": "QUEUED",
            "result": None
        }
        await self.queue.put(task)
        self.history.append(task)
        logging.info(f"TaskQueue: Added task '{task_name}' (ID: {task_id})")
        
        if not self.running:
            asyncio.create_task(self.process_queue())
            
        return task_id

    async def process_queue(self):
        """Processes tasks in the queue sequentially."""
        self.running = True
        while not self.queue.empty():
            self.current_task = await self.queue.get()
            self.current_task["status"] = "RUNNING"
            logging.info(f"TaskQueue: Processing task '{self.current_task['name']}'")
            
            try:
                if asyncio.iscoroutinefunction(self.current_task["func"]):
                    res = await self.current_task["func"](**self.current_task["params"])
                else:
                    res = self.current_task["func"](**self.current_task["params"])
                
                self.current_task["status"] = "COMPLETED"
                self.current_task["result"] = res
            except Exception as e:
                logging.error(f"TaskQueue: Error processing task '{self.current_task['name']}': {e}")
                self.current_task["status"] = "FAILED"
                self.current_task["result"] = str(e)
            
            self.queue.task_done()
            # Update GUI if available
            if hasattr(self.controller, "gui") and self.controller.gui:
                self.controller.gui.update_activity(f"Task {self.current_task['name']} {self.current_task['status']}")
        
        self.current_task = None
        self.running = False

    def get_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Returns the last N tasks from history."""
        return self.history[-limit:]

class CostMonitor:
    """
    LUNA-ULTRA Cost Monitor: Tracks token usage and estimated API costs.
    """
    def __init__(self, controller):
        self.controller = controller
        self.total_tokens = 0
        self.estimated_cost = 0.0
        self.daily_limit = self.controller.config.get("llm", {}).get("daily_limit", 5.0) # USD

    def track_usage(self, tokens: int, model: str = "deepseek-chat"):
        """Tracks token usage and updates estimated cost."""
        # Simplified pricing (e.g., $0.01 per 1k tokens)
        cost_per_1k = 0.01
        self.total_tokens += tokens
        self.estimated_cost += (tokens / 1000) * cost_per_1k
        
        if self.estimated_cost > self.daily_limit:
            logging.warning(f"CostMonitor: Daily limit reached! Estimated cost: ${self.estimated_cost:.2f}")
            if hasattr(self.controller, "gui") and self.controller.gui:
                self.controller.gui.update_activity(f"⚠️ API Cost Alert: ${self.estimated_cost:.2f} reached!")

    def get_report(self) -> Dict[str, Any]:
        """Returns the current cost report."""
        return {
            "total_tokens": self.total_tokens,
            "estimated_cost": round(self.estimated_cost, 4),
            "daily_limit": self.daily_limit
        }

class RiskScoringEngine:
    """
    LUNA-ULTRA Risk Scoring Engine: Assigns risk scores to commands before execution.
    """
    def __init__(self, controller):
        self.controller = controller
        self.risk_patterns = {
            r"rm -rf": 100,
            r"sudo": 80,
            r"chmod": 60,
            r"curl.*\|.*bash": 95,
            r"wget.*\|.*bash": 95,
            r"mv .*/dev/null": 90,
            r"dd if=/dev/zero": 100,
            r"mkfs": 100,
            r"reboot": 70,
            r"shutdown": 70
        }

    def score_command(self, command: str) -> int:
        """Calculates a risk score (0-100) for a given command."""
        import re
        max_score = 0
        for pattern, score in self.risk_patterns.items():
            if re.search(pattern, command, re.IGNORECASE):
                max_score = max(max_score, score)
        
        # Base score for any shell command
        if not max_score and command:
            max_score = 10
            
        return max_score

    def get_risk_level(self, score: int) -> str:
        """Returns a human-readable risk level based on the score."""
        if score >= 90: return "CRITICAL"
        if score >= 70: return "HIGH"
        if score >= 40: return "MEDIUM"
        if score >= 10: return "LOW"
        return "SAFE"
