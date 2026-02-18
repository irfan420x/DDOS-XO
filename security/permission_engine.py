# Path: security/permission_engine.py
import os
import logging
from enum import Enum
from typing import Dict, Any

class PermissionLevel(Enum):
    SAFE = 1
    STANDARD = 2
    ADVANCED = 3
    ROOT = 4

class PermissionEngine:
    """
    LUNA-ULTRA Permission Engine: Gated OS control.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        level_str = config.get('level') or config.get('security', {}).get('level', 'SAFE')
        self.current_level = PermissionLevel[level_str]
        self.require_confirmation = config.get('require_confirmation', True)
        self.setup_audit_log()
        self.blacklist = config.get('blacklist', [r"rm\s+-rf\s+/", r"mkfs", r"dd\s+if=/dev/zero", r"sudo\s+rm", r"chmod\s+777"])

    def setup_audit_log(self):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        # Use a separate logger for audit to avoid conflict with system log
        self.audit_logger = logging.getLogger("audit")
        if not self.audit_logger.handlers:
            handler = logging.FileHandler("logs/audit.log")
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.audit_logger.addHandler(handler)
            self.audit_logger.setLevel(logging.INFO)

    def check_permission(self, action_type: str, details: str = "") -> bool:
        """
        Verifies if the action is allowed based on current permission level and blacklist.
        """
        import re
        # 1. Regex-based Blacklist Check
        for pattern in self.blacklist:
            if re.search(pattern, details):
                self.audit_logger.critical(f"SECURITY ALERT: Blocked command attempt (Blacklist): {details}")
                return False

        permission_map = {
            "read_file": PermissionLevel.SAFE,
            "write_file": PermissionLevel.STANDARD,
            "shell_exec": PermissionLevel.ADVANCED,
            "system_control": PermissionLevel.ROOT,
            "mouse_click": PermissionLevel.STANDARD,
            "keyboard_type": PermissionLevel.STANDARD,
            "screen_capture": PermissionLevel.STANDARD
        }
        required_level = permission_map.get(action_type, PermissionLevel.ROOT)
        
        if self.current_level.value >= required_level.value:
            logging.info(f"Permission Granted: {action_type} - {details}")
            return True
        
        logging.warning(f"Permission Denied: {action_type} - {details}. Required: {required_level.name}, Current: {self.current_level.name}")
        return False

    def analyze_risk(self, action_type: str, details: str) -> float:
        risk = 0.0
        if "rm -rf" in details: risk = 1.0
        elif "sudo" in details: risk = 0.8
        elif "curl" in details and "|" in details: risk = 0.7
        return risk
