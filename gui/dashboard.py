# Path: gui/dashboard.py

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QProgressBar, 
                             QTextEdit, QFrame, QStackedWidget)
from PyQt6.QtCore import Qt, QTimer
from qt_material import apply_stylesheet

class ModernDashboard(QMainWindow):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.setWindowTitle("JARVIS-CORE v2.0 PRO")
        self.setMinimumSize(1000, 700)
        self.init_ui()
        
        # Update timer for system stats
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(2000)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        
        self.btn_home = QPushButton("Dashboard")
        self.btn_modules = QPushButton("Modules")
        self.btn_security = QPushButton("Security")
        self.btn_logs = QPushButton("Audit Logs")
        
        sidebar_layout.addWidget(QLabel("JARVIS PRO"))
        sidebar_layout.addWidget(self.btn_home)
        sidebar_layout.addWidget(self.btn_modules)
        sidebar_layout.addWidget(self.btn_security)
        sidebar_layout.addWidget(self.btn_logs)
        sidebar_layout.addStretch()
        
        main_layout.addWidget(sidebar)

        # Content Area
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        
        # Stats Header
        stats_layout = QHBoxLayout()
        self.cpu_bar = QProgressBar()
        self.mem_bar = QProgressBar()
        stats_layout.addWidget(QLabel("CPU:"))
        stats_layout.addWidget(self.cpu_bar)
        stats_layout.addWidget(QLabel("MEM:"))
        stats_layout.addWidget(self.mem_bar)
        self.content_layout.addLayout(stats_layout)

        # Console
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setPlaceholderText("System initialized. Waiting for commands...")
        self.content_layout.addWidget(self.console)

        # Input
        input_layout = QHBoxLayout()
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(60)
        self.btn_send = QPushButton("Execute")
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.btn_send)
        self.content_layout.addLayout(input_layout)

        main_layout.addWidget(content)

    def update_stats(self):
        # In a real app, this would call engine.get_stats()
        import psutil
        self.cpu_bar.setValue(int(psutil.cpu_percent()))
        self.mem_bar.setValue(int(psutil.virtual_memory().percent))

    def log(self, message: str):
        self.console.append(f"<b>[SYS]</b>: {message}")

def start_gui(engine):
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    window = ModernDashboard(engine)
    window.show()
    sys.exit(app.exec())
