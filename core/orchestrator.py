# Path: core/orchestrator.py
import logging
import json
import re
from typing import Dict, Any, List

class Orchestrator:
    """
    LUNA-ULTRA Orchestrator: Multi-agent coordination with deep intent analysis.
    """
    def __init__(self, controller):
        self.controller = controller
        self.agents = {}
        self.initialize_agents()

    def initialize_agents(self):
        from agents.code_agent import CodeAgent
        from agents.automation_agent import AutomationAgent
        from agents.screen_agent import ScreenAgent
        from agents.system_agent import SystemAgent
        from agents.dynamic_agent import DynamicAgent
        from agents.architect_agent import ArchitectAgent

        self.agents["code"] = CodeAgent(self.controller.config, self.controller.llm_router)
        self.agents["automation"] = AutomationAgent(self.controller.config, self.controller.permission_engine)
        self.agents["screen"] = ScreenAgent(self.controller.config, self.controller.permission_engine)
        self.agents["system"] = SystemAgent(self.controller.config)
        self.agents["dynamic"] = DynamicAgent(self.controller.config, self.controller.llm_router, self.controller.permission_engine)
        self.agents["architect"] = ArchitectAgent(self.controller.config, self.controller.llm_router)
        
        logging.info(f"Orchestrator: Initialized {len(self.agents)} agents.")

    async def handle_task(self, user_input: str) -> Dict[str, Any]:
        logging.info(f"Orchestrator: Analyzing task: {user_input}")
        
        # 0. Get Memory Context
        memory_context = self.controller.memory_manager.get_context(user_input)

        # 1. Intent Classification
        intent_prompt = (
            f"Context:\n{memory_context}\n\n"
            f"Classify the user intent for: \"{user_input}\"\n"
            f"Categories: GREETING, CONVERSATION, CODING, SYSTEM_ACTION, WEB_ACTION, AUTOMATION, ANALYSIS.\n"
            f"Respond in format: INTENT: <CATEGORY> | THOUGHT: <REASONING>"
        )
        reasoning_response = await self.controller.llm_router.generate_response(intent_prompt)
        
        intent = "CONVERSATION"
        thought = "Direct response."
        if "INTENT:" in reasoning_response:
            parts = reasoning_response.split("|")
            intent = parts[0].replace("INTENT:", "").strip().upper()
            if len(parts) > 1:
                thought = parts[1].replace("THOUGHT:", "").strip()

        # Update GUI/Telegram with Thought
        if hasattr(self.controller, 'gui') and self.controller.gui:
            self.controller.gui.update_activity(f"🧠 THOUGHT: {thought}")

        # 2. Routing Logic
        action_intents = ["CODING", "SYSTEM_ACTION", "WEB_ACTION", "AUTOMATION", "ANALYSIS"]
        if intent not in action_intents:
            chat_prompt = f"Context:\n{memory_context}\n\nUser: {user_input}"
            chat_response = await self.controller.llm_router.generate_response(chat_prompt)
            return {"response": chat_response, "type": "chat", "thought": thought}

        # 3. Tool Planning
        plan_prompt = (
            f"User Task: {user_input}\n"
            f"Thought: {thought}\n"
            f"Available Agents: {list(self.agents.keys())}.\n"
            f"Generate a JSON list of steps: [{{'agent': 'name', 'action': 'method', 'params': {{}} }}]\n"
            f"Return ONLY the JSON list."
        )
        plan_str = await self.controller.llm_router.generate_response(plan_prompt)
        
        plan = []
        try:
            json_match = re.search(r"\[.*\]", plan_str, re.DOTALL)
            if json_match:
                plan = json.loads(json_match.group(0))
        except Exception as e:
            logging.error(f"Orchestrator: Plan error: {e}")

        # 4. Execution (with Self-Reflective Thought Loop)
        if plan:
            # Use ThoughtLoop for complex tasks or if multiple steps are involved
            if len(plan) > 1 or intent in ["CODING", "AUTOMATION"]:
                self.controller.gui.update_activity("🧠 LUNA: Entering Thought Loop for self-reflection...")
                loop_result = await self.controller.thought_loop.run_with_reflection(user_input, plan)
                return {"plan": plan, "results": loop_result.get("results"), "type": "tool_action", "thought": thought, "success": loop_result.get("success")}
            
            # Simple execution for single steps
            results = []
            for step in plan:
                agent = self.agents.get(step.get("agent"))
                if agent:
                    res = await agent.execute(step.get("action"), step.get("params", {}))
                    results.append({"step": step, "result": res})
                    if not res.get("success"): break
            return {"plan": plan, "results": results, "type": "tool_action", "thought": thought}
        
        return {"response": "I understood your request but couldn't form a plan.", "type": "chat"}
