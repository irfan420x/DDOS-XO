# Path: core/master_orchestrator.py
import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

from core.plan_engine import PlanEngine
from core.execution_state import ExecutionStateManager
from core.validation_engine import ValidationEngine
from core.resume_engine import ResumeEngine
from core.github_safe_flow import GitHubSafeFlow
from tools.registry import ToolRegistry


class MasterOrchestrator:
    """
    Master Orchestrator for Agent Mode.
    Coordinates structured planning, execution, validation, and resumption.
    Similar to Manus AI's agent loop architecture.
    """
    
    def __init__(self, controller):
        self.controller = controller
        self.plan_engine = PlanEngine(controller)
        self.state_manager = ExecutionStateManager()
        self.validation_engine = ValidationEngine(controller)
        self.resume_engine = ResumeEngine(controller, self.state_manager)
        self.github_flow = GitHubSafeFlow(controller)
        
        self.current_mode = "chat"  # chat, automation, agent
        self.agent_mode_active = False
        
        logging.info("MasterOrchestrator: Initialized for Agent Mode.")
    
    def set_mode(self, mode: str):
        """
        Set the current operating mode.
        Modes: chat, automation, agent
        """
        if mode not in ["chat", "automation", "agent"]:
            logging.warning(f"MasterOrchestrator: Invalid mode '{mode}'. Defaulting to 'chat'.")
            mode = "chat"
        
        self.current_mode = mode
        self.agent_mode_active = (mode == "agent")
        logging.info(f"MasterOrchestrator: Mode set to '{mode}'.")
    
    async def handle_agent_task(self, goal: str, user_approved: bool = False) -> Dict[str, Any]:
        """
        Main entry point for Agent Mode tasks.
        
        Workflow:
        1. Generate structured plan
        2. Require user approval
        3. Execute step-by-step
        4. Validate after each step
        5. Persist state
        6. Resume on failure
        7. Commit changes
        8. Ask confirmation before push
        """
        
        if not self.agent_mode_active:
            return {
                "success": False,
                "error": "Agent Mode is not active. Please switch to Agent Mode first."
            }
        
        # Check if we're resuming from a previous state
        if self.state_manager.has_active_execution():
            logging.info("MasterOrchestrator: Resuming previous execution...")
            return await self.resume_engine.resume_execution()
        
        # Step 1: Generate Plan
        logging.info(f"MasterOrchestrator: Generating plan for goal: {goal}")
        plan_result = await self.plan_engine.generate_plan(goal)
        
        if not plan_result.get("success"):
            return {
                "success": False,
                "error": f"Plan generation failed: {plan_result.get('error')}",
                "plan": None
            }
        
        plan = plan_result.get("plan")
        
        # Step 2: Require User Approval (if not already approved)
        if not user_approved:
            return {
                "success": True,
                "requires_approval": True,
                "plan": plan,
                "message": "Plan generated. Please review and approve before execution."
            }
        
        # Step 3: Initialize Execution State
        self.state_manager.initialize_execution(goal, plan)
        
        # Step 4: Execute Plan Step-by-Step
        execution_result = await self._execute_plan_with_validation(plan)
        
        # Step 5: Final Validation
        if execution_result.get("success"):
            validation_result = await self.validation_engine.validate_project()
            
            if not validation_result.get("success"):
                logging.warning("MasterOrchestrator: Final validation failed. Entering patch loop...")
                # Attempt to fix issues
                patch_result = await self._patch_validation_errors(validation_result)
                execution_result["validation"] = patch_result
            else:
                execution_result["validation"] = validation_result
        
        # Step 6: Mark execution complete
        self.state_manager.mark_execution_complete(execution_result.get("success", False))
        
        # Step 7: Prepare for GitHub push (if successful)
        if execution_result.get("success"):
            git_prep_result = self.github_flow.prepare_for_push(execution_result)
            execution_result["git_preparation"] = git_prep_result
        
        return execution_result
    
    async def _execute_plan_with_validation(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute plan steps with validation and retry logic.
        Respects permission engine for security.
        """
        steps = plan.get("steps", [])
        results = []
        
        for idx, step in enumerate(steps):
            logging.info(f"MasterOrchestrator: Executing step {idx + 1}/{len(steps)}: {step.get('description', 'N/A')}")
            
            # Check permissions before execution
            if not self._check_step_permissions(step):
                logging.error(f"MasterOrchestrator: Step {idx + 1} denied by permission engine.")
                return {
                    "success": False,
                    "error": f"Step {idx + 1} denied: Insufficient permissions.",
                    "completed_steps": idx,
                    "total_steps": len(steps),
                    "results": results
                }
            
            # Update state before execution
            self.state_manager.update_current_step(idx)
            
            # Execute step with retry logic
            step_result = await self._execute_step_with_retry(step, max_retries=3)
            
            results.append(step_result)
            
            # Mark step as complete
            self.state_manager.mark_step_complete(idx, step_result.get("success", False))
            
            # If step failed after retries, stop execution
            if not step_result.get("success"):
                logging.error(f"MasterOrchestrator: Step {idx + 1} failed after retries. Stopping execution.")
                return {
                    "success": False,
                    "error": f"Step {idx + 1} failed: {step_result.get('error')}",
                    "completed_steps": idx,
                    "total_steps": len(steps),
                    "results": results
                }
        
        return {
            "success": True,
            "completed_steps": len(steps),
            "total_steps": len(steps),
            "results": results
        }
    
    def _check_step_permissions(self, step: Dict[str, Any]) -> bool:
        """
        Check if step is allowed by permission engine.
        """
        action = step.get("action", "")
        params = step.get("params", {})
        
        # Map actions to permission types
        permission_map = {
            "read_file": "read_file",
            "write_file": "write_file",
            "execute_shell": "shell_exec",
            "system_control": "system_control"
        }
        
        # Determine permission type
        permission_type = permission_map.get(action, "shell_exec")
        
        # Check with permission engine
        details = f"Agent Mode: {action} with params {params}"
        return self.controller.permission_engine.check_permission(permission_type, details)
    
    async def _execute_step_with_retry(self, step: Dict[str, Any], max_retries: int = 3) -> Dict[str, Any]:
        """
        Execute a single step with retry logic and error detection.
        """
        retry_count = 0
        last_error = None
        
        while retry_count <= max_retries:
            try:
                # Execute step via orchestrator or tool registry
                result = await self._execute_single_step(step)
                
                # Validate step execution
                if result.get("success"):
                    # Compile and check for runtime errors
                    compile_result = await self.validation_engine.compile_project()
                    
                    if compile_result.get("success"):
                        return result
                    else:
                        # Compilation failed, enter patch loop
                        logging.warning(f"MasterOrchestrator: Compilation failed after step execution. Retry {retry_count + 1}/{max_retries}")
                        last_error = compile_result.get("error")
                        retry_count += 1
                        
                        # Attempt to fix compilation errors
                        if retry_count <= max_retries:
                            await self._attempt_patch(compile_result)
                else:
                    last_error = result.get("error")
                    retry_count += 1
                    
            except Exception as e:
                logging.error(f"MasterOrchestrator: Exception during step execution: {e}")
                last_error = str(e)
                retry_count += 1
        
        return {
            "success": False,
            "error": f"Step failed after {max_retries} retries. Last error: {last_error}",
            "retry_count": retry_count
        }
    
    async def _execute_single_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single step using the appropriate agent or tool.
        """
        agent_name = step.get("agent")
        action = step.get("action")
        params = step.get("params", {})
        
        # Get agent from orchestrator
        agent = self.controller.orchestrator.agents.get(agent_name)
        
        if agent:
            # Execute via agent
            result = await agent.execute(action, params)
            return result
        else:
            # Try to execute via ToolRegistry
            tool_result = ToolRegistry.execute_tool(
                action, 
                params, 
                current_permission=self.controller.permission_engine.current_level.name
            )
            return tool_result
    
    async def _attempt_patch(self, error_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempt to automatically patch compilation or runtime errors.
        """
        error_msg = error_result.get("error", "")
        
        # Use LLM to generate patch
        patch_prompt = f"""
        The following error occurred during execution:
        {error_msg}
        
        Please provide a fix for this error. Return only the corrected code or fix instructions.
        """
        
        try:
            patch_response = await self.controller.llm_router.generate_response(patch_prompt)
            logging.info(f"MasterOrchestrator: Generated patch: {patch_response[:100]}...")
            
            # Apply patch (this would need more sophisticated logic)
            return {"success": True, "patch": patch_response}
        except Exception as e:
            logging.error(f"MasterOrchestrator: Patch generation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _patch_validation_errors(self, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempt to patch validation errors.
        """
        errors = validation_result.get("errors", [])
        
        for error in errors:
            patch_result = await self._attempt_patch({"error": error})
            if not patch_result.get("success"):
                return {
                    "success": False,
                    "error": f"Failed to patch validation error: {error}"
                }
        
        # Re-validate after patching
        return await self.validation_engine.validate_project()
    
    def get_current_state(self) -> Dict[str, Any]:
        """
        Get current execution state for display in GUI.
        """
        return self.state_manager.get_state()
    
    def clear_state(self):
        """
        Clear current execution state.
        """
        self.state_manager.clear_state()
        logging.info("MasterOrchestrator: Execution state cleared.")
    
    async def push_to_github(self, branch_name: str) -> Dict[str, Any]:
        """
        Push changes to GitHub after user confirmation.
        Should only be called after user explicitly confirms.
        """
        logging.info(f"MasterOrchestrator: Pushing branch '{branch_name}' to GitHub...")
        
        result = self.github_flow.push_branch(branch_name)
        
        if result.get("success"):
            logging.info(f"MasterOrchestrator: Successfully pushed branch '{branch_name}'.")
        else:
            logging.error(f"MasterOrchestrator: Failed to push branch: {result.get('error')}")
        
        return result
