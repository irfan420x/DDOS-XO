# Path: security/permission_engine.py
from enum import Enum
from typing import Dict, Any

class PermissionLevel(Enum):
    SAFE = 1
    STANDARD = 2
    ADVANCED = 3
    ROOT = 4

class PermissionEngine:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.current_level = PermissionLevel[config.get('level', 'SAFE')]
        self.require_confirmation = config.get('require_confirmation', True)

    def check_permission(self, action_type: str) -> bool:
        # Simple permission mapping
        permission_map = {
            "read": PermissionLevel.SAFE,
            "file_write": PermissionLevel.STANDARD,
            "shell_exec": PermissionLevel.ADVANCED,
            "system_control": PermissionLevel.ROOT
        }
        
        required_level = permission_map.get(action_type, PermissionLevel.ROOT)
        return self.current_level.value >= required_level.value

    def set_level(self, level_name: str):
        if level_name in PermissionLevel.__members__:
            self.current_level = PermissionLevel[level_name]
        else:
            raise ValueError(f"Invalid permission level: {level_name}")
