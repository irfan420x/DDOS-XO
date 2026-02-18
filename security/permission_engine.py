# Path: security/permission_engine.py

from enum import IntEnum
from typing import Dict, Any, List
from loguru import logger

class PermissionLevel(IntEnum):
    DENIED = 0
    SAFE = 1
    STANDARD = 2
    ADVANCED = 3
    ROOT = 4

class PermissionEngine:
    def __init__(self, config_manager):
        self.config = config_manager
        self.level = self._parse_level(self.config.get("security.level", "SAFE"))
        self.restricted_cmds = self.config.get("security.restricted_commands", [])
        self.protected_paths = self.config.get("security.protected_paths", [])

    def _parse_level(self, level_str: str) -> PermissionLevel:
        try:
            return PermissionLevel[level_str.upper()]
        except KeyError:
            return PermissionLevel.SAFE

    def check_permission(self, module: str, action: str, context: Dict[str, Any]) -> bool:
        logger.info(f"Permission Check: [{module}] -> {action} (Level: {self.level.name})")
        
        # Global Safety Filters
        if not self._safety_filter(action, context):
            return False

        # Module-specific logic
        if self.level == PermissionLevel.ROOT:
            return True
        
        if self.level == PermissionLevel.DENIED:
            return False

        # Example logic for SAFE level
        if self.level == PermissionLevel.SAFE:
            allowed_actions = ["read", "status", "listen", "speak"]
            return action in allowed_actions

        return True

    def _safety_filter(self, action: str, context: Dict[str, Any]) -> bool:
        # Command Blacklist
        if "command" in context:
            cmd = context["command"].lower()
            if any(r in cmd for r in self.restricted_cmds):
                logger.warning(f"BLOCKED: Dangerous command detected: {cmd}")
                return False

        # Path Protection
        if "path" in context:
            path = context["path"]
            if any(path.startswith(p) for p in self.protected_paths):
                logger.warning(f"BLOCKED: Access to protected path: {path}")
                return False

        return True

    def upgrade_level(self, new_level: str, token: str):
        # In a real system, this would validate a secure token/password
        if token == "ADMIN_TOKEN": # Placeholder
            self.level = self._parse_level(new_level)
            logger.success(f"Security level upgraded to {self.level.name}")
            return True
        return False
