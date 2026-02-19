# Path: agents/thought_loop.py
import logging
import json
import re
from typing import Dict, Any, List, Optional

class ThoughtLoop:
    """
    LUNA-ULTRA Thought Loop: Self-reflective debugging and multi-agent collaboration.
    """
    def __init__(self, controller):
        self.controller = controller
        self.max_iterations = 3

    async def run_with_reflection(self, task: str, initial_plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executes a plan and reflects on the results, fixing errors autonomously.
        """
        logging.info(f"ThoughtLoop: Starting reflective execution for task: {task}")
        current_plan = initial_plan
        all_results = []
        
        for i in range(self.max_iterations):
            logging.info(f"ThoughtLoop: Iteration {i+1}/{self.max_iterations}")
            
            # 1. Execution Phase
            iteration_results = []
            success = True
            for step in current_plan:
                agent_name = step.get("agent")
                agent = self.controller.orchestrator.agents.get(agent_name)
                if agent:
                    res = await agent.execute(step.get("action"), step.get("params", {}))
                    iteration_results.append({"step": step, "result": res})
                    if not res.get("success"):
                        success = False
                        break
            
            all_results.append({"iteration": i, "results": iteration_results, "success": success})
            
            if success:
                logging.info("ThoughtLoop: Task completed successfully.")
                # Aggregate outputs for the final response
                final_output = ""
                for res in iteration_results:
                    if "output" in res["result"]:
                        final_output += res["result"]["output"] + "\n\n"
                
                return {
                    "success": True, 
                    "results": all_results, 
                    "output": final_output.strip() or "Task completed successfully."
                }
            
            # 2. Reflection Phase (Self-Debugging)
            error_report = iteration_results[-1].get("result", {}).get("error", "Unknown error")
            logging.warning(f"ThoughtLoop: Error detected: {error_report}. Reflecting...")
            
            reflection_prompt = (
                f"Task: {task}\n"
                f"Previous Plan: {json.dumps(current_plan)}\n"
                f"Error Encountered: {error_report}\n"
                f"Analyze why it failed and provide a corrected plan to fix the issue.\n"
                f"Return ONLY a JSON list of steps: [{{'agent': 'name', 'action': 'method', 'params': {{}} }}]"
            )
            
            new_plan_str = await self.controller.llm_router.generate_response(reflection_prompt)
            try:
                json_match = re.search(r"\[.*\]", new_plan_str, re.DOTALL)
                if json_match:
                    current_plan = json.loads(json_match.group(0))
                else:
                    break
            except Exception as e:
                logging.error(f"ThoughtLoop: Reflection parsing error: {e}")
                break
                
        return {"success": False, "error": "Max iterations reached without success", "results": all_results}

    async def multi_agent_collab(self, complex_task: str) -> str:
        """
        Simulates collaboration between specialized internal agents.
        """
        collab_prompt = (
            f"Complex Task: {complex_task}\n"
            f"Simulate a discussion between three LUNA internal agents:\n"
            f"1. LUNA-Architect (Planning)\n"
            f"2. LUNA-Coder (Implementation)\n"
            f"3. LUNA-Security (Safety & Validation)\n"
            f"Provide their dialogue and the final consensus plan."
        )
        return await self.controller.llm_router.generate_response(collab_prompt)
