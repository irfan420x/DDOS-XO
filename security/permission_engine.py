# Path: security/permission_engine.py
from enum import Enum
from typing import Dict, Any, List, Optional
import logging

class PermissionLevel(Enum):
    SAFE = 1      # Read-only access
    STANDARD = 2  # File and application level access
    ADVANCED = 3  # Shell and Docker execution allowed
    ROOT = 4      # Full system control

class PermissionEngine:
    """
    LUNA-ULTRA Permission Engine: Strict gated OS control.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.current_level = PermissionLevel[config.get('level', 'SAFE')]
        self.require_confirmation = config.get('require_confirmation', True)
        self.audit_logger = logging.getLogger("luna_audit")
        self.setup_audit_log()

    def setup_audit_log(self):
        log_path = "logs/audit.log"
        if not os.path.exists("logs"):
            os.makedirs("logs")
        
        handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.audit_logger.addHandler(handler)
        self.audit_logger.setLevel(logging.INFO)

    def check_permission(self, action_type: str, details: str = "") -> bool:
        """
        Gated permission check for every action.
        """
        permission_map = {
            "read_file": PermissionLevel.SAFE,
            "write_file": PermissionLevel.STANDARD,
            "open_app": PermissionLevel.STANDARD,
            "shell_exec": PermissionLevel.ADVANCED,
            "docker_run": PermissionLevel.ADVANCED,
            "system_reboot": PermissionLevel.ROOT,
            "delete_system_file": PermissionLevel.ROOT
        }
        
        required_level = permission_map.get(action_type, PermissionLevel.ROOT)
        
        # 1. Level Check
        if self.current_level.value < required_level.value:
            self.audit_logger.warning(f"Permission Denied: {action_type} (Required: {required_level.name}, Current: {self.current_level.name})")
            return False
        
        # 2. Risk Analysis (Simulated)
        risk_score = self.analyze_risk(action_type, details)
        
        # 3. Confirmation Check
        if self.require_confirmation and risk_score > 0.5:
            # In a real GUI, this would trigger a popup
            self.audit_logger.info(f"Permission Pending Confirmation: {action_type}")
            return False # Default to false if confirmation is required but not handled here
            
        self.audit_logger.info(f"Permission Granted: {action_type} - {details}")
        return True

    def analyze_risk(self, action_type: str, details: str) -> float:
        """
        Simple risk analysis based on action type and details.
        """
        high_risk_keywords = ["rm -rf", "sudo", "format", "delete", "kill"]
        risk_score = 0.0
        
        if action_type in ["shell_exec", "system_reboot"]:
            risk_score += 0.6
            
        for keyword in high_risk_keywords:
            if keyword in details.lower():
                risk_score += 0.4
                
        return min(risk_score, 1.0)

class PolicyEngine:
    """
    Enforces security policies and command blacklists.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.blacklist = config.get('blacklist', ["rm -rf /", "mkfs", "dd if=/dev/zero"])

    def is_allowed(self, command: str) -> bool:
        for blocked in self.blacklist:
            if blocked in command:
                return False
        return True
