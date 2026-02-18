# Path: gui/main_window.py
import sys
import os
import logging
import threading
import asyncio
import psutil
from typing import Dict, Any, Optional
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QComboBox, QCheckBox, QTextEdit, 
    QFrame, QScrollArea, QProgressBar, QSplitter, QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QSize
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette
import qtawesome as qta

from gui.themes.dark_theme import get_dark_theme
from gui.voice_engine import VoiceEngine

class WorkerSignals(QObject):
    response_received = pyqtSignal(str)
    activity_logged = pyqtSignal(str)
    thought_logged = pyqtSignal(str)

class LunaGUI(QMainWindow):
    """
    LUNA-ULTRA Main GUI Window: Modern PyQt6 3-panel dashboard.
    """
    def __init__(self, controller: Any):
        super().__init__()
        self.controller = controller
        self.controller.gui = self
        self.signals = WorkerSignals()
        
        # Initialize Voice Engine
        self.voice_engine = VoiceEngine(self.controller.config)
        
        self.setWindowTitle("🌙 LUNA-ULTRA")
        self.resize(1200, 850)
        self.setStyleSheet(get_dark_theme())
        
        self.setup_ui()
        self.setup_signals()
        self.start_system_monitors()
        
        self.display_welcome_message()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # --- TOP BAR ---
        top_bar = QFrame()
        top_bar.setFixedHeight(60)
        top_bar.setObjectName("Panel")
        top_layout = QHBoxLayout(top_bar)
        
        # Branding
        brand_label = QLabel("🌙 LUNA-ULTRA")
        brand_label.setObjectName("Header")
        top_layout.addWidget(brand_label)
        
        top_layout.addStretch()
        
        # Stats
        self.cpu_label = QLabel("CPU: 0%")
        self.ram_label = QLabel("RAM: 0%")
        top_layout.addWidget(self.cpu_label)
        top_layout.addWidget(self.ram_label)
        
        # Status Indicators
        self.llm_status = QLabel("● LLM: ONLINE")
        self.llm_status.setStyleSheet("color: #03dac6; font-weight: bold;")
        top_layout.addWidget(self.llm_status)
        
        self.perm_indicator = QLabel(f"LEVEL: {self.controller.config.get('permissions', {}).get('level', 'SAFE')}")
        self.perm_indicator.setStyleSheet("color: #cf6679; font-weight: bold;")
        top_layout.addWidget(self.perm_indicator)
        
        main_layout.addWidget(top_bar)

        # --- MAIN CONTENT (3 PANELS) ---
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 1. LEFT PANEL (Control Center)
        left_panel = QFrame()
        left_panel.setObjectName("Panel")
        left_panel.setFixedWidth(280)
        left_layout = QVBoxLayout(left_panel)
        
        left_layout.addWidget(QLabel("CONTROL CENTER", objectName="SubHeader"))
        
        # LLM Config
        left_layout.addWidget(QLabel("LLM Provider:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["deepseek", "openai", "anthropic", "gemini"])
        self.provider_combo.setCurrentText(self.controller.config.get('llm', {}).get('default_provider', 'deepseek'))
        left_layout.addWidget(self.provider_combo)
        
        left_layout.addWidget(QLabel("API Key:"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText("Enter API Key...")
        left_layout.addWidget(self.api_key_input)
        
        # Permission
        left_layout.addWidget(QLabel("Permission Level:"))
        self.perm_combo = QComboBox()
        self.perm_combo.addItems(["SAFE", "STANDARD", "ADVANCED", "ROOT"])
        self.perm_combo.setCurrentText(self.controller.config.get('permissions', {}).get('level', 'SAFE'))
        left_layout.addWidget(self.perm_combo)
        
        # Module Toggles
        left_layout.addSpacing(10)
        left_layout.addWidget(QLabel("MODULES", objectName="SubHeader"))
        self.voice_toggle = QCheckBox("Voice Interaction")
        self.voice_toggle.setChecked(self.controller.config.get('gui', {}).get('voice_mode', False))
        left_layout.addWidget(self.voice_toggle)
        
        self.vision_toggle = QCheckBox("Screen Awareness")
        self.vision_toggle.setChecked(self.controller.config.get('vision', {}).get('enabled', False))
        left_layout.addWidget(self.vision_toggle)
        
        self.auto_toggle = QCheckBox("Automation")
        self.auto_toggle.setChecked(True)
        left_layout.addWidget(self.auto_toggle)
        
        # Modes
        left_layout.addSpacing(10)
        self.always_on_toggle = QCheckBox("Always-On Mode")
        left_layout.addWidget(self.always_on_toggle)
        
        self.dry_run_toggle = QCheckBox("Dry-Run Mode")
        left_layout.addWidget(self.dry_run_toggle)
        
        left_layout.addStretch()
        
        # Apply Button
        apply_btn = QPushButton("APPLY CONFIG")
        apply_btn.setObjectName("ActionButton")
        apply_btn.clicked.connect(self.apply_config)
        left_layout.addWidget(apply_btn)
        
        content_splitter.addWidget(left_panel)
        
        # 2. CENTER PANEL (Chat & Reasoning)
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(0, 0, 0, 0)
        
        # Chat Display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setObjectName("Panel")
        center_layout.addWidget(self.chat_display, 7)
        
        # Reasoning / Thought View
        self.thought_display = QTextEdit()
        self.thought_display.setReadOnly(True)
        self.thought_display.setPlaceholderText("Reasoning process will appear here...")
        self.thought_display.setMaximumHeight(150)
        self.thought_display.setStyleSheet("background-color: #1a1f2b; color: #9ca3af; font-style: italic;")
        center_layout.addWidget(self.thought_display, 2)
        
        # Input Area
        input_frame = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask LUNA anything...")
        self.input_field.returnPressed.connect(self.send_message)
        input_frame.addWidget(self.input_field)
        
        send_btn = QPushButton("SEND")
        send_btn.setObjectName("ActionButton")
        send_btn.clicked.connect(self.send_message)
        input_frame.addWidget(send_btn)
        
        center_layout.addLayout(input_frame)
        
        content_splitter.addWidget(center_panel)
        
        # 3. RIGHT PANEL (Logs & Memory)
        right_panel = QFrame()
        right_panel.setObjectName("Panel")
        right_panel.setFixedWidth(300)
        right_layout = QVBoxLayout(right_panel)
        
        right_layout.addWidget(QLabel("LIVE ACTIVITY", objectName="SubHeader"))
        self.activity_log = QTextEdit()
        self.activity_log.setReadOnly(True)
        self.activity_log.setStyleSheet("font-family: 'Consolas'; font-size: 11px; color: #03dac6;")
        right_layout.addWidget(self.activity_log)
        
        right_layout.addWidget(QLabel("MEMORY SUMMARY", objectName="SubHeader"))
        self.memory_view = QTextEdit()
        self.memory_view.setReadOnly(True)
        self.memory_view.setMaximumHeight(200)
        right_layout.addWidget(self.memory_view)
        
        content_splitter.addWidget(right_panel)
        
        main_layout.addWidget(content_splitter)

    def setup_signals(self):
        self.signals.response_received.connect(self.update_chat)
        self.signals.activity_logged.connect(self.update_activity)
        self.signals.thought_logged.connect(self.update_thought)

    def start_system_monitors(self):
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(2000)

    def update_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        self.cpu_label.setText(f"CPU: {cpu}%")
        self.ram_label.setText(f"RAM: {ram}%")

    def display_welcome_message(self):
        welcome = self.controller.config.get('gui', {}).get('welcome_message', "Welcome back, IRFAN.")
        self.chat_display.append(f"<b style='color: #bb86fc;'>🌙 LUNA:</b> {welcome}")
        self.voice_engine.speak(welcome)

    def send_message(self):
        text = self.input_field.text().strip()
        if text:
            self.chat_display.append(f"<b style='color: #e0e0e0;'>You:</b> {text}")
            self.input_field.clear()
            self.thought_display.clear()
            self.update_activity(f"Processing: {text[:30]}...")
            
            # Run in thread
            threading.Thread(target=self.process_input_async, args=(text,), daemon=True).start()

    def process_input_async(self, text):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response_data = loop.run_until_complete(self.controller.orchestrator.handle_task(text))
            
            thought = response_data.get("thought", "Analyzing...")
            self.signals.thought_logged.emit(thought)
            
            if response_data.get("type") == "chat":
                response = response_data.get("response", "No response.")
            else:
                results = response_data.get("results", [])
                if results:
                    last_res = results[-1].get("result", {})
                    response = f"Task completed. Output: {last_res.get('output', 'Success')}" if last_res.get("success") else f"Error: {last_res.get('error')}"
                else:
                    response = "I've processed your request."
            
            self.signals.response_received.emit(response)
        except Exception as e:
            self.signals.response_received.emit(f"System Error: {str(e)}")

    def update_chat(self, response):
        self.chat_display.append(f"<b style='color: #bb86fc;'>🌙 LUNA:</b> {response}")
        self.voice_engine.speak(response)

    def update_activity(self, text):
        self.activity_log.append(f"> {text}")

    def update_thought(self, text):
        self.thought_display.setText(text)

    def apply_config(self):
        # Phase 2 logic will go here
        new_config = {
            "llm": {"default_provider": self.provider_combo.currentText()},
            "permissions": {"level": self.perm_combo.currentText()},
            "gui": {"voice_mode": self.voice_toggle.isChecked()},
            "vision": {"enabled": self.vision_toggle.isChecked()}
        }
        self.update_activity("Updating configuration...")
        # Call controller to update
        self.controller.update_config(new_config)
        self.perm_indicator.setText(f"LEVEL: {self.perm_combo.currentText()}")

    def run(self):
        self.show()
        # PyQt6 event loop is handled by the caller or sys.exit(app.exec())
