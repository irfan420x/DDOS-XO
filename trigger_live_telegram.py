#!/usr/bin/env python3
import asyncio
import sys
import os
import logging

# Setup logging to see what's happening
logging.basicConfig(level=logging.INFO)

# Add the DDOS-XO directory to path
sys.path.insert(0, '/home/ubuntu/DDOS-XO')

async def main():
    os.chdir("/home/ubuntu/DDOS-XO")
    
    try:
        from core.controller import LunaController
        print("[INFO] Initializing LunaController with your real Telegram Token...")
        
        # This will trigger the send_startup_notification() in LunaController.__init__
        controller = LunaController("config")
        
        print("[INFO] Waiting for Telegram notification to be sent...")
        # Give it enough time to complete the async task
        await asyncio.sleep(10)
        
        print("[SUCCESS] Startup notification task should have completed. Please check your Telegram.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
