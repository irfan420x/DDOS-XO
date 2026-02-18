# Path: gui/main_window.py
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Dict, Any

class LunaGUI:
    """
    LUNA-ULTRA Main GUI Window: Modern Dark UI.
    """
    def __init__(self, controller: Any):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("🌙 LUNA-ULTRA")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=("Segoe UI", 10))
        style.configure("TButton", background="#333333", foreground="#ffffff", borderwidth=0)
        style.map("TButton", background=[('active', '#444444')])

    def create_widgets(self):
        # Top Bar
        top_bar = ttk.Frame(self.root)
        top_bar.pack(side="top", fill="x", padx=10, pady=5)
        ttk.Label(top_bar, text="🌙 LUNA-ULTRA", font=("Segoe UI", 14, "bold")).pack(side="left")
        self.status_label = ttk.Label(top_bar, text="🟢 DeepSeek Connected", foreground="#4caf50")
        self.status_label.pack(side="right", padx=10)

        # Main Content
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Panel (Settings)
        left_panel = ttk.Frame(main_frame, width=200)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        ttk.Label(left_panel, text="Settings", font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))
        ttk.Label(left_panel, text="Permission Level:").pack(anchor="w")
        self.perm_var = tk.StringVar(value="SAFE")
        ttk.OptionMenu(left_panel, self.perm_var, "SAFE", "SAFE", "STANDARD", "ADVANCED", "ROOT").pack(fill="x", pady=5)

        # Center (Chat)
        chat_frame = ttk.Frame(main_frame)
        chat_frame.pack(side="left", fill="both", expand=True)
        self.chat_display = scrolledtext.ScrolledText(chat_frame, bg="#252526", fg="#ffffff", font=("Consolas", 10))
        self.chat_display.pack(fill="both", expand=True)
        
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill="x", pady=(10, 0))
        self.input_field = tk.Entry(input_frame, bg="#3c3c3c", fg="#ffffff", insertbackground="white", borderwidth=0)
        self.input_field.pack(side="left", fill="x", expand=True, ipady=5)
        self.input_field.bind("<Return>", self.send_message)
        ttk.Button(input_frame, text="Send", command=self.send_message).pack(side="right", padx=(10, 0))

    def send_message(self, event=None):
        msg = self.input_field.get()
        if msg:
            self.chat_display.insert(tk.END, f"You: {msg}\n")
            self.input_field.delete(0, tk.END)
            self.chat_display.insert(tk.END, "LUNA: Thinking...\n")
            self.chat_display.see(tk.END)

    def run(self):
        self.root.mainloop()
