# Path: gui/main_window.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Dict, Any
import threading
import asyncio
from gui.voice_engine import VoiceEngine

class LunaGUI:
    """
    LUNA-ULTRA Main GUI Window: Modern Dark UI with integrated voice mode.
    """
    def __init__(self, controller: Any):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("🌙 LUNA-ULTRA")
        self.root.geometry(self.controller.config.get('gui', {}).get('window_size', "1100x750"))
        self.root.configure(bg="#121212")
        
        # Initialize Voice Engine
        self.voice_engine = VoiceEngine(self.controller.config)
        
        self.setup_styles()
        self.create_widgets()
        self.display_welcome_message()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#121212")
        style.configure("TLabel", background="#121212", foreground="#e0e0e0", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#121212", foreground="#bb86fc", font=("Segoe UI", 14, "bold"))
        style.configure("TButton", background="#1f1f1f", foreground="#ffffff", borderwidth=0, font=("Segoe UI", 10))
        style.configure("Action.TButton", background="#bb86fc", foreground="#000000", borderwidth=0, font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[('active', '#333333')])
        style.map("Action.TButton", background=[('active', '#d7b7fd')])

    def create_widgets(self):
        # Top Bar
        top_bar = ttk.Frame(self.root)
        top_bar.pack(side="top", fill="x", padx=20, pady=15)
        ttk.Label(top_bar, text="🌙 LUNA-ULTRA", style="Header.TLabel").pack(side="left")
        
        status = self.controller.get_status()
        self.status_label = ttk.Label(
            top_bar, 
            text=f"● {status['provider'].upper()} ACTIVE | {status['permission']}", 
            foreground="#03dac6",
            font=("Segoe UI", 9, "bold")
        )
        self.status_label.pack(side="right", padx=10)

        # Main Content
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Left Panel (System Controls)
        left_panel = ttk.Frame(main_frame, width=250)
        left_panel.pack(side="left", fill="y", padx=(0, 20))
        
        ttk.Label(left_panel, text="CONTROL PANEL", font=("Segoe UI", 11, "bold"), foreground="#bb86fc").pack(anchor="w", pady=(0, 15))
        
        # Voice Toggle
        voice_frame = ttk.Frame(left_panel)
        voice_frame.pack(fill="x", pady=10)
        ttk.Label(voice_frame, text="Voice Mode:").pack(side="left")
        self.voice_var = tk.BooleanVar(value=self.voice_engine.enabled)
        self.voice_toggle = ttk.Checkbutton(
            voice_frame, 
            variable=self.voice_var, 
            command=self.toggle_voice
        )
        self.voice_toggle.pack(side="right")

        # Permission Level
        ttk.Label(left_panel, text="Permission Level:").pack(anchor="w", pady=(15, 5))
        self.perm_var = tk.StringVar(value=status['permission'])
        perm_menu = ttk.OptionMenu(
            left_panel, 
            self.perm_var, 
            status['permission'], 
            "SAFE", "STANDARD", "ADVANCED", "ROOT",
            command=self.update_permission
        )
        perm_menu.pack(fill="x", pady=5)

        # System Info Card
        info_card = tk.Frame(left_panel, bg="#1f1f1f", padx=15, pady=15)
        info_card.pack(fill="x", pady=20)
        tk.Label(info_card, text="SYSTEM STATUS", bg="#1f1f1f", fg="#bb86fc", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.user_label = tk.Label(info_card, text=f"User: {status['user']}", bg="#1f1f1f", fg="#e0e0e0", font=("Segoe UI", 9)).pack(anchor="w", pady=(5, 0))
        self.mode_label = tk.Label(info_card, text=f"Mode: {status['mode']}", bg="#1f1f1f", fg="#e0e0e0", font=("Segoe UI", 9)).pack(anchor="w")
        self.os_label = tk.Label(info_card, text=f"OS: {status['os_type']}", bg="#1f1f1f", fg="#e0e0e0", font=("Segoe UI", 9)).pack(anchor="w")

        # Center (Chat Area)
        chat_container = tk.Frame(main_frame, bg="#1e1e1e", highlightbackground="#333333", highlightthickness=1)
        chat_container.pack(side="left", fill="both", expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_container, 
            bg="#1e1e1e", 
            fg="#e0e0e0", 
            font=("Consolas", 11),
            padx=15,
            pady=15,
            borderwidth=0,
            highlightthickness=0
        )
        self.chat_display.pack(fill="both", expand=True)
        
        # Input Area
        input_container = ttk.Frame(chat_container)
        input_container.pack(fill="x", padx=15, pady=15)
        
        self.input_field = tk.Entry(
            input_container, 
            bg="#2c2c2c", 
            fg="#ffffff", 
            insertbackground="#bb86fc", 
            borderwidth=0,
            font=("Segoe UI", 11),
            highlightbackground="#444444",
            highlightthickness=1
        )
        self.input_field.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.input_field.bind("<Return>", self.send_message)
        
        send_btn = ttk.Button(input_container, text="SEND", style="Action.TButton", command=self.send_message)
        send_btn.pack(side="right")

    def toggle_voice(self):
        self.voice_engine.toggle(self.voice_var.get())
        state = "Enabled" if self.voice_var.get() else "Disabled"
        self.chat_display.insert(tk.END, f"SYSTEM: Voice mode {state}\n\n")
        self.chat_display.see(tk.END)

    def update_permission(self, level):
        # Update logic here if needed to sync with controller
        self.chat_display.insert(tk.END, f"SYSTEM: Permission level changed to {level}\n\n")
        self.chat_display.see(tk.END)

    def display_welcome_message(self):
        welcome = self.controller.config.get('gui', {}).get('welcome_message', "Welcome back, IRFAN.")
        self.chat_display.insert(tk.END, f"🌙 LUNA: {welcome}\n\n")
        self.chat_display.see(tk.END)
        # Voice welcome
        self.voice_engine.speak(welcome)

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
        response_data = loop.run_until_complete(self.controller.orchestrator.handle_task(msg))
        
        # Extract the actual text response
        if response_data.get("type") == "chat":
            response = response_data.get("response", "No response received.")
        else:
            # For tool actions, summarize results
            results = response_data.get("results", [])
            if results:
                last_result = results[-1].get("result", {})
                if last_result.get("success"):
                    response = f"Task completed successfully. Output: {last_result.get('output', 'Success')}"
                else:
                    response = f"Task failed: {last_result.get('error', 'Unknown error')}"
            else:
                response = "No actions were performed."
                
        self.root.after(0, self.update_chat, response)

    def update_chat(self, response):
        # Remove the "Thinking..." line before adding response
        self.chat_display.delete("end-2l", "end-1l")
        self.chat_display.insert(tk.END, f"🌙 LUNA: {response}\n\n")
        self.chat_display.see(tk.END)
        # Speak the response
        self.voice_engine.speak(response)

    def run(self):
        self.root.mainloop()
