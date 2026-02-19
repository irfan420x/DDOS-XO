#!/usr/bin/env python3
"""
Comprehensive test script for LUNA-ULTRA
Tests various intents: CONVERSATION, CODING, and SYSTEM_ACTION
"""

import asyncio
import sys
import os

# Add the DDOS-XO directory to path
sys.path.insert(0, '/home/ubuntu/DDOS-XO')

async def run_test(controller, task_name, user_input):
    print("="*60)
    print(f"TEST: {task_name}")
    print("="*60)
    print(f"User: {user_input}")
    try:
        response = await controller.process_input(user_input)
        print(f"LUNA: {response}\n")
        return response
    except Exception as e:
        print(f"❌ ERROR in {task_name}: {str(e)}\n")
        return None

async def main():
    # Ensure logs directory exists
    if not os.path.exists("/home/ubuntu/DDOS-XO/logs"):
        os.makedirs("/home/ubuntu/DDOS-XO/logs")
    
    # Change to DDOS-XO directory
    os.chdir("/home/ubuntu/DDOS-XO")
    
    try:
        from core.controller import LunaController
        print("[INFO] Initializing LunaController...")
        controller = LunaController("config")
        print("[SUCCESS] Controller initialized\n")
        
        # 1. Complex Math (Should be CONVERSATION now)
        await run_test(controller, "Complex Math", "What is the factorial of 5 divided by 2?")
        
        # 2. Coding Request (Should be CODING intent)
        await run_test(controller, "Coding Request", "Write a simple Python function to check if a number is prime.")
        
        # 3. System Information (Should be SYSTEM_ACTION or CONVERSATION)
        await run_test(controller, "System Info", "What is the current working directory?")
        
        # 4. Logical Reasoning
        await run_test(controller, "Logical Reasoning", "If I have 3 apples and you give me 5 more, but I eat 2, how many do I have left?")

    except Exception as e:
        print(f"❌ Initialization Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
