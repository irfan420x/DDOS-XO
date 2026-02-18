# Path: app/main.py
import asyncio
import sys
import os
import logging
from app.bootstrap import LunaBootstrap
from app.lifecycle import LifecycleManager


# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/system.log"),
        logging.StreamHandler()
    ]
)

async def main():
    """
    Main entry point for LUNA-ULTRA.
    """
    logging.info("LUNA-ULTRA: Starting system...")
    
    # 1. Initialize Bootstrap
    bootstrap = LunaBootstrap("config/config.yaml")
    
    # 2. Initialize System
    controller = await bootstrap.initialize_system()
    
    # 3. Display Startup Banner (Console)
    from app.startup_banner import StartupBanner
    StartupBanner.display(controller.config)
    
    # 4. Initialize Lifecycle Manager
    lifecycle = LifecycleManager(controller)
    
    # 5. Run in CLI mode if --cli argument is provided
    if "--cli" in sys.argv:
        logging.info("LUNA-ULTRA: Running in CLI mode.")
        print("LUNA-ULTRA CLI Mode. Type 'exit' to quit.")
        while True:
            try:
                user_input = await asyncio.to_thread(input, "You: ")
                if user_input.lower() == 'exit':
                    break
                response = await controller.process_input(user_input)
                print(f"LUNA: {response}")
            except KeyboardInterrupt:
                break
            except Exception as e:
                logging.error(f"LUNA-ULTRA CLI Error: {str(e)}")
                print(f"LUNA: An error occurred: {str(e)}")
        await lifecycle.shutdown()
    else:
        # 5. Initialize GUI (Tkinter)
        # Note: In some environments, GUI might need to run in the main thread
        from gui.main_window import LunaGUI # Import here to avoid error if not running GUI
        logging.info("LUNA-ULTRA: Launching GUI...")
        gui = LunaGUI(controller)
        
        # 6. Run GUI
        try:
            gui.run()
        except KeyboardInterrupt:
            logging.info("LUNA-ULTRA: Shutdown signal received.")
            await lifecycle.shutdown()
        except Exception as e:
            logging.error(f"LUNA-ULTRA: Fatal error: {str(e)}")
            await lifecycle.shutdown()
            sys.exit(1)

if __name__ == "__main__":
    # Ensure directories exist for logging
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("LUNA-ULTRA: CLI mode terminated by user.")
    except Exception as e:
        logging.error(f"LUNA-ULTRA: Unhandled exception in main: {e}")
        sys.exit(1)
