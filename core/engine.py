# Path: core/engine.py

import asyncio
import sys
from loguru import logger
from .config_manager import ConfigManager
from security.permission_engine import PermissionEngine
from llm.router import LLMRouter

class JarvisEngine:
    def __init__(self):
        self.config = ConfigManager()
        self.security = PermissionEngine(self.config)
        self.llm = LLMRouter(self.config)
        self.running = False
        self._setup_logging()

    def _setup_logging(self):
        log_level = self.config.get("system.log_level", "INFO")
        logger.remove()
        logger.add(sys.stderr, level=log_level)
        logger.add("logs/jarvis_core.log", rotation="10MB", level="DEBUG")
        logger.success("JARVIS-CORE Engine Logging Initialized")

    async def start(self):
        logger.info("Initializing JARVIS-CORE v2.0.0-PRO...")
        self.running = True
        
        # Start background tasks
        asyncio.create_task(self._heartbeat())
        
        logger.success("Engine is now online.")

    async def stop(self):
        self.running = False
        logger.info("Shutting down JARVIS-CORE...")

    async def process_query(self, query: str) -> str:
        # 1. Permission Check
        if not self.security.check_permission("core", "query", {"text": query}):
            return "Access Denied: Security policy violation."

        # 2. LLM Processing
        response = await self.llm.generate(query)
        return response

    async def _heartbeat(self):
        interval = self.config.get("system.heartbeat_interval", 60)
        while self.running:
            logger.debug("System Heartbeat: OK")
            await asyncio.sleep(interval)
