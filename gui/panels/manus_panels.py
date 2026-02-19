# Path: gui/panels/manus_panels.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QScrollArea, 
                             QComboBox, QCheckBox, QTabWidget, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal

class GitHubPanel(QFrame):
    """Manus-style GitHub Connection Panel."""
    repo_selected = pyqtSignal(str)

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setObjectName("Panel")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header = QLabel("GitHub Integration")
        header.setObjectName("Header")
        layout.addWidget(header)

        sub_header = QLabel("Connect and manage your repositories like Manus AI.")
        sub_header.setObjectName("SubHeader")
        layout.addWidget(sub_header)

        # Token Input
        token_layout = QVBoxLayout()
        token_label = QLabel("Personal Access Token")
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("ghp_xxxxxxxxxxxx")
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        token_layout.addWidget(token_label)
        token_layout.addWidget(self.token_input)
        layout.addLayout(token_layout)

        # Repo URL Input
        repo_layout = QVBoxLayout()
        repo_label = QLabel("Repository URL")
        self.repo_input = QLineEdit()
        self.repo_input.setPlaceholderText("https://github.com/user/repo")
        repo_layout.addWidget(repo_label)
        repo_layout.addWidget(self.repo_input)
        layout.addLayout(repo_layout)

        # Action Buttons
        btn_layout = QHBoxLayout()
        self.connect_btn = QPushButton("Connect & Clone")
        self.connect_btn.setObjectName("PrimaryButton")
        self.connect_btn.clicked.connect(self.on_connect)
        
        self.audit_btn = QPushButton("Run Full Audit")
        self.audit_btn.clicked.connect(self.on_audit)
        
        btn_layout.addWidget(self.connect_btn)
        btn_layout.addWidget(self.audit_btn)
        layout.addLayout(btn_layout)

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        layout.addStretch()

    def on_connect(self):
        repo_url = self.repo_input.text()
        token = self.token_input.text()
        if repo_url:
            # Update config dynamically
            self.controller.config["github"] = {"token": token}
            self.repo_selected.emit(repo_url)
            self.controller.gui.update_activity(f"Connecting to {repo_url}...")

    def on_audit(self):
        self.controller.gui.update_activity("Starting full repository audit...")

class SettingsPanel(QFrame):
    """Advanced Settings Dashboard for LUNA-ULTRA."""
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setObjectName("Panel")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header = QLabel("Advanced Settings")
        header.setObjectName("Header")
        layout.addWidget(header)

        tabs = QTabWidget()
        
        # 1. LLM Settings
        llm_tab = QWidget()
        llm_layout = QVBoxLayout(llm_tab)
        
        llm_model_label = QLabel("Default LLM Model")
        self.llm_model_combo = QComboBox()
        self.llm_model_combo.addItems(["deepseek-chat", "gpt-4-turbo", "claude-3-opus"])
        llm_layout.addWidget(llm_model_label)
        llm_layout.addWidget(self.llm_model_combo)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter API Key")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        llm_layout.addWidget(QLabel("API Key Override"))
        llm_layout.addWidget(self.api_key_input)
        
        llm_layout.addStretch()
        tabs.addTab(llm_tab, "LLM")

        # 2. Security Settings
        sec_tab = QWidget()
        sec_layout = QVBoxLayout(sec_tab)
        
        self.sec_level_combo = QComboBox()
        self.sec_level_combo.addItems(["SAFE", "STANDARD", "ADVANCED", "ROOT"])
        sec_layout.addWidget(QLabel("Security Level"))
        sec_layout.addWidget(self.sec_level_combo)
        
        self.dry_run_check = QCheckBox("Enable Dry-Run Mode")
        sec_layout.addWidget(self.dry_run_check)
        
        self.sentinel_check = QCheckBox("Enable Security Sentinel")
        self.sentinel_check.setChecked(True)
        sec_layout.addWidget(self.sentinel_check)
        
        sec_layout.addStretch()
        tabs.addTab(sec_tab, "Security")

        # 3. Voice Settings
        voice_tab = QWidget()
        voice_layout = QVBoxLayout(voice_tab)
        
        self.voice_enabled = QCheckBox("Enable Voice Interaction")
        voice_layout.addWidget(self.voice_enabled)
        
        self.wake_word_input = QLineEdit()
        self.wake_word_input.setText("LUNA")
        voice_layout.addWidget(QLabel("Wake Word"))
        voice_layout.addWidget(self.wake_word_input)
        
        voice_layout.addStretch()
        tabs.addTab(voice_tab, "Voice")

        layout.addWidget(tabs)

        # Save Button
        self.save_btn = QPushButton("Apply & Save Settings")
        self.save_btn.setObjectName("PrimaryButton")
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)

    def save_settings(self):
        # Update controller config dynamically
        self.controller.config["llm"]["model"] = self.llm_model_combo.currentText()
        self.controller.config["security"]["level"] = self.sec_level_combo.currentText()
        self.controller.config["security"]["dry_run"] = self.dry_run_check.isChecked()
        self.controller.gui.update_activity("Settings applied successfully.")
