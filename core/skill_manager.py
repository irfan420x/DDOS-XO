# Path: core/skill_manager.py
import os
import logging
import importlib.util
from typing import Dict, Any, List

class SkillManager:
    """
    LUNA-ULTRA Skill Manager: Handles the storage and loading of self-written tools (skills).
    """
    def __init__(self):
        self.skills_dir = "skills"
        if not os.path.exists(self.skills_dir):
            os.makedirs(self.skills_dir)
        self.skills = {}
        self.load_skills()

    def load_skills(self):
        """Dynamically loads all skills from the skills directory."""
        for filename in os.listdir(self.skills_dir):
            if filename.endswith(".py"):
                skill_name = filename[:-3]
                file_path = os.path.join(self.skills_dir, filename)
                try:
                    spec = importlib.util.spec_from_file_location(skill_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.skills[skill_name] = module
                    logging.info(f"SkillManager: Loaded skill '{skill_name}'.")
                except Exception as e:
                    logging.error(f"SkillManager: Failed to load skill '{skill_name}': {e}")

    def add_skill(self, name: str, code: str) -> bool:
        """Saves a new skill code to a file and loads it."""
        file_path = os.path.join(self.skills_dir, f"{name}.py")
        try:
            with open(file_path, "w") as f:
                f.write(code)
            # Reload to include the new skill
            self.load_skills()
            return True
        except Exception as e:
            logging.error(f"SkillManager: Failed to add skill '{name}': {e}")
            return False

    def get_skill_list(self) -> List[str]:
        return list(self.skills.keys())
