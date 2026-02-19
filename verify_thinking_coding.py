#!/usr/bin/env python3
import asyncio
import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Add the DDOS-XO directory to path
sys.path.insert(0, '/home/ubuntu/DDOS-XO')

async def run_integrated_test():
    os.chdir("/home/ubuntu/DDOS-XO")
    
    try:
        from core.controller import LunaController
        print("\n[SYSTEM] Initializing LUNA-ULTRA for Integrated Thinking & Coding...")
        controller = LunaController("config")
        
        # The Integrated Task
        task = "সিস্টেমের মেমোরি অ্যানালাইজ করার জন্য একটি পাইথন স্ক্রিপ্ট 'memory_monitor.py' তৈরি করো। যদি মেমোরি ব্যবহার ৮০% এর বেশি হয় তবে এটি টপ ৩টি প্রসেস দেখাবে। কোডটি লেখার আগে তোমার চিন্তাভাবনা এবং কাজের ধাপগুলো বাংলায় বুঝিয়ে বলো।"
        
        print(f"\n--- INTEGRATED TASK: {task} ---")
        
        # Register with watchdog
        task_id = "thinking_coding_verify"
        controller.watchdog.register_task(task_id, task)
        
        response = await controller.process_input(task)
        
        controller.watchdog.unregister_task(task_id)
        
        print(f"\nLUNA RESPONSE:\n{response}")
        
        # Verify if file exists
        if os.path.exists("memory_monitor.py"):
            print("\n[VERIFICATION] 'memory_monitor.py' was successfully created.")
            with open("memory_monitor.py", "r") as f:
                print("--- CODE PREVIEW ---")
                print(f.read()[:500] + "...")
        else:
            print("\n[VERIFICATION] 'memory_monitor.py' was NOT found.")

    except Exception as e:
        print(f"❌ Integrated Test Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_integrated_test())
