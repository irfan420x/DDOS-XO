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
    QListWidget, QListWidgetItem, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QSize
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette, QTextCursor
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
    LUNA-ULTRA v2.6: Professional AI Interface with Modern Aesthetics.
    """
    def __init__(self, controller: Any):
        super().__init__()
        self.controller = controller
        self.controller.gui = self
        self.signals = WorkerSignals()
        
        # Initialize Voice Engine
        self.voice_engine = VoiceEngine(self.controller.config)
        
        self.setWindowTitle("LUNA-ULTRA | Professional AI Architect")
        self.setMinimumSize(1300, 900)
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
        sidebar.setFixedWidth(85)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 40, 10, 40)
        sidebar_layout.setSpacing(30)

        # Logo with Glow
        logo = QLabel("🌙")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 36px; margin-bottom: 20px;")
        sidebar_layout.addWidget(logo)

        # Nav Buttons
        self.nav_chat = self.create_nav_btn("comment", "Chat")
        self.nav_agent = self.create_nav_btn("robot", "Agent")
        self.nav_github = self.create_nav_btn("github", "GitHub")
        self.nav_settings = self.create_nav_btn("cog", "Settings")
        
        sidebar_layout.addWidget(self.nav_chat)
        sidebar_layout.addWidget(self.nav_agent)
        sidebar_layout.addWidget(self.nav_github)
        sidebar_layout.addWidget(self.nav_settings)
        
        sidebar_layout.addStretch()
        
        # Status Indicator
        status_container = QVBoxLayout()
        self.status_dot = QLabel("●")
        self.status_dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_dot.setStyleSheet("color: #10B981; font-size: 24px;")
        status_container.addWidget(self.status_dot)
        
        status_label = QLabel("ONLINE")
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_label.setStyleSheet("color: #6B7280; font-size: 9px; font-weight: bold;")
        status_container.addWidget(status_label)
        sidebar_layout.addLayout(status_container)

        main_layout.addWidget(sidebar)

        # --- 2. MAIN CONTENT AREA ---
        content_area = QFrame()
        content_area.setObjectName("MainContent")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(30, 30, 30, 30)
        
        # Top Header
        header_layout = QHBoxLayout()
        header_info = QVBoxLayout()
        self.page_title = QLabel("Chat Interface")
        self.page_title.setObjectName("Header")
        header_info.addWidget(self.page_title)
        
        self.page_subtitle = QLabel("Autonomous AI Interaction & Reasoning")
        self.page_subtitle.setObjectName("SubHeader")
        header_info.addWidget(self.page_subtitle)
        header_layout.addLayout(header_info)
        
        header_layout.addStretch()
        
        # System Monitors
        monitor_layout = QHBoxLayout()
        monitor_layout.setSpacing(20)
        
        def create_monitor(label_text):
            container = QVBoxLayout()
            lbl = QLabel(label_text)
            lbl.setObjectName("SubHeader")
            lbl.setStyleSheet("font-size: 10px;")
            bar = QProgressBar()
            bar.setFixedWidth(120)
            bar.setFixedHeight(4)
            bar.setTextVisible(False)
            container.addWidget(lbl)
            container.addWidget(bar)
            return container, bar

        cpu_cont, self.cpu_bar = create_monitor("CPU USAGE")
        ram_cont, self.ram_bar = create_monitor("RAM USAGE")
        
        monitor_layout.addLayout(cpu_cont)
        monitor_layout.addLayout(ram_cont)
        header_layout.addLayout(monitor_layout)
        
        content_layout.addLayout(header_layout)
        content_layout.addSpacing(30)

        # Stacked Widget for Pages
        self.pages = QStackedWidget()
        
        # Page 1: Chat
        chat_page = QWidget()
        chat_layout = QHBoxLayout(chat_page)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.setSpacing(20)
        
        chat_splitter = QSplitter(Qt.Orientation.Horizontal)
        chat_splitter.setHandleWidth(1)
        chat_splitter.setStyleSheet("QSplitter::handle { background-color: transparent; }")
        
        # Chat Main
        chat_main = QFrame()
        chat_main.setObjectName("Panel")
        chat_main_layout = QVBoxLayout(chat_main)
        chat_main_layout.setContentsMargins(20, 20, 20, 20)
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background: transparent; border: none; font-size: 14px; line-height: 1.6;")
        self.chat_display.setPlaceholderText("Conversation history will appear here...")
        chat_main_layout.addWidget(self.chat_display)
        
        # Thought Process Area
        thought_frame = QFrame()
        thought_frame.setStyleSheet("background-color: #111114; border-radius: 10px; border: 1px solid #1F1F23;")
        thought_frame_layout = QVBoxLayout(thought_frame)
        thought_frame_layout.setContentsMargins(15, 10, 15, 10)
        
        thought_header = QHBoxLayout()
        thought_icon = QLabel()
        thought_icon.setPixmap(qta.icon("fa5s.brain", color="#5850EC").pixmap(14, 14))
        thought_header.addWidget(thought_icon)
        thought_header.addWidget(QLabel("REASONING PROCESS", objectName="SubHeader"))
        thought_header.addStretch()
        thought_frame_layout.addLayout(thought_header)
        
        self.thought_display = QTextEdit()
        self.thought_display.setReadOnly(True)
        self.thought_display.setPlaceholderText("Waiting for input...")
        self.thought_display.setMaximumHeight(80)
        self.thought_display.setStyleSheet("background: transparent; border: none; color: #9CA3AF; font-family: 'Consolas'; font-size: 12px;")
        thought_frame_layout.addWidget(self.thought_display)
        chat_main_layout.addWidget(thought_frame)
        
        # Input Area
        input_container = QFrame()
        input_container.setStyleSheet("background-color: #111114; border-radius: 12px; border: 1px solid #1F1F23;")
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(10, 5, 10, 5)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type a message or command for LUNA...")
        self.input_field.setStyleSheet("background: transparent; border: none; padding: 10px; font-size: 14px;")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        self.send_btn = QPushButton()
        self.send_btn.setIcon(qta.icon("fa5s.paper-plane", color="white"))
        self.send_btn.setFixedSize(40, 40)
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.setStyleSheet("background-color: #5850EC; border-radius: 8px; border: none;")
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)
        
        chat_main_layout.addSpacing(10)
        chat_main_layout.addWidget(input_container)
        
        chat_splitter.addWidget(chat_main)
        
        # Activity Sidebar
        activity_side = QFrame()
        activity_side.setObjectName("Panel")
        activity_side.setFixedWidth(320)
        activity_layout = QVBoxLayout(activity_side)
        activity_layout.setContentsMargins(20, 20, 20, 20)
        
        act_header = QHBoxLayout()
        act_header.addWidget(QLabel("LIVE ACTIVITY", objectName="SubHeader"))
        act_header.addStretch()
        activity_layout.addLayout(act_header)
        
        self.activity_log = QTextEdit()
        self.activity_log.setReadOnly(True)
        self.activity_log.setStyleSheet("font-family: 'Consolas'; font-size: 11px; color: #10B981; background: transparent; border: none;")
        activity_layout.addWidget(self.activity_log)
        
        chat_splitter.addWidget(activity_side)
        chat_layout.addWidget(chat_splitter)
        
        self.pages.addWidget(chat_page)
        
        # Other Pages
        from gui.panels.agent_mode_panel import AgentModePanel
        self.agent_panel = AgentModePanel(self.controller)
        self.pages.addWidget(self.agent_panel)
        
        self.github_panel = GitHubPanel(self.controller)
        self.pages.addWidget(self.github_panel)
        
        self.settings_panel = SettingsPanel(self.controller)
        self.pages.addWidget(self.settings_panel)
        
        content_layout.addWidget(self.pages)
        main_layout.addWidget(content_area)

    def create_nav_btn(self, icon_name, tooltip):
        btn = QPushButton()
        btn.setIcon(qta.icon(f"fa5s.{icon_name}", color="#6B7280"))
        btn.setIconSize(QSize(22, 22))
        btn.setToolTip(tooltip)
        btn.setFixedSize(55, 55)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("background: transparent; border: none; border-radius: 15px;")
        
        # Connect to page switching
        if tooltip == "Chat": btn.clicked.connect(lambda: self.switch_page(0, "Chat Interface", "Autonomous AI Interaction & Reasoning"))
        elif tooltip == "Agent": btn.clicked.connect(lambda: self.switch_page(1, "Agent Mode", "Multi-Agent Coordination & Execution"))
        elif tooltip == "GitHub": btn.clicked.connect(lambda: self.switch_page(2, "GitHub Integration", "Secure Repository Management & Deployment"))
        elif tooltip == "Settings": btn.clicked.connect(lambda: self.switch_page(3, "Advanced Settings", "System Configuration & Personality Tuning"))
        
        return btn

    def switch_page(self, index, title, subtitle):
        self.pages.setCurrentIndex(index)
        self.page_title.setText(title)
        self.page_subtitle.setText(subtitle)
        
        btns = [self.nav_chat, self.nav_agent, self.nav_github, self.nav_settings]
        icon_names = ["comment", "robot", "github", "cog"]
        for i, btn in enumerate(btns):
            if i == index:
                btn.setIcon(qta.icon(f"fa5s.{icon_names[i]}", color="#5850EC"))
                btn.setStyleSheet("background-color: #1F1F23; border: none; border-radius: 15px;")
            else:
                btn.setIcon(qta.icon(f"fa5s.{icon_names[i]}", color="#6B7280"))
                btn.setStyleSheet("background: transparent; border: none; border-radius: 15px;")

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
        welcome = self.controller.config.get('gui', {}).get('welcome_message', "System online. LUNA-ULTRA v2.6 ready for command, IRFAN.")
        self.update_chat(welcome)

    def send_message(self):
        text = self.input_field.text().strip()
        if text:
            self.chat_display.append(f"<div style='margin: 10px 0;'><span style='color: #6B7280; font-weight: bold;'>USER:</span><br/>{text}</div>")
            self.input_field.clear()
            self.thought_display.clear()
            self.update_activity(f"Analyzing intent: {text[:40]}...")
            threading.Thread(target=self.process_input_async, args=(text,), daemon=True).start()
            
            # Scroll to bottom
            self.chat_display.moveCursor(QTextCursor.MoveOperation.End)

    def process_input_async(self, text):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response_data = loop.run_until_complete(self.controller.orchestrator.handle_task(text))
            thought = response_data.get("thought", "Processing...")
            self.signals.thought_logged.emit(thought)
            
            if response_data.get("type") == "chat":
                response = response_data.get("response", "No response.")
            else:
                results = response_data.get("results", [])
                response = results[-1].get('result', {}).get('output', 'Task completed successfully.') if results else "Action performed."
            
            self.signals.response_received.emit(response)
        except Exception as e:
            self.signals.response_received.emit(f"System Error: {str(e)}")

    def update_chat(self, response):
        # Format response with simple HTML for better look
        formatted = f"<div style='margin: 15px 0; padding: 12px; background-color: #141417; border-left: 4px solid #5850EC; border-radius: 4px;'>" \
                    f"<span style='color: #5850EC; font-weight: bold;'>LUNA:</span><br/>{response}</div>"
        self.chat_display.append(formatted)
        self.chat_display.moveCursor(QTextCursor.MoveOperation.End)
        self.voice_engine.speak(response)

    def update_activity(self, text):
        self.activity_log.append(f"<span style='color: #10B981;'>[SYSTEM]</span> {text}")
        self.activity_log.moveCursor(QTextCursor.MoveOperation.End)

    def update_thought(self, text):
        self.thought_display.setText(text)

    def run(self):
        self.show()
        # Set initial active button
        self.switch_page(0, "Chat Interface", "Autonomous AI Interaction & Reasoning")
