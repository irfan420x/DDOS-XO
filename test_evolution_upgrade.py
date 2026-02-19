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

async def test_voice_first_evolution():
    os.chdir("/home/ubuntu/DDOS-XO")
    
    try:
        from core.controller import LunaController
        print("\n[1/4] Initializing LunaController (Startup Notification & Watchdog)...")
        controller = LunaController("config")
        
        # Enable voice mode for testing
        controller.config['gui']['voice_mode'] = True
        if hasattr(controller, 'gui') and controller.gui:
            controller.gui.voice_engine.enabled = True
            
        print("\n[2/4] Testing Human-like Voice Response (Chat)...")
        response = await controller.process_input("Hello Luna, how are you today?")
        print(f"LUNA: {response}")
        
        print("\n[3/4] Testing Structured Transparency (System Action)...")
        # This should trigger GUI activity updates and voice announcements
        response = await controller.process_input("List the files in the current directory")
        print(f"LUNA: {response}")
        
        print("\n[4/4] Testing Error Intelligence (Failed Task)...")
        # Try an action that might fail or be unsupported to see root cause analysis
        response = await controller.process_input("Delete the system root directory")
        print(f"LUNA: {response}")
        
        print("\n[SUCCESS] Evolution Upgrade Test Completed.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_voice_first_evolution())
