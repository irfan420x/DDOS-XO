# Path: gui/panels/settings_panel.py
import tkinter as tk
from tkinter import ttk

class SettingsPanel(ttk.Frame):
    """
    LUNA-ULTRA Settings Panel: Configuration UI.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Settings", font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))
        ttk.Label(self, text="Permission Level:").pack(anchor="w")
        self.perm_var = tk.StringVar(value="SAFE")
        ttk.OptionMenu(self, self.perm_var, "SAFE", "SAFE", "STANDARD", "ADVANCED", "ROOT").pack(fill="x", pady=5)
        
        ttk.Label(self, text="LLM Provider:").pack(anchor="w")
        self.llm_var = tk.StringVar(value="DeepSeek")
        ttk.OptionMenu(self, self.llm_var, "DeepSeek", "DeepSeek", "OpenAI", "Anthropic", "Gemini").pack(fill="x", pady=5)
