#!/usr/bin/env python3
import asyncio
import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Add the DDOS-XO directory to path
sys.path.insert(0, '/home/ubuntu/DDOS-XO')

async def run_coding_test():
    os.chdir("/home/ubuntu/DDOS-XO")
    
    try:
        from core.controller import LunaController
        print("\n[SYSTEM] Initializing LUNA-ULTRA for Coding Task...")
        controller = LunaController("config")
        
        # The Coding Task
        task = "Write a Python script named 'task_manager.py' that allows users to add, view, and delete tasks. The tasks should be saved in a file named 'tasks.txt'. After writing, run the script to add one test task named 'Complete Manus Upgrade'."
        
        print(f"\n--- CODING TASK: {task} ---")
        
        # Register with watchdog
        task_id = "coding_verify_task"
        controller.watchdog.register_task(task_id, task)
        
        response = await controller.process_input(task)
        
        controller.watchdog.unregister_task(task_id)
        
        print(f"\nLUNA RESPONSE:\n{response}")
        
        # Verify if file exists
        if os.path.exists("task_manager.py"):
            print("\n[VERIFICATION] 'task_manager.py' was successfully created.")
            with open("task_manager.py", "r") as f:
                print("--- CODE PREVIEW ---")
                print(f.read()[:500] + "...")
        else:
            print("\n[VERIFICATION] 'task_manager.py' was NOT found.")

    except Exception as e:
        print(f"❌ Coding Test Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_coding_test())
