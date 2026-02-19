# Path: tools/registry.py
import logging
from typing import Dict, Any, List, Callable, Optional

class ToolRegistry:
    """
    LUNA-ULTRA Unified Tool Registry: Manages automation tools and permissions.
    """
    _instance = None
    _tools: Dict[str, Dict[str, Any]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, name: str, func: Callable, permission_level: str = "SAFE", description: str = ""):
        """Registers a tool with its required permission level."""
        cls._tools[name] = {
            "func": func,
            "permission_level": permission_level,
            "description": description
        }
        logging.info(f"ToolRegistry: Registered tool '{name}' (Level: {permission_level})")

    @classmethod
    def get_tool(cls, name: str) -> Optional[Dict[str, Any]]:
        """Retrieves a tool by name."""
        return cls._tools.get(name)

    @classmethod
    def list_tools(cls) -> List[str]:
        """Lists all registered tools."""
        return list(cls._tools.keys())

    @classmethod
    def execute_tool(cls, name: str, params: Dict[str, Any], current_permission: str = "SAFE") -> Dict[str, Any]:
        """Executes a tool after validating permission levels."""
        tool = cls.get_tool(name)
        if not tool:
            return {"success": False, "error": f"Tool '{name}' not found in registry."}

        # Permission Validation Logic
        levels = ["SAFE", "STANDARD", "ADVANCED", "ROOT"]
        required_idx = levels.index(tool["permission_level"])
        current_idx = levels.index(current_permission)

        if current_idx < required_idx:
            return {
                "success": False, 
                "error": f"Permission Denied: Tool '{name}' requires {tool['permission_level']} access. Current level: {current_permission}"
            }

        try:
            # Execute the tool function
            import asyncio
            if asyncio.iscoroutinefunction(tool["func"]):
                # This would need to be awaited in an async context
                return {"success": False, "error": "Async tools must be executed via an async wrapper."}
            
            result = tool["func"](**params)
            return {"success": True, "output": result}
        except Exception as e:
            logging.error(f"ToolRegistry: Error executing tool '{name}': {e}")
            return {"success": False, "error": str(e)}
