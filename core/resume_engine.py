# Path: core/resume_engine.py
import logging
from typing import Dict, Any, Optional


class ResumeEngine:
    """
    Resume Engine for Agent Mode.
    Handles resumption after token limit errors or crashes.
    """
    
    def __init__(self, controller, state_manager):
        self.controller = controller
        self.state_manager = state_manager
        self.max_resume_attempts = 3
        logging.info("ResumeEngine: Initialized.")
    
    async def resume_execution(self) -> Dict[str, Any]:
        """
        Resume execution from saved state.
        
        Handles:
        - Token limit errors
        - Crashes
        - Partial execution
        """
        
        logging.info("ResumeEngine: Attempting to resume execution...")
        
        # Get current state
        state = self.state_manager.get_state()
        
        if not state:
            return {
                "success": False,
                "error": "No execution state found to resume."
            }
        
        # Check if we've exceeded max resume attempts
        resume_count = state.get("resume_count", 0)
        if resume_count >= self.max_resume_attempts:
            return {
                "success": False,
                "error": f"Max resume attempts ({self.max_resume_attempts}) exceeded. Please restart the task."
            }
        
        # Update resume count
        state["resume_count"] = resume_count + 1
        self.state_manager.current_state = state
        self.state_manager._save_state()
        
        logging.info(f"ResumeEngine: Resume attempt {resume_count + 1}/{self.max_resume_attempts}")
        
        # Get plan and current progress
        plan = state.get("plan")
        current_step = state.get("current_step", 0)
        completed_steps = state.get("completed_steps", [])
        remaining_steps = state.get("remaining_steps", [])
        
        # Generate compressed context for LLM
        compressed_context = self._generate_compressed_context(state)
        
        logging.info(f"ResumeEngine: Resuming from step {current_step + 1}. Completed: {len(completed_steps)}, Remaining: {len(remaining_steps)}")
        
        # Continue execution from current step
        try:
            # Import MasterOrchestrator to continue execution
            from core.master_orchestrator import MasterOrchestrator
            
            # Get the master orchestrator instance
            master = MasterOrchestrator(self.controller)
            
            # Execute remaining steps
            remaining_plan = {
                "steps": [plan["steps"][i] for i in remaining_steps],
                "goal": plan.get("goal"),
                "risk_level": plan.get("risk_level"),
                "estimated_complexity": plan.get("estimated_complexity")
            }
            
            execution_result = await master._execute_plan_with_validation(remaining_plan)
            
            if execution_result.get("success"):
                # Mark execution as complete
                self.state_manager.mark_execution_complete(True)
                
                return {
                    "success": True,
                    "message": "Execution resumed and completed successfully.",
                    "resumed_from_step": current_step,
                    "results": execution_result.get("results", [])
                }
            else:
                # Execution failed, save state for potential retry
                self.state_manager.add_error(execution_result.get("error", "Unknown error during resume"))
                
                return {
                    "success": False,
                    "error": f"Resumed execution failed: {execution_result.get('error')}",
                    "can_retry": resume_count + 1 < self.max_resume_attempts
                }
                
        except Exception as e:
            logging.error(f"ResumeEngine: Error during resume: {e}")
            self.state_manager.add_error(str(e))
            
            return {
                "success": False,
                "error": f"Resume failed with exception: {str(e)}",
                "can_retry": resume_count + 1 < self.max_resume_attempts
            }
    
    def _generate_compressed_context(self, state: Dict[str, Any]) -> str:
        """
        Generate compressed context summary for LLM to avoid token limits.
        """
        context = []
        
        context.append("=== EXECUTION CONTEXT (RESUMED) ===")
        context.append(f"Goal: {state.get('goal', 'N/A')}")
        context.append(f"Status: {state.get('status', 'N/A')}")
        context.append(f"Current Step: {state.get('current_step', 0) + 1}")
        context.append(f"Completed Steps: {len(state.get('completed_steps', []))}")
        context.append(f"Remaining Steps: {len(state.get('remaining_steps', []))}")
        
        # Summarize completed steps
        context.append("\nCompleted Steps Summary:")
        for result in state.get("results", [])[-5:]:  # Last 5 results
            step_idx = result.get("step_index", "?")
            success = result.get("success", False)
            context.append(f"  Step {step_idx + 1}: {'✓' if success else '✗'}")
        
        # List remaining steps
        context.append("\nRemaining Steps:")
        plan = state.get("plan", {})
        for step_idx in state.get("remaining_steps", []):
            if step_idx < len(plan.get("steps", [])):
                step = plan["steps"][step_idx]
                context.append(f"  {step_idx + 1}. {step.get('description', 'N/A')}")
        
        # Include recent errors
        if state.get("errors"):
            context.append("\nRecent Errors:")
            for error in state.get("errors", [])[-3:]:  # Last 3 errors
                context.append(f"  - {error.get('error', 'N/A')}")
        
        context.append("=== END CONTEXT ===")
        
        return "\n".join(context)
    
    def detect_token_limit_error(self, error_message: str) -> bool:
        """
        Detect if an error is related to token limits.
        """
        token_error_keywords = [
            "context_length_exceeded",
            "token_limit",
            "maximum context length",
            "too many tokens",
            "context window"
        ]
        
        error_lower = error_message.lower()
        
        for keyword in token_error_keywords:
            if keyword in error_lower:
                return True
        
        return False
    
    async def handle_token_limit_error(self, error_message: str) -> Dict[str, Any]:
        """
        Handle token limit errors by saving state and preparing for resume.
        """
        logging.warning(f"ResumeEngine: Token limit error detected: {error_message}")
        
        # Save current state
        if self.state_manager.current_state:
            self.state_manager.add_error(f"Token limit error: {error_message}")
            self.state_manager._save_state()
            
            return {
                "success": False,
                "error": "Token limit exceeded. State saved. Please resume execution.",
                "can_resume": True,
                "state_saved": True
            }
        
        return {
            "success": False,
            "error": "Token limit exceeded but no state to save.",
            "can_resume": False
        }
    
    def clear_resume_state(self):
        """
        Clear resume state after successful completion.
        """
        self.state_manager.clear_state()
        logging.info("ResumeEngine: Resume state cleared.")
