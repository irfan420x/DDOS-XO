# Path: core/execution_watchdog.py
import time
import logging
import threading
import psutil
from typing import Dict, Any, Optional, Callable

class ExecutionWatchdog:
    """
    LUNA-ULTRA Execution Watchdog: Implements the Unlimited Execution Policy.
    Monitors CPU, memory, and process activity without hard time limits.
    """
    def __init__(self, controller):
        self.controller = controller
        self.active_tasks = {}
        self.stuck_threshold = 300  # 5 minutes of no activity/high usage
        self.is_running = False
        self._monitor_thread = None

    def start(self):
        if not self.is_running:
            self.is_running = True
            self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._monitor_thread.start()
            logging.info("ExecutionWatchdog: Started soft monitoring.")

    def stop(self):
        self.is_running = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=1)

    def register_task(self, task_id: str, task_name: str, process_id: Optional[int] = None):
        self.active_tasks[task_id] = {
            "name": task_name,
            "pid": process_id,
            "start_time": time.time(),
            "last_activity": time.time(),
            "notified": False
        }
        logging.info(f"ExecutionWatchdog: Registered task '{task_name}' (ID: {task_id})")

    def unregister_task(self, task_id: str):
        if task_id in self.active_tasks:
            del self.active_tasks[task_id]
            logging.info(f"ExecutionWatchdog: Unregistered task ID: {task_id}")

    def _monitor_loop(self):
        while self.is_running:
            try:
                current_time = time.time()
                for task_id, info in list(self.active_tasks.items()):
                    elapsed = current_time - info["start_time"]
                    
                    # Check if process is actually doing something
                    is_stuck = False
                    if info["pid"]:
                        try:
                            proc = psutil.Process(info["pid"])
                            if proc.status() == psutil.STATUS_ZOMBIE:
                                is_stuck = True
                            # If CPU usage is 0 for a long time, it might be stuck waiting
                            # But we allow unlimited time, so we only notify if it's very long
                        except psutil.NoSuchProcess:
                            is_stuck = True
                    
                    if elapsed > self.stuck_threshold and not info["notified"]:
                        self._notify_user_stuck(task_id, info)
                        info["notified"] = True
                
                time.sleep(10)
            except Exception as e:
                logging.error(f"ExecutionWatchdog Error: {e}")
                time.sleep(5)

    def _notify_user_stuck(self, task_id: str, info: Dict[str, Any]):
        msg = f"The task '{info['name']}' has been running for over 5 minutes. It appears to be active but taking longer than usual. Should I continue or would you like to interrupt it?"
        
        # Notify via GUI if available
        if hasattr(self.controller, 'gui') and self.controller.gui:
            self.controller.gui.signals.activity_logged.emit(f"⚠️ WATCHDOG: {msg}")
        
        # Notify via Telegram
        if self.controller.telegram:
            import asyncio
            asyncio.create_task(self.controller.telegram.send_notification(f"⚠️ Watchdog Alert: {msg}"))
        
        # Notify via Voice
        if hasattr(self.controller, 'gui') and self.controller.gui and self.controller.gui.voice_engine.enabled:
            self.controller.gui.voice_engine.speak(msg)
        
        logging.warning(f"ExecutionWatchdog: Task '{info['name']}' might be stuck. User notified.")
