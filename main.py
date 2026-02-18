# Path: main.py

import asyncio
import sys
from core.engine import JarvisEngine
from loguru import logger

async def main():
    engine = JarvisEngine()
    
    try:
        await engine.start()
        
        print("\n--- JARVIS-CORE v2.0.0-PRO ---")
        print("Type 'exit' to shutdown.")
        
        while engine.running:
            try:
                user_input = await asyncio.get_event_loop().run_in_executor(None, input, "JARVIS > ")
                
                if user_input.lower() in ['exit', 'quit', 'shutdown']:
                    await engine.stop()
                    break
                
                if not user_input.strip():
                    continue
                    
                response = await engine.process_query(user_input)
                print(f"\nAssistant: {response}\n")
                
            except EOFError:
                break
                
    except KeyboardInterrupt:
        logger.info("Interrupt received, stopping...")
    finally:
        await engine.stop()

if __name__ == "__main__":
    asyncio.run(main())
