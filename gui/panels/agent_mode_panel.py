# Path: gui/panels/agent_mode_panel.py
import logging
import asyncio
import threading
from typing import Dict, Any, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QProgressBar, QFrame, QScrollArea, QListWidget,
    QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QFont


class AgentModeSignals(QObject):
    plan_generated = pyqtSignal(dict)
    execution_started = pyqtSignal()
    step_completed = pyqtSignal(int, bool)
    execution_finished = pyqtSignal(dict)
    git_ready = pyqtSignal(dict)


class AgentModePanel(QWidget):
    """
    Agent Mode Panel for LUNA-ULTRA GUI.
    
    Features:
    - Goal input field
    - Plan preview panel
    - Step progress tracker
    - Retry counter
    - Current step display
    - Validation status
    - Git branch name
    - Push confirmation button
    """
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.signals = AgentModeSignals()
        
        # Initialize master orchestrator
        from core.master_orchestrator import MasterOrchestrator
        self.master_orchestrator = MasterOrchestrator(controller)
        self.master_orchestrator.set_mode("agent")
        
        self.current_plan = None
        self.current_branch = None
        
        self.setup_ui()
        self.setup_signal_connections()
        
        logging.info("AgentModePanel: Initialized.")
    
    def setup_ui(self):
        """Setup the Agent Mode UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("🤖 Agent Mode")
        header.setObjectName("Header")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #4F46E5;")
        layout.addWidget(header)
        
        # Description
        desc = QLabel("Structured autonomous execution with planning, validation, and safe Git operations.")
        desc.setStyleSheet("color: #9CA3AF; font-size: 13px;")
        layout.addWidget(desc)
        
        layout.addSpacing(10)
        
        # Goal Input Section
        goal_label = QLabel("Goal:")
        goal_label.setStyleSheet("font-weight: bold; color: #E0E0E6;")
        layout.addWidget(goal_label)
        
        self.goal_input = QTextEdit()
        self.goal_input.setPlaceholderText("Enter your goal here... (e.g., 'Add a new feature to export data as CSV')")
        self.goal_input.setMaximumHeight(80)
        self.goal_input.setObjectName("Panel")
        layout.addWidget(self.goal_input)
        
        # Generate Plan Button
        btn_layout = QHBoxLayout()
        self.generate_plan_btn = QPushButton("📋 Generate Plan")
        self.generate_plan_btn.setObjectName("PrimaryButton")
        self.generate_plan_btn.clicked.connect(self.generate_plan)
        btn_layout.addWidget(self.generate_plan_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Plan Preview Panel
        plan_label = QLabel("Execution Plan:")
        plan_label.setStyleSheet("font-weight: bold; color: #E0E0E6; margin-top: 10px;")
        layout.addWidget(plan_label)
        
        self.plan_display = QTextEdit()
        self.plan_display.setReadOnly(True)
        self.plan_display.setPlaceholderText("Plan will appear here after generation...")
        self.plan_display.setObjectName("Panel")
        self.plan_display.setStyleSheet("font-family: 'Consolas'; font-size: 11px;")
        layout.addWidget(self.plan_display)
        
        # Approval Buttons
        approval_layout = QHBoxLayout()
        self.approve_btn = QPushButton("✅ Approve & Execute")
        self.approve_btn.setObjectName("PrimaryButton")
        self.approve_btn.setEnabled(False)
        self.approve_btn.clicked.connect(self.approve_and_execute)
        approval_layout.addWidget(self.approve_btn)
        
        self.reject_btn = QPushButton("❌ Reject")
        self.reject_btn.setObjectName("SecondaryButton")
        self.reject_btn.setEnabled(False)
        self.reject_btn.clicked.connect(self.reject_plan)
        approval_layout.addWidget(self.reject_btn)
        
        approval_layout.addStretch()
        layout.addLayout(approval_layout)
        
        # Progress Section
        progress_label = QLabel("Execution Progress:")
        progress_label.setStyleSheet("font-weight: bold; color: #E0E0E6; margin-top: 10px;")
        layout.addWidget(progress_label)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #4F46E5;
                border-radius: 5px;
                text-align: center;
                background-color: #16161D;
                color: #E0E0E6;
            }
            QProgressBar::chunk {
                background-color: #4F46E5;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Status Info
        status_layout = QHBoxLayout()
        
        self.current_step_label = QLabel("Current Step: -")
        self.current_step_label.setStyleSheet("color: #9CA3AF; font-size: 12px;")
        status_layout.addWidget(self.current_step_label)
        
        self.retry_label = QLabel("Retries: 0")
        self.retry_label.setStyleSheet("color: #9CA3AF; font-size: 12px;")
        status_layout.addWidget(self.retry_label)
        
        self.validation_label = QLabel("Validation: Pending")
        self.validation_label.setStyleSheet("color: #9CA3AF; font-size: 12px;")
        status_layout.addWidget(self.validation_label)
        
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # Git Section
        git_label = QLabel("Git Operations:")
        git_label.setStyleSheet("font-weight: bold; color: #E0E0E6; margin-top: 10px;")
        layout.addWidget(git_label)
        
        self.git_info_label = QLabel("Branch: Not created yet")
        self.git_info_label.setStyleSheet("color: #9CA3AF; font-size: 12px;")
        layout.addWidget(self.git_info_label)
        
        self.push_btn = QPushButton("🚀 Push to GitHub")
        self.push_btn.setObjectName("PrimaryButton")
        self.push_btn.setEnabled(False)
        self.push_btn.clicked.connect(self.push_to_github)
        layout.addWidget(self.push_btn)
        
        layout.addStretch()
    
    def setup_signal_connections(self):
        """Setup signal connections."""
        self.signals.plan_generated.connect(self.on_plan_generated)
        self.signals.execution_finished.connect(self.on_execution_finished)
        self.signals.git_ready.connect(self.on_git_ready)
    
    def generate_plan(self):
        """Generate execution plan from goal."""
        goal = self.goal_input.toPlainText().strip()
        
        if not goal:
            QMessageBox.warning(self, "No Goal", "Please enter a goal before generating a plan.")
            return
        
        self.generate_plan_btn.setEnabled(False)
        self.plan_display.setText("🔄 Generating plan...")
        
        # Run plan generation in background
        threading.Thread(target=self._generate_plan_async, args=(goal,), daemon=True).start()
    
    def _generate_plan_async(self, goal: str):
        """Generate plan asynchronously."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(self.master_orchestrator.handle_agent_task(goal, user_approved=False))
            
            if result.get("success") and result.get("requires_approval"):
                self.current_plan = result.get("plan")
                self.signals.plan_generated.emit(result)
            else:
                error = result.get("error", "Unknown error")
                self.plan_display.setText(f"❌ Plan generation failed:\n{error}")
                self.generate_plan_btn.setEnabled(True)
                
        except Exception as e:
            logging.error(f"AgentModePanel: Error generating plan: {e}")
            self.plan_display.setText(f"❌ Error: {str(e)}")
            self.generate_plan_btn.setEnabled(True)
    
    def on_plan_generated(self, result: Dict[str, Any]):
        """Handle plan generation completion."""
        plan = result.get("plan")
        
        if plan:
            # Format and display plan
            formatted_plan = self.master_orchestrator.plan_engine.format_plan_for_display(plan)
            self.plan_display.setText(formatted_plan)
            
            # Enable approval buttons
            self.approve_btn.setEnabled(True)
            self.reject_btn.setEnabled(True)
            self.generate_plan_btn.setEnabled(True)
    
    def approve_and_execute(self):
        """Approve plan and start execution."""
        if not self.current_plan:
            QMessageBox.warning(self, "No Plan", "No plan to approve.")
            return
        
        # Confirm with user
        reply = QMessageBox.question(
            self,
            "Confirm Execution",
            f"Are you sure you want to execute this plan?\n\nRisk Level: {self.current_plan.get('risk_level')}\nComplexity: {self.current_plan.get('estimated_complexity')}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.approve_btn.setEnabled(False)
            self.reject_btn.setEnabled(False)
            self.generate_plan_btn.setEnabled(False)
            
            # Start execution
            threading.Thread(target=self._execute_plan_async, daemon=True).start()
    
    def _execute_plan_async(self):
        """Execute plan asynchronously."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            goal = self.current_plan.get("goal")
            result = loop.run_until_complete(self.master_orchestrator.handle_agent_task(goal, user_approved=True))
            
            self.signals.execution_finished.emit(result)
            
        except Exception as e:
            logging.error(f"AgentModePanel: Error executing plan: {e}")
            self.signals.execution_finished.emit({
                "success": False,
                "error": str(e)
            })
    
    def on_execution_finished(self, result: Dict[str, Any]):
        """Handle execution completion."""
        if result.get("success"):
            # Update progress
            total = result.get("total_steps", 0)
            completed = result.get("completed_steps", 0)
            self.progress_bar.setValue(100)
            self.current_step_label.setText(f"Current Step: Completed ({completed}/{total})")
            self.validation_label.setText("Validation: ✅ Passed")
            
            # Check if Git preparation is ready
            git_prep = result.get("git_preparation")
            if git_prep and git_prep.get("success"):
                self.signals.git_ready.emit(git_prep)
            
            QMessageBox.information(self, "Success", "Execution completed successfully!")
        else:
            error = result.get("error", "Unknown error")
            self.validation_label.setText("Validation: ❌ Failed")
            QMessageBox.critical(self, "Execution Failed", f"Execution failed:\n{error}")
        
        # Re-enable buttons
        self.generate_plan_btn.setEnabled(True)
    
    def on_git_ready(self, git_prep: Dict[str, Any]):
        """Handle Git preparation completion."""
        branch_name = git_prep.get("branch_name")
        self.current_branch = branch_name
        
        self.git_info_label.setText(f"Branch: {branch_name} (ready to push)")
        self.push_btn.setEnabled(True)
        
        # Show diff preview
        diff_preview = git_prep.get("diff_preview", "")
        commit_message = git_prep.get("commit_message", "")
        
        msg = f"Changes committed to branch: {branch_name}\n\n"
        msg += f"Commit Message:\n{commit_message}\n\n"
        msg += f"Diff Preview:\n{diff_preview}"
        
        QMessageBox.information(self, "Git Ready", msg)
    
    def push_to_github(self):
        """Push changes to GitHub after confirmation."""
        if not self.current_branch:
            QMessageBox.warning(self, "No Branch", "No branch to push.")
            return
        
        # Confirm with user
        reply = QMessageBox.question(
            self,
            "Confirm Push",
            f"Are you sure you want to push branch '{self.current_branch}' to GitHub?\n\nThis will upload all changes to the remote repository.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.push_btn.setEnabled(False)
            threading.Thread(target=self._push_to_github_async, daemon=True).start()
    
    def _push_to_github_async(self):
        """Push to GitHub asynchronously."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(self.master_orchestrator.push_to_github(self.current_branch))
            
            if result.get("success"):
                QMessageBox.information(self, "Success", f"Branch '{self.current_branch}' pushed successfully!")
                self.git_info_label.setText(f"Branch: {self.current_branch} (pushed ✅)")
            else:
                error = result.get("error", "Unknown error")
                QMessageBox.critical(self, "Push Failed", f"Failed to push branch:\n{error}")
                self.push_btn.setEnabled(True)
                
        except Exception as e:
            logging.error(f"AgentModePanel: Error pushing to GitHub: {e}")
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
            self.push_btn.setEnabled(True)
    
    def reject_plan(self):
        """Reject the current plan."""
        self.current_plan = None
        self.plan_display.clear()
        self.approve_btn.setEnabled(False)
        self.reject_btn.setEnabled(False)
        QMessageBox.information(self, "Plan Rejected", "Plan has been rejected. You can generate a new plan.")
