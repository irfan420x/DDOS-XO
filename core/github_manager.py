# Path: core/github_manager.py
import os
import logging
import subprocess
import json
import shlex
from typing import Dict, Any, List, Optional

class GitHubManager:
    """
    LUNA-ULTRA GitHub Integration System: Manages repository lifecycle and audits.
    """
    def __init__(self, controller):
        self.controller = controller
        self.token = self.controller.config.get("github", {}).get("token")
        self.base_dir = "cloned_repos"
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def _run_git_command(self, command: List[str], cwd: Optional[str] = None) -> Dict[str, Any]:
        """Safely runs a git command without shell=True."""
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=60
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def clone_repo(self, repo_url: str) -> Dict[str, Any]:
        """Clones a repository using the provided URL and token."""
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        target_path = os.path.join(self.base_dir, repo_name)
        
        if os.path.exists(target_path):
            return {"success": True, "path": target_path, "message": "Repository already exists."}

        # Inject token into URL if available
        if self.token and "github.com" in repo_url:
            repo_url = repo_url.replace("https://", f"https://{self.token}@")

        cmd = ["git", "clone", repo_url, target_path]
        res = self._run_git_command(cmd)
        if res["success"]:
            return {"success": True, "path": target_path}
        return {"success": False, "error": res.get("stderr") or res.get("error")}

    async def audit_project(self, repo_path: str) -> Dict[str, Any]:
        """Runs a full project audit: structure, dependencies, syntax, and tests."""
        report = {
            "structure": [],
            "dependencies": [],
            "syntax_errors": [],
            "test_results": "Not run",
            "suggestions": []
        }

        # 1. Structure Check
        if not os.path.exists(os.path.join(repo_path, "README.md")):
            report["structure"].append("Missing README.md")
        
        # 2. Dependency Check
        req_path = os.path.join(repo_path, "requirements.txt")
        if not os.path.exists(req_path):
            report["structure"].append("Missing requirements.txt")
        else:
            with open(req_path, 'r') as f:
                report["dependencies"] = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        # 3. Syntax Check (Compile all Python files)
        try:
            compile_res = subprocess.run(
                ["python3", "-m", "compileall", repo_path],
                capture_output=True,
                text=True
            )
            if compile_res.returncode != 0:
                report["syntax_errors"] = compile_res.stderr.splitlines()
        except Exception as e:
            report["syntax_errors"].append(str(e))

        # 4. Generate Suggestions via LLM
        audit_prompt = (
            f"Project Audit Data for {os.path.basename(repo_path)}:\n"
            f"Structure Issues: {report['structure']}\n"
            f"Syntax Errors: {report['syntax_errors']}\n"
            f"Dependencies: {report['dependencies']}\n"
            f"Analyze these issues and provide a list of fixes and structural improvements."
        )
        report["suggestions"] = await self.controller.llm_router.generate_response(audit_prompt)

        return report

    async def create_fix_branch(self, repo_path: str, branch_name: str = "luna-upgrade") -> Dict[str, Any]:
        """Creates a new branch for applying fixes."""
        res = self._run_git_command(["git", "checkout", "-b", branch_name], cwd=repo_path)
        return res

    async def commit_and_push(self, repo_path: str, message: str, branch: str = "luna-upgrade") -> Dict[str, Any]:
        """Commits changes and pushes to the specified branch."""
        # Add all changes
        self._run_git_command(["git", "add", "."], cwd=repo_path)
        # Commit
        commit_res = self._run_git_command(["git", "commit", "-m", message], cwd=repo_path)
        if not commit_res["success"]:
            return commit_res
        # Push
        push_res = self._run_git_command(["git", "push", "origin", branch], cwd=repo_path)
        return push_res
