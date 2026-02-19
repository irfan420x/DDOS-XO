# Path: plugins/loader.py
import os
import importlib.util
import logging
from typing import Dict, Any, List, Optional

class PluginLoader:
    """
    LUNA-ULTRA Plugin System: Safely loads and isolates external plugins.
    """
    def __init__(self, controller):
        self.controller = controller
        self.plugins_dir = "plugins"
        self.loaded_plugins: Dict[str, Any] = {}
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)

    def load_all(self) -> List[str]:
        """Scans and loads all valid plugins from the plugins directory."""
        logging.info(f"PluginLoader: Scanning for plugins in {self.plugins_dir}")
        plugin_files = [f for f in os.listdir(self.plugins_dir) if f.endswith(".py") and f != "__init__.py" and f != "loader.py"]
        
        loaded_names = []
        for f in plugin_files:
            plugin_name = f.replace(".py", "")
            if self.load_plugin(plugin_name):
                loaded_names.append(plugin_name)
        
        return loaded_names

    def load_plugin(self, plugin_name: str) -> bool:
        """Loads a single plugin by name."""
        plugin_path = os.path.join(self.plugins_dir, f"{plugin_name}.py")
        if not os.path.exists(plugin_path):
            logging.error(f"PluginLoader: Plugin {plugin_name} not found at {plugin_path}")
            return False

        try:
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check for mandatory 'setup' function in plugin
                if hasattr(module, "setup"):
                    # Pass controller to plugin for initialization
                    module.setup(self.controller)
                    self.loaded_plugins[plugin_name] = module
                    logging.info(f"PluginLoader: Successfully loaded plugin '{plugin_name}'")
                    return True
                else:
                    logging.warning(f"PluginLoader: Plugin '{plugin_name}' is missing mandatory 'setup(controller)' function.")
                    return False
        except Exception as e:
            logging.error(f"PluginLoader: Error loading plugin '{plugin_name}': {e}")
            return False
        return False

    def get_plugin(self, plugin_name: str) -> Optional[Any]:
        """Retrieves a loaded plugin module."""
        return self.loaded_plugins.get(plugin_name)
