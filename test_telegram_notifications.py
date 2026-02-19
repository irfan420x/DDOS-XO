#!/usr/bin/env python3
import asyncio
import sys
import os

# Add the DDOS-XO directory to path
sys.path.insert(0, '/home/ubuntu/DDOS-XO')

async def main():
    os.chdir("/home/ubuntu/DDOS-XO")
    
    try:
        from core.controller import LunaController
        print("[INFO] Initializing LunaController (this should trigger a startup notification)...")
        controller = LunaController("config")
        
        # Wait a bit for the startup notification task to run
        await asyncio.sleep(5)
        
        print("\n[INFO] Testing Power Action (Shutdown)...")
        # Simulate a shutdown command
        response = await controller.process_input("Shutdown the system")
        print(f"LUNA Response: {response}")
        
        # Wait for the notification task
        await asyncio.sleep(3)
        
        print("\n[INFO] Testing Power Action (Restart)...")
        # Simulate a restart command
        response = await controller.process_input("Restart the laptop")
        print(f"LUNA Response: {response}")
        
        await asyncio.sleep(3)
        print("\n[SUCCESS] Test completed. Please check your Telegram for notifications.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
