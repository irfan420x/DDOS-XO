# Path: agents/skill_acquisition.py
import os
import logging
import json
import requests
from typing import Dict, Any, List, Optional

class SkillAcquisition:
    """
    LUNA-ULTRA Skill Acquisition: Autonomous tool finding and plugin system.
    """
    def __init__(self, controller):
        self.controller = controller
        self.skills_dir = "skills"
        if not os.path.exists(self.skills_dir):
            os.makedirs(self.skills_dir)

    async def acquire_skill(self, task: str) -> Dict[str, Any]:
        """
        Finds and installs a new skill (Python script) to handle a specific task.
        """
        logging.info(f"SkillAcquisition: Searching for skill to handle: {task}")
        
        # 1. Search for a solution/library
        search_query = f"Python script to {task} standalone"
        search_results = await self.controller.browser.search(search_query)
        
        if not search_results:
            return {"success": False, "error": "No relevant skill found online."}
            
        # 2. Generate a custom skill script based on search results
        skill_prompt = (
            f"Task: {task}\n"
            f"Search Context: {json.dumps(search_results)}\n"
            f"Write a standalone Python script named 'skill_{task.replace(' ', '_')}.py' to perform this task.\n"
            f"The script must have a main() function that takes params as a dictionary.\n"
            f"Return ONLY the Python code."
        )
        
        skill_code = await self.controller.llm_router.generate_response(skill_prompt)
        
        # 3. Save and Install Skill
        skill_name = f"skill_{task.replace(' ', '_')}.py"
        skill_path = os.path.join(self.skills_dir, skill_name)
        
        try:
            with open(skill_path, 'w') as f:
                f.write(skill_code)
            logging.info(f"SkillAcquisition: Successfully acquired and saved skill: {skill_name}")
            return {"success": True, "skill_path": skill_path, "skill_name": skill_name}
        except Exception as e:
            logging.error(f"SkillAcquisition: Failed to save skill: {e}")
            return {"success": False, "error": str(e)}

    def list_skills(self) -> List[str]:
        """
        Lists all currently acquired skills.
        """
        return [f for f in os.listdir(self.skills_dir) if f.endswith(".py")]
