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
    
    # Start background services (Telegram, etc.)
    await controller.start_services()
    
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
        await controller.shutdown_services()
        await lifecycle.shutdown()
    else:
        # Launch GUI
        from PyQt6.QtWidgets import QApplication
        from gui.main_window import LunaGUI
        
        app = QApplication(sys.argv)
        logging.info("LUNA-ULTRA: Launching GUI...")
        gui = LunaGUI(controller)
        gui.show()
        
        # Run GUI event loop
        try:
            sys.exit(app.exec())
        except KeyboardInterrupt:
            logging.info("LUNA-ULTRA: Shutdown signal received.")
            await controller.shutdown_services()
            await lifecycle.shutdown()
        except Exception as e:
            logging.error(f"LUNA-ULTRA: Fatal error: {str(e)}")
            await controller.shutdown_services()
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
