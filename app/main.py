# Path: app/main.py
import asyncio
import sys
import os
from app.bootstrap import LunaBootstrap, LifecycleManager
from gui.main_window import LunaGUI

async def main():
    """
    Main entry point for LUNA-ULTRA.
    """
    # 1. Initialize Bootstrap
    bootstrap = LunaBootstrap("config/config.yaml")
    
    # 2. Initialize System
    controller = bootstrap.initialize_system()
    
    # 3. Display Startup Banner
    bootstrap.display_startup_banner()
    
    # 4. Initialize Lifecycle Manager
    lifecycle = LifecycleManager(controller)
    
    # 5. Initialize GUI
    # Note: In a real app, the GUI would run in the main thread
    # and the controller would run in an async loop.
    # For this implementation, we'll simulate the GUI startup.
    gui = LunaGUI(controller)
    
    # 6. Run GUI (This is a blocking call)
    try:
        gui.run()
    except KeyboardInterrupt:
        lifecycle.shutdown()
    except Exception as e:
        print(f"LUNA-ULTRA: Fatal error: {str(e)}")
        lifecycle.shutdown()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
