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
        self.controller.gui = self # Register GUI with controller
        self.root = tk.Tk()
        self.root.title("🌙 LUNA-ULTRA")
        self.root.geometry(self.controller.config.get('gui', {}).get('window_size', "1200x800"))
        self.root.configure(bg="#0b0e14")
        
        # Initialize Voice Engine
        self.voice_engine = VoiceEngine(self.controller.config)
        
        self.setup_styles()
        self.create_widgets()
        self.display_welcome_message()
        self.check_for_resume()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#0b0e14")
        style.configure("TLabel", background="#0b0e14", foreground="#e0e0e0", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#0b0e14", foreground="#bb86fc", font=("Segoe UI", 16, "bold"))
        style.configure("TButton", background="#1f2937", foreground="#ffffff", borderwidth=0, font=("Segoe UI", 10))
        style.configure("Action.TButton", background="#bb86fc", foreground="#000000", borderwidth=0, font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[('active', '#374151')])
        style.map("Action.TButton", background=[('active', '#d7b7fd')])

    def create_widgets(self):
        # Top Bar
        top_bar = ttk.Frame(self.root)
        top_bar.pack(side="top", fill="x", padx=25, pady=20)
        ttk.Label(top_bar, text="🌙 LUNA-ULTRA", style="Header.TLabel").pack(side="left")
        
        status = self.controller.get_status()
        self.status_label = ttk.Label(
            top_bar, 
            text=f"● {status['provider'].upper()} ONLINE | {status['permission']}", 
            foreground="#03dac6",
            font=("Segoe UI", 10, "bold")
        )
        self.status_label.pack(side="right", padx=10)

        # Main Layout: Three Columns
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        # 1. Left Sidebar (Controls)
        left_sidebar = ttk.Frame(content_frame, width=220)
        left_sidebar.pack(side="left", fill="y", padx=(0, 20))
        
        ttk.Label(left_sidebar, text="CONTROLS", font=("Segoe UI", 10, "bold"), foreground="#bb86fc").pack(anchor="w", pady=(0, 15))
        
        # Voice Mode
        v_frame = ttk.Frame(left_sidebar)
        v_frame.pack(fill="x", pady=5)
        ttk.Label(v_frame, text="Voice:").pack(side="left")
        self.voice_var = tk.BooleanVar(value=self.voice_engine.enabled)
        ttk.Checkbutton(v_frame, variable=self.voice_var, command=self.toggle_voice).pack(side="right")

        # Voice Selection
        ttk.Label(left_sidebar, text="Voice Personality:").pack(anchor="w", pady=(15, 5))
        self.voice_lang_var = tk.StringVar(value="English")
        voice_menu = ttk.OptionMenu(
            left_sidebar, 
            self.voice_lang_var, 
            "English", 
            *self.voice_engine.available_langs.keys(),
            command=self.change_voice
        )
        voice_menu.pack(fill="x", pady=5)

        # Permission
        ttk.Label(left_sidebar, text="Access Level:").pack(anchor="w", pady=(15, 5))
        self.perm_var = tk.StringVar(value=status['permission'])
        ttk.OptionMenu(left_sidebar, self.perm_var, status['permission'], "SAFE", "STANDARD", "ADVANCED", "ROOT").pack(fill="x", pady=5)

        # System Status Card
        info_card = tk.Frame(left_sidebar, bg="#1a1f2b", padx=15, pady=15)
        info_card.pack(fill="x", pady=25)
        tk.Label(info_card, text="AGENT STATUS", bg="#1a1f2b", fg="#bb86fc", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.user_label = tk.Label(info_card, text=f"User: {status['user']}", bg="#1a1f2b", fg="#9ca3af", font=("Segoe UI", 9)).pack(anchor="w", pady=(5, 0))
        self.mode_label = tk.Label(info_card, text=f"Mode: {status['mode']}", bg="#1a1f2b", fg="#9ca3af", font=("Segoe UI", 9)).pack(anchor="w")

        # 2. Middle Column (Chat Area)
        chat_column = ttk.Frame(content_frame)
        chat_column.pack(side="left", fill="both", expand=True)
        
        chat_container = tk.Frame(chat_column, bg="#0f172a", highlightbackground="#1e293b", highlightthickness=1)
        chat_container.pack(fill="both", expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_container, 
            bg="#0f172a", fg="#f1f5f9", font=("Segoe UI", 11),
            padx=20, pady=20, borderwidth=0, highlightthickness=0
        )
        self.chat_display.pack(fill="both", expand=True)
        
        # Input Area
        input_container = tk.Frame(chat_column, bg="#0b0e14", pady=15)
        input_container.pack(fill="x")
        
        self.input_field = tk.Entry(
            input_container, 
            bg="#1e293b", fg="#ffffff", insertbackground="#bb86fc",
            borderwidth=0, font=("Segoe UI", 12), highlightbackground="#334155", highlightthickness=1
        )
        self.input_field.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 15))
        self.input_field.bind("<Return>", self.send_message)
        
        ttk.Button(input_container, text="SEND", style="Action.TButton", command=self.send_message).pack(side="right")

        # 3. Right Sidebar (Manus-style Activity Feed)
        right_sidebar = ttk.Frame(content_frame, width=350)
        right_sidebar.pack(side="left", fill="y", padx=(20, 0))
        
        ttk.Label(right_sidebar, text="LIVE ACTIVITY", font=("Segoe UI", 10, "bold"), foreground="#bb86fc").pack(anchor="w", pady=(0, 15))
        
        activity_container = tk.Frame(right_sidebar, bg="#0f172a", highlightbackground="#1e293b", highlightthickness=1)
        activity_container.pack(fill="both", expand=True)
        
        self.activity_display = scrolledtext.ScrolledText(
            activity_container, 
            bg="#0f172a", fg="#03dac6", font=("Consolas", 10),
            padx=15, pady=15, borderwidth=0, highlightthickness=0
        )
        self.activity_display.pack(fill="both", expand=True)

    def update_activity(self, text: str):
        self.activity_display.insert(tk.END, f"> {text}\n")
        self.activity_display.see(tk.END)

    def change_voice(self, lang_name: str):
        self.voice_engine.set_language(lang_name)
        self.update_activity(f"Voice changed to {lang_name}")

    def check_for_resume(self):
        resume_data = self.controller.state_manager.get_resume_data()
        if resume_data:
            msg = f"I have a pending task: '{resume_data['current_task']}'. Would you like me to resume?"
            self.chat_display.insert(tk.END, f"🌙 LUNA: {msg}\n\n")
            self.voice_engine.speak(msg)

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
