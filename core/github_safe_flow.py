# Path: core/github_safe_flow.py
import logging
import os
import subprocess
from typing import Dict, Any, List
from datetime import datetime


class GitHubSafeFlow:
    """
    GitHub Safe Flow for Agent Mode.
    Ensures safe Git operations with user confirmation.
    
    Features:
    - Create new branch with timestamp
    - Commit changes with summary
    - Show diff preview
    - Require user confirmation before push
    - Never auto-merge
    - Respect .gitignore
    """
    
    def __init__(self, controller):
        self.controller = controller
        self.project_root = os.getcwd()
        self.branch_prefix = "luna-agent"
        logging.info("GitHubSafeFlow: Initialized.")
    
    def create_agent_branch(self) -> Dict[str, Any]:
        """
        Create a new branch for agent changes.
        Format: luna-agent-<timestamp>
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            branch_name = f"{self.branch_prefix}-{timestamp}"
            
            # Create and checkout new branch
            result = subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logging.info(f"GitHubSafeFlow: Created branch '{branch_name}'")
                return {
                    "success": True,
                    "branch_name": branch_name
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to create branch: {result.stderr}"
                }
                
        except Exception as e:
            logging.error(f"GitHubSafeFlow: Error creating branch: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_changed_files(self) -> Dict[str, Any]:
        """
        Get list of changed files.
        """
        try:
            # Get status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                changed_files = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        # Parse git status output
                        status = line[:2]
                        file_path = line[3:]
                        changed_files.append({
                            "status": status.strip(),
                            "path": file_path
                        })
                
                return {
                    "success": True,
                    "changed_files": changed_files,
                    "count": len(changed_files)
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }
                
        except Exception as e:
            logging.error(f"GitHubSafeFlow: Error getting changed files: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def stage_changes(self, files: List[str] = None) -> Dict[str, Any]:
        """
        Stage changes for commit.
        Respects .gitignore and excludes sensitive files.
        """
        try:
            # Files to always exclude
            exclude_patterns = [
                "__pycache__",
                "*.pyc",
                ".env",
                "*.db",
                "agent_execution_state.json",
                "*.log"
            ]
            
            if files:
                # Stage specific files
                for file in files:
                    # Check if file should be excluded
                    should_exclude = any(pattern in file for pattern in exclude_patterns)
                    
                    if not should_exclude:
                        result = subprocess.run(
                            ["git", "add", file],
                            cwd=self.project_root,
                            capture_output=True,
                            text=True
                        )
                        
                        if result.returncode != 0:
                            logging.warning(f"GitHubSafeFlow: Failed to stage {file}: {result.stderr}")
            else:
                # Stage all changes (respecting .gitignore)
                result = subprocess.run(
                    ["git", "add", "-A"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    return {
                        "success": False,
                        "error": result.stderr
                    }
            
            return {
                "success": True,
                "message": "Changes staged successfully."
            }
            
        except Exception as e:
            logging.error(f"GitHubSafeFlow: Error staging changes: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def commit_changes(self, message: str, description: str = "") -> Dict[str, Any]:
        """
        Commit staged changes with message.
        """
        try:
            commit_msg = message
            if description:
                commit_msg += f"\n\n{description}"
            
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logging.info(f"GitHubSafeFlow: Changes committed: {message}")
                return {
                    "success": True,
                    "message": "Changes committed successfully.",
                    "commit_output": result.stdout
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }
                
        except Exception as e:
            logging.error(f"GitHubSafeFlow: Error committing changes: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_diff_preview(self) -> Dict[str, Any]:
        """
        Get diff preview of staged changes.
        """
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--stat"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "diff_stat": result.stdout
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }
                
        except Exception as e:
            logging.error(f"GitHubSafeFlow: Error getting diff: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def push_branch(self, branch_name: str, force: bool = False) -> Dict[str, Any]:
        """
        Push branch to remote.
        Should only be called after user confirmation.
        """
        try:
            cmd = ["git", "push", "origin", branch_name]
            if force:
                cmd.append("--force")
            
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logging.info(f"GitHubSafeFlow: Branch '{branch_name}' pushed to remote.")
                return {
                    "success": True,
                    "message": f"Branch '{branch_name}' pushed successfully.",
                    "output": result.stdout
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }
                
        except Exception as e:
            logging.error(f"GitHubSafeFlow: Error pushing branch: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_commit_summary(self, execution_results: Dict[str, Any]) -> str:
        """
        Generate commit summary from execution results.
        """
        summary_lines = []
        
        summary_lines.append("Agent Mode: Automated changes")
        summary_lines.append("")
        
        # Add goal
        goal = execution_results.get("goal", "N/A")
        summary_lines.append(f"Goal: {goal}")
        summary_lines.append("")
        
        # Add steps summary
        completed_steps = execution_results.get("completed_steps", 0)
        total_steps = execution_results.get("total_steps", 0)
        summary_lines.append(f"Completed: {completed_steps}/{total_steps} steps")
        summary_lines.append("")
        
        # Add changed files
        changed_files = self.get_changed_files()
        if changed_files.get("success"):
            summary_lines.append("Changed files:")
            for file_info in changed_files.get("changed_files", [])[:10]:  # First 10 files
                summary_lines.append(f"  - {file_info.get('path')}")
        
        return "\n".join(summary_lines)
    
    def prepare_for_push(self, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare changes for push with full workflow.
        
        Steps:
        1. Create new branch
        2. Stage changes
        3. Commit with summary
        4. Get diff preview
        5. Return info for user confirmation
        """
        
        # Step 1: Create branch
        branch_result = self.create_agent_branch()
        if not branch_result.get("success"):
            return branch_result
        
        branch_name = branch_result.get("branch_name")
        
        # Step 2: Get changed files
        changed_files_result = self.get_changed_files()
        if not changed_files_result.get("success"):
            return changed_files_result
        
        # Step 3: Stage changes
        stage_result = self.stage_changes()
        if not stage_result.get("success"):
            return stage_result
        
        # Step 4: Generate commit message
        commit_message = self.generate_commit_summary(execution_results)
        
        # Step 5: Commit changes
        commit_result = self.commit_changes(
            "Agent Mode: Automated changes",
            commit_message
        )
        if not commit_result.get("success"):
            return commit_result
        
        # Step 6: Get diff preview
        diff_result = self.get_diff_preview()
        
        return {
            "success": True,
            "branch_name": branch_name,
            "changed_files": changed_files_result.get("changed_files", []),
            "commit_message": commit_message,
            "diff_preview": diff_result.get("diff_stat", ""),
            "ready_to_push": True,
            "requires_confirmation": True
        }
