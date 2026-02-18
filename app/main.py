# Path: app/main.py
import asyncio
import sys
import os
from app.bootstrap import LunaBootstrap
from app.lifecycle import LifecycleManager
from gui.main_window import LunaGUI

async def main():
    """
    Main entry point for LUNA-ULTRA.
    """
    # 1. Initialize Bootstrap
    bootstrap = LunaBootstrap("config/config.yaml")
    
    # 2. Initialize System
    controller = await bootstrap.initialize_system()
    
    # 3. Display Startup Banner
    from app.startup_banner import StartupBanner
    StartupBanner.display(controller.config)
    
    # 4. Initialize Lifecycle Manager
    lifecycle = LifecycleManager(controller)
    
    # 5. Initialize GUI
    gui = LunaGUI(controller)
    
    # 6. Run GUI
    try:
        gui.run()
    except KeyboardInterrupt:
        await lifecycle.shutdown()
    except Exception as e:
        print(f"LUNA-ULTRA: Fatal error: {str(e)}")
        await lifecycle.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
