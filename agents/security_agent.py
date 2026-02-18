# Path: agents/security_agent.py
from typing import Dict, Any
from security.permission_engine import PermissionEngine
from security.policy_engine import PolicyEngine

class SecurityAgent:
    """
    LUNA-ULTRA Security Agent: Handles risk analysis and policy enforcement.
    """
    def __init__(self, config: Dict[str, Any], permission_engine: PermissionEngine):
        self.config = config
        self.permission_engine = permission_engine
        self.policy_engine = PolicyEngine(config.get('security', {}))

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if action == "analyze_risk":
            risk = self.permission_engine.analyze_risk(params.get('action_type'), params.get('details'))
            return {"success": True, "risk_score": risk}
        elif action == "check_policy":
            allowed = self.policy_engine.is_allowed(params.get('command'))
            return {"success": True, "allowed": allowed}
        return {"error": f"Action {action} not supported"}
