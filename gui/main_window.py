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
    QFrame, QScrollArea, QProgressBar, QSplitter, QStackedWidget,
    QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QSize
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette
import qtawesome as qta

from gui.themes.manus_theme import MANUS_STYLE
from gui.panels.manus_panels import GitHubPanel, SettingsPanel
from gui.voice_engine import VoiceEngine

class WorkerSignals(QObject):
    response_received = pyqtSignal(str)
    activity_logged = pyqtSignal(str)
    thought_logged = pyqtSignal(str)

class LunaGUI(QMainWindow):
    """
    LUNA-ULTRA v2.5: Modern Manus-style GUI with GitHub & Advanced Settings.
    """
    def __init__(self, controller: Any):
        super().__init__()
        self.controller = controller
        self.controller.gui = self
        self.signals = WorkerSignals()
        
        # Initialize Voice Engine
        self.voice_engine = VoiceEngine(self.controller.config)
        
        self.setWindowTitle("🌙 LUNA-ULTRA | Autonomous System")
        self.setMinimumSize(1280, 850)
        self.setStyleSheet(MANUS_STYLE)
        
        self.setup_ui()
        self.setup_signals()
        self.start_system_monitors()
        
        self.display_welcome_message()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- 1. SIDEBAR (Navigation) ---
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(80)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 30, 10, 30)
        sidebar_layout.setSpacing(25)

        # Logo
        logo = QLabel("🌙")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 32px;")
        sidebar_layout.addWidget(logo)

        # Nav Buttons
        self.nav_chat = self.create_nav_btn("comment", "Chat")
        self.nav_github = self.create_nav_btn("github", "GitHub")
        self.nav_settings = self.create_nav_btn("cog", "Settings")
        
        sidebar_layout.addWidget(self.nav_chat)
        sidebar_layout.addWidget(self.nav_github)
        sidebar_layout.addWidget(self.nav_settings)
        
        sidebar_layout.addStretch()
        
        # Status Dot
        self.status_dot = QLabel("●")
        self.status_dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_dot.setStyleSheet("color: #10B981; font-size: 20px;")
        sidebar_layout.addWidget(self.status_dot)

        main_layout.addWidget(sidebar)

        # --- 2. MAIN CONTENT AREA ---
        content_area = QFrame()
        content_area.setObjectName("MainContent")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Top Header
        header_layout = QHBoxLayout()
        self.page_title = QLabel("Chat Interface")
        self.page_title.setObjectName("Header")
        header_layout.addWidget(self.page_title)
        
        header_layout.addStretch()
        
        # Stats
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setFixedWidth(100)
        self.cpu_bar.setFixedHeight(6)
        self.cpu_bar.setTextVisible(False)
        header_layout.addWidget(QLabel("CPU"))
        header_layout.addWidget(self.cpu_bar)
        
        self.ram_bar = QProgressBar()
        self.ram_bar.setFixedWidth(100)
        self.ram_bar.setFixedHeight(6)
        self.ram_bar.setTextVisible(False)
        header_layout.addWidget(QLabel("RAM"))
        header_layout.addWidget(self.ram_bar)
        
        content_layout.addLayout(header_layout)
        content_layout.addSpacing(20)

        # Stacked Widget for Pages
        self.pages = QStackedWidget()
        
        # Page 1: Chat
        chat_page = QWidget()
        chat_layout = QHBoxLayout(chat_page)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        
        chat_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Chat Main
        chat_main = QWidget()
        chat_main_layout = QVBoxLayout(chat_main)
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setObjectName("Panel")
        chat_main_layout.addWidget(self.chat_display)
        
        self.thought_display = QTextEdit()
        self.thought_display.setReadOnly(True)
        self.thought_display.setPlaceholderText("Reasoning process...")
        self.thought_display.setMaximumHeight(100)
        self.thought_display.setStyleSheet("background-color: #16161D; color: #9CA3AF; border: none;")
        chat_main_layout.addWidget(self.thought_display)
        
        input_frame = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Message LUNA...")
        self.input_field.returnPressed.connect(self.send_message)
        input_frame.addWidget(self.input_field)
        
        send_btn = QPushButton("Send")
        send_btn.setObjectName("PrimaryButton")
        send_btn.clicked.connect(self.send_message)
        input_frame.addWidget(send_btn)
        chat_main_layout.addLayout(input_frame)
        
        chat_splitter.addWidget(chat_main)
        
        # Activity Sidebar
        activity_side = QFrame()
        activity_side.setObjectName("Panel")
        activity_side.setFixedWidth(300)
        activity_layout = QVBoxLayout(activity_side)
        activity_layout.addWidget(QLabel("LIVE ACTIVITY", objectName="SubHeader"))
        self.activity_log = QTextEdit()
        self.activity_log.setReadOnly(True)
        self.activity_log.setStyleSheet("font-family: 'Consolas'; font-size: 11px; color: #10B981; background: transparent; border: none;")
        activity_layout.addWidget(self.activity_log)
        
        chat_splitter.addWidget(activity_side)
        chat_layout.addWidget(chat_splitter)
        
        self.pages.addWidget(chat_page)
        
        # Page 2: GitHub
        self.github_panel = GitHubPanel(self.controller)
        self.pages.addWidget(self.github_panel)
        
        # Page 3: Settings
        self.settings_panel = SettingsPanel(self.controller)
        self.pages.addWidget(self.settings_panel)
        
        content_layout.addWidget(self.pages)
        main_layout.addWidget(content_area)

    def create_nav_btn(self, icon_name, tooltip):
        btn = QPushButton()
        btn.setIcon(qta.icon(f"fa5s.{icon_name}", color="#9CA3AF"))
        btn.setIconSize(QSize(24, 24))
        btn.setToolTip(tooltip)
        btn.setFixedSize(50, 50)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("background: transparent; border: none;")
        
        # Connect to page switching
        if tooltip == "Chat": btn.clicked.connect(lambda: self.switch_page(0, "Chat Interface"))
        elif tooltip == "GitHub": btn.clicked.connect(lambda: self.switch_page(1, "GitHub Integration"))
        elif tooltip == "Settings": btn.clicked.connect(lambda: self.switch_page(2, "Advanced Settings"))
        
        return btn

    def switch_page(self, index, title):
        self.pages.setCurrentIndex(index)
        self.page_title.setText(title)
        # Update icon colors
        btns = [self.nav_chat, self.nav_github, self.nav_settings]
        for i, btn in enumerate(btns):
            color = "#4F46E5" if i == index else "#9CA3AF"
            # Re-set icon with new color (simplified)
            icon_names = ["comment", "github", "cog"]
            btn.setIcon(qta.icon(f"fa5s.{icon_names[i]}", color=color))

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
        self.cpu_bar.setValue(int(cpu))
        self.ram_bar.setValue(int(ram))

    def display_welcome_message(self):
        welcome = self.controller.config.get('gui', {}).get('welcome_message', "Welcome back, IRFAN. LUNA-ULTRA v2.5 is online.")
        self.chat_display.append(f"<div style='margin-bottom: 10px;'><b style='color: #4F46E5;'>🌙 LUNA:</b> {welcome}</div>")
        self.voice_engine.speak(welcome)

    def send_message(self):
        text = self.input_field.text().strip()
        if text:
            self.chat_display.append(f"<div style='margin-bottom: 10px;'><b style='color: #E0E0E6;'>You:</b> {text}</div>")
            self.input_field.clear()
            self.thought_display.clear()
            self.update_activity(f"Processing: {text[:30]}...")
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
                response = f"Task completed. Output: {results[-1].get('result', {}).get('output', 'Success')}" if results else "Processed."
            
            self.signals.response_received.emit(response)
        except Exception as e:
            self.signals.response_received.emit(f"System Error: {str(e)}")

    def update_chat(self, response):
        self.chat_display.append(f"<div style='margin-bottom: 10px;'><b style='color: #4F46E5;'>🌙 LUNA:</b> {response}</div>")
        self.voice_engine.speak(response)

    def update_activity(self, text):
        self.activity_log.append(f"> {text}")

    def update_thought(self, text):
        self.thought_display.setText(text)

    def run(self):
        self.show()
