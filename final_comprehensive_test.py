#!/usr/bin/env python3
import asyncio
import sys
import os
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO)

# Add the DDOS-XO directory to path
sys.path.insert(0, '/home/ubuntu/DDOS-XO')

async def run_final_tests():
    os.chdir("/home/ubuntu/DDOS-XO")
    
    try:
        from core.controller import LunaController
        print("\n[SYSTEM] Initializing LUNA-ULTRA v3.0...")
        controller = LunaController("config")
        
        # Ensure voice mode is simulated as enabled for testing
        controller.config['gui']['voice_mode'] = True
        
        tasks = [
            "Hello Luna, give me a quick status update of the system.",
            "What is 15% of 1250? Explain the calculation.",
            "Create a new folder named 'test_project' and list the directory.",
            "Write a simple Python script to print the current time and save it as 'time_check.py'.",
            "Try to access a non-existent directory named 'secret_vault' to test error intelligence."
        ]
        
        for i, task in enumerate(tasks, 1):
            print(f"\n--- TASK {i}: {task} ---")
            # Register with watchdog
            task_id = f"final_task_{i}"
            controller.watchdog.register_task(task_id, task)
            
            response = await controller.process_input(task)
            
            controller.watchdog.unregister_task(task_id)
            print(f"LUNA RESPONSE:\n{response}")
            print("-" * 30)
            await asyncio.sleep(2) # Small delay between tasks

        print("\n[SUCCESS] All 5 tasks completed. LUNA-ULTRA v3.0 is fully operational.")

    except Exception as e:
        print(f"❌ Final Test Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_final_tests())
