# Path: gui/widgets/chat_bubble.py
import tkinter as tk
from tkinter import ttk

class ChatBubble(ttk.Frame):
    """
    LUNA-ULTRA Chat Bubble: Custom widget for chat messages.
    """
    def __init__(self, parent, text, sender="user"):
        super().__init__(parent)
        self.text = text
        self.sender = sender
        self.create_widgets()

    def create_widgets(self):
        bg_color = "#3c3c3c" if self.sender == "user" else "#252526"
        fg_color = "#ffffff"
        
        label = tk.Label(self, text=self.text, bg=bg_color, fg=fg_color, wraplength=400, justify="left", padx=10, pady=5)
        label.pack(side="left" if self.sender == "user" else "right", padx=5, pady=2)
