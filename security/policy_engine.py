# Path: security/policy_engine.py
from typing import Dict, Any, List

class PolicyEngine:
    """
    LUNA-ULTRA Policy Engine: Command blacklist and security policies.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.blacklist = config.get('blacklist', ["rm -rf /", "mkfs", "dd if=/dev/zero"])

    def is_allowed(self, command: str) -> bool:
        for blocked in self.blacklist:
            if blocked in command:
                return False
        return True
