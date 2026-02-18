# Path: core/module_loader.py
import importlib
import logging
from typing import Any, Optional

class ModuleLoader:
    """
    Handles safe importing of optional modules with graceful fallbacks.
    """
    @staticmethod
    def safe_import(module_name: str, class_name: Optional[str] = None) -> Any:
        try:
            module = importlib.import_module(module_name)
            if class_name:
                return getattr(module, class_name)
            return module
        except (ImportError, AttributeError) as e:
            logging.warning(f"ModuleLoader: Optional module '{module_name}' is unavailable. Reason: {e}")
            return None

    @staticmethod
    def is_available(module_name: str) -> bool:
        try:
            importlib.import_module(module_name)
            return True
        except ImportError:
            return False
