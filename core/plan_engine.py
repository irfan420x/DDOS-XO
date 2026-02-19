# Path: core/plan_engine.py
import logging
import json
import re
from typing import Dict, Any, List


class PlanEngine:
    """
    Plan Engine for Agent Mode.
    Generates structured JSON plans with risk assessment and complexity estimation.
    """
    
    def __init__(self, controller):
        self.controller = controller
        logging.info("PlanEngine: Initialized.")
    
    async def generate_plan(self, goal: str) -> Dict[str, Any]:
        """
        Generate a structured plan for the given goal.
        
        Returns:
        {
            "success": bool,
            "plan": {
                "goal": str,
                "steps": [
                    {
                        "id": int,
                        "description": str,
                        "agent": str,
                        "action": str,
                        "params": dict
                    }
                ],
                "risk_level": str,  # LOW, MEDIUM, HIGH, CRITICAL
                "estimated_complexity": str,  # SIMPLE, MODERATE, COMPLEX, VERY_COMPLEX
                "files_expected_to_change": list
            }
        }
        """
        
        logging.info(f"PlanEngine: Generating plan for goal: {goal}")
        
        # Get available agents and tools
        available_agents = list(self.controller.orchestrator.agents.keys())
        available_tools = self.controller.orchestrator.agents.get("dynamic").list_available_tools() if self.controller.orchestrator.agents.get("dynamic") else []
        
        # Create planning prompt
        planning_prompt = f"""
You are an AI planning engine. Generate a detailed, structured execution plan for the following goal:

GOAL: {goal}

Available Agents: {', '.join(available_agents)}
Available Tools: {', '.join(available_tools) if available_tools else 'Standard system tools'}

Generate a JSON plan with the following structure:
{{
    "goal": "...",
    "steps": [
        {{
            "id": 1,
            "description": "Clear description of what this step does",
            "agent": "agent_name",
            "action": "method_or_tool_name",
            "params": {{"key": "value"}}
        }}
    ],
    "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
    "estimated_complexity": "SIMPLE|MODERATE|COMPLEX|VERY_COMPLEX",
    "files_expected_to_change": ["file1.py", "file2.py"]
}}

Risk Assessment Guidelines:
- LOW: Read-only operations, simple queries
- MEDIUM: File modifications, non-critical system changes
- HIGH: System configuration changes, external API calls
- CRITICAL: Root operations, destructive actions, security-sensitive operations

Complexity Guidelines:
- SIMPLE: 1-3 steps, single agent
- MODERATE: 4-7 steps, multiple agents
- COMPLEX: 8-15 steps, coordination required
- VERY_COMPLEX: 16+ steps, multi-phase execution

Return ONLY the JSON plan, no additional text.
"""
        
        try:
            # Generate plan using LLM
            plan_response = await self.controller.llm_router.generate_response(planning_prompt)
            
            # Extract JSON from response
            plan_json = self._extract_json(plan_response)
            
            if not plan_json:
                return {
                    "success": False,
                    "error": "Failed to extract valid JSON plan from LLM response."
                }
            
            # Validate plan structure
            validation_result = self._validate_plan(plan_json)
            
            if not validation_result.get("valid"):
                return {
                    "success": False,
                    "error": f"Plan validation failed: {validation_result.get('error')}"
                }
            
            # Enhance plan with additional metadata
            plan_json["generated_at"] = self._get_timestamp()
            plan_json["status"] = "pending_approval"
            
            logging.info(f"PlanEngine: Successfully generated plan with {len(plan_json.get('steps', []))} steps.")
            
            return {
                "success": True,
                "plan": plan_json
            }
            
        except Exception as e:
            logging.error(f"PlanEngine: Error generating plan: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _extract_json(self, text: str) -> Dict[str, Any]:
        """
        Extract JSON object from text response.
        """
        try:
            # Try to find JSON object in text
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            
            # If no match, try to parse entire text as JSON
            return json.loads(text)
        except json.JSONDecodeError as e:
            logging.error(f"PlanEngine: JSON decode error: {e}")
            return None
        except Exception as e:
            logging.error(f"PlanEngine: Error extracting JSON: {e}")
            return None
    
    def _validate_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate plan structure and required fields.
        """
        required_fields = ["goal", "steps", "risk_level", "estimated_complexity"]
        
        # Check required fields
        for field in required_fields:
            if field not in plan:
                return {
                    "valid": False,
                    "error": f"Missing required field: {field}"
                }
        
        # Validate steps
        steps = plan.get("steps", [])
        if not isinstance(steps, list) or len(steps) == 0:
            return {
                "valid": False,
                "error": "Steps must be a non-empty list."
            }
        
        # Validate each step
        for idx, step in enumerate(steps):
            step_required = ["id", "description", "agent", "action"]
            for field in step_required:
                if field not in step:
                    return {
                        "valid": False,
                        "error": f"Step {idx + 1} missing required field: {field}"
                    }
        
        # Validate risk level
        valid_risk_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        if plan.get("risk_level") not in valid_risk_levels:
            return {
                "valid": False,
                "error": f"Invalid risk_level. Must be one of: {', '.join(valid_risk_levels)}"
            }
        
        # Validate complexity
        valid_complexity = ["SIMPLE", "MODERATE", "COMPLEX", "VERY_COMPLEX"]
        if plan.get("estimated_complexity") not in valid_complexity:
            return {
                "valid": False,
                "error": f"Invalid estimated_complexity. Must be one of: {', '.join(valid_complexity)}"
            }
        
        return {"valid": True}
    
    def _get_timestamp(self) -> str:
        """
        Get current timestamp in ISO format.
        """
        from datetime import datetime
        return datetime.now().isoformat()
    
    def format_plan_for_display(self, plan: Dict[str, Any]) -> str:
        """
        Format plan for display in GUI or console.
        """
        output = []
        output.append("=" * 60)
        output.append("AGENT MODE - EXECUTION PLAN")
        output.append("=" * 60)
        output.append(f"\nGOAL: {plan.get('goal', 'N/A')}")
        output.append(f"RISK LEVEL: {plan.get('risk_level', 'N/A')}")
        output.append(f"COMPLEXITY: {plan.get('estimated_complexity', 'N/A')}")
        output.append(f"\nSTEPS ({len(plan.get('steps', []))}):")
        output.append("-" * 60)
        
        for step in plan.get("steps", []):
            output.append(f"\n{step.get('id')}. {step.get('description')}")
            output.append(f"   Agent: {step.get('agent')} | Action: {step.get('action')}")
            if step.get("params"):
                output.append(f"   Params: {step.get('params')}")
        
        output.append("\n" + "-" * 60)
        
        if plan.get("files_expected_to_change"):
            output.append(f"\nEXPECTED FILE CHANGES:")
            for file in plan.get("files_expected_to_change", []):
                output.append(f"  - {file}")
        
        output.append("\n" + "=" * 60)
        
        return "\n".join(output)
