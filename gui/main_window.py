# Path: gui/main_window.py
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Dict, Any
import threading
import asyncio

class LunaGUI:
    """
    LUNA-ULTRA Main GUI Window: Modern Dark UI with integrated welcome message.
    """
    def __init__(self, controller: Any):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("🌙 LUNA-ULTRA")
        self.root.geometry(self.controller.config.get('gui', {}).get('window_size', "1000x700"))
        self.root.configure(bg="#1e1e1e")
        self.setup_styles()
        self.create_widgets()
        self.display_welcome_message()

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
        
        status = self.controller.get_status()
        self.status_label = ttk.Label(
            top_bar, 
            text=f"🟢 {status['provider'].upper()} Connected | {status['permission']}", 
            foreground="#4caf50"
        )
        self.status_label.pack(side="right", padx=10)

        # Main Content
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Panel (System Info)
        left_panel = ttk.Frame(main_frame, width=200)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        ttk.Label(left_panel, text="System Info", font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))
        
        ttk.Label(left_panel, text=f"User: {status['user']}").pack(anchor="w", pady=2)
        ttk.Label(left_panel, text=f"Mode: {status['mode']}").pack(anchor="w", pady=2)
        
        ttk.Label(left_panel, text="Permission Level:").pack(anchor="w", pady=(10, 0))
        self.perm_var = tk.StringVar(value=status['permission'])
        ttk.OptionMenu(left_panel, self.perm_var, status['permission'], "SAFE", "STANDARD", "ADVANCED", "ROOT").pack(fill="x", pady=5)

        # Center (Chat)
        chat_frame = ttk.Frame(main_frame)
        chat_frame.pack(side="left", fill="both", expand=True)
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, 
            bg="#252526", 
            fg="#ffffff", 
            font=("Consolas", 10),
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill="both", expand=True)
        
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill="x", pady=(10, 0))
        self.input_field = tk.Entry(input_frame, bg="#3c3c3c", fg="#ffffff", insertbackground="white", borderwidth=0)
        self.input_field.pack(side="left", fill="x", expand=True, ipady=5)
        self.input_field.bind("<Return>", self.send_message)
        ttk.Button(input_frame, text="Send", command=self.send_message).pack(side="right", padx=(10, 0))

    def display_welcome_message(self):
        welcome = self.controller.config.get('gui', {}).get('welcome_message', "Welcome back, IRFAN.")
        self.chat_display.insert(tk.END, f"🌙 LUNA: {welcome}\n\n")
        self.chat_display.see(tk.END)

    def send_message(self, event=None):
        msg = self.input_field.get()
        if msg:
            self.chat_display.insert(tk.END, f"You: {msg}\n")
            self.input_field.delete(0, tk.END)
            self.chat_display.insert(tk.END, "LUNA: Thinking...\n")
            self.chat_display.see(tk.END)
            
            # Run processing in a separate thread to keep GUI responsive
            threading.Thread(target=self.process_input_async, args=(msg,), daemon=True).start()

    def process_input_async(self, msg):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(self.controller.process_input(msg))
        self.root.after(0, self.update_chat, response)

    def update_chat(self, response):
        self.chat_display.insert(tk.END, f"LUNA: {response}\n\n")
        self.chat_display.see(tk.END)

    def run(self):
        self.root.mainloop()
