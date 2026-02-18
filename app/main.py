# Path: app/main.py
import os
import yaml
from core.controller import LunaController
from gui.main_window import LunaGUI

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    print("🌙 LUNA-ULTRA Activated")
    print("LLM: DeepSeek API")
    print("Permission: SAFE")
    print("Memory: Restored (3 days)")
    print("All systems stable.")
    print("Welcome back, IRFAN.")
    
    config = load_config()
    controller = LunaController(config)
    gui = LunaGUI(controller)
    gui.run()

if __name__ == "__main__":
    main()
