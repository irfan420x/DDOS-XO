# Path: core/config_manager.py

import os
import yaml
import threading
from typing import Any, Dict, Optional
from loguru import logger

class ConfigManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ConfigManager, cls).__new__(cls)
            return cls._instance

    def __init__(self, config_path: str = "config/config.yaml"):
        if hasattr(self, '_initialized'): return
        self.config_path = config_path
        self.config = self._load_config()
        self._runtime_overrides = {}
        self._initialized = True
        logger.info(f"ConfigManager initialized with {config_path}")

    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            logger.critical(f"Configuration file missing at {self.config_path}")
            return {}
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logger.error(f"Failed to parse config: {e}")
            return {}

    def get(self, key_path: str, default: Any = None) -> Any:
        # Priority 1: Runtime Overrides
        if key_path in self._runtime_overrides:
            return self._runtime_overrides[key_path]

        # Priority 2: Environment Variables
        env_key = f"JARVIS_{key_path.replace('.', '_').upper()}"
        if env_key in os.environ:
            return os.environ[env_key]

        # Priority 3: Config File
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set_override(self, key: str, value: Any):
        with self._lock:
            self._runtime_overrides[key] = value
            logger.debug(f"Runtime override: {key} -> {value}")

    def reload(self):
        with self._lock:
            self.config = self._load_config()
            logger.info("Configuration reloaded from disk")
