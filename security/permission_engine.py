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
        self.current_level = PermissionLevel[config.get('level', 'SAFE')]
        self.require_confirmation = config.get('require_confirmation', True)
        self.setup_audit_log()

    def setup_audit_log(self):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        logging.basicConfig(filename="logs/audit.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def check_permission(self, action_type: str, details: str = "") -> bool:
        permission_map = {
            "read_file": PermissionLevel.SAFE,
            "write_file": PermissionLevel.STANDARD,
            "shell_exec": PermissionLevel.ADVANCED,
            "system_control": PermissionLevel.ROOT
        }
        required_level = permission_map.get(action_type, PermissionLevel.ROOT)
        
        if self.current_level.value >= required_level.value:
            logging.info(f"Permission Granted: {action_type} - {details}")
            return True
        
        logging.warning(f"Permission Denied: {action_type} - {details}")
        return False

    def analyze_risk(self, action_type: str, details: str) -> float:
        risk = 0.0
        if "rm -rf" in details: risk = 1.0
        elif "sudo" in details: risk = 0.8
        return risk
