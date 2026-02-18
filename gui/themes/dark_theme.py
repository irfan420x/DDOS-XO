# Path: gui/themes/dark_theme.py
from typing import Dict, Any

class DarkTheme:
    """
    LUNA-ULTRA Dark Theme: Modern Dark UI colors and styles.
    """
    COLORS = {
        "bg_primary": "#1e1e1e",
        "bg_secondary": "#252526",
        "bg_tertiary": "#3c3c3c",
        "fg_primary": "#ffffff",
        "fg_secondary": "#cccccc",
        "accent": "#4caf50",
        "warning": "#ff9800",
        "error": "#f44336"
    }

    FONTS = {
        "title": ("Segoe UI", 14, "bold"),
        "body": ("Segoe UI", 10),
        "code": ("Consolas", 10)
    }
