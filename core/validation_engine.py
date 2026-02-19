# Path: core/validation_engine.py
import logging
import os
import py_compile
import subprocess
from typing import Dict, Any, List


class ValidationEngine:
    """
    Validation Engine for Agent Mode.
    Validates project integrity, compilation, and dependencies.
    """
    
    def __init__(self, controller):
        self.controller = controller
        self.project_root = os.getcwd()
        logging.info("ValidationEngine: Initialized.")
    
    async def validate_project(self) -> Dict[str, Any]:
        """
        Perform comprehensive project validation.
        
        Steps:
        1. Compile all Python files
        2. Check for syntax errors
        3. Detect missing dependencies
        4. Validate expected files exist
        5. Generate validation report
        """
        
        logging.info("ValidationEngine: Starting project validation...")
        
        validation_results = {
            "success": True,
            "errors": [],
            "warnings": [],
            "compilation": None,
            "dependencies": None,
            "file_check": None
        }
        
        # Step 1: Compile entire project
        compile_result = await self.compile_project()
        validation_results["compilation"] = compile_result
        
        if not compile_result.get("success"):
            validation_results["success"] = False
            validation_results["errors"].extend(compile_result.get("errors", []))
        
        # Step 2: Check dependencies
        deps_result = await self.check_dependencies()
        validation_results["dependencies"] = deps_result
        
        if not deps_result.get("success"):
            validation_results["warnings"].extend(deps_result.get("warnings", []))
        
        # Step 3: Validate critical files exist
        file_check_result = self.validate_critical_files()
        validation_results["file_check"] = file_check_result
        
        if not file_check_result.get("success"):
            validation_results["success"] = False
            validation_results["errors"].extend(file_check_result.get("errors", []))
        
        logging.info(f"ValidationEngine: Validation {'passed' if validation_results['success'] else 'failed'}.")
        
        return validation_results
    
    async def compile_project(self) -> Dict[str, Any]:
        """
        Compile all Python files in the project.
        """
        logging.info("ValidationEngine: Compiling project...")
        
        errors = []
        compiled_files = []
        
        # Find all Python files
        python_files = []
        for root, dirs, files in os.walk(self.project_root):
            # Skip __pycache__ and .git directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'env', 'node_modules']]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        # Compile each file
        for py_file in python_files:
            try:
                py_compile.compile(py_file, doraise=True)
                compiled_files.append(py_file)
            except py_compile.PyCompileError as e:
                error_msg = f"Compilation error in {py_file}: {e.msg}"
                errors.append(error_msg)
                logging.error(error_msg)
        
        if errors:
            return {
                "success": False,
                "errors": errors,
                "compiled_files": compiled_files,
                "total_files": len(python_files)
            }
        
        return {
            "success": True,
            "compiled_files": compiled_files,
            "total_files": len(python_files)
        }
    
    async def check_dependencies(self) -> Dict[str, Any]:
        """
        Check for missing dependencies.
        """
        logging.info("ValidationEngine: Checking dependencies...")
        
        warnings = []
        missing_deps = []
        
        # Check if requirements.txt exists
        req_files = [
            "requirements.txt",
            "requirements-core.txt",
            "requirements-automation.txt",
            "requirements-vision.txt",
            "requirements-voice.txt"
        ]
        
        all_requirements = set()
        
        for req_file in req_files:
            req_path = os.path.join(self.project_root, req_file)
            if os.path.exists(req_path):
                try:
                    with open(req_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                # Extract package name (before ==, >=, etc.)
                                pkg_name = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                                all_requirements.add(pkg_name)
                except Exception as e:
                    warnings.append(f"Failed to read {req_file}: {e}")
        
        # Try to import each requirement
        for pkg in all_requirements:
            try:
                __import__(pkg.replace('-', '_'))
            except ImportError:
                missing_deps.append(pkg)
                warnings.append(f"Missing dependency: {pkg}")
        
        if missing_deps:
            return {
                "success": False,
                "warnings": warnings,
                "missing_dependencies": missing_deps
            }
        
        return {
            "success": True,
            "warnings": warnings,
            "checked_dependencies": len(all_requirements)
        }
    
    def validate_critical_files(self) -> Dict[str, Any]:
        """
        Validate that critical files exist.
        """
        logging.info("ValidationEngine: Validating critical files...")
        
        critical_files = [
            "app/main.py",
            "core/controller.py",
            "core/orchestrator.py",
            "core/master_orchestrator.py",
            "core/plan_engine.py",
            "core/execution_state.py",
            "core/validation_engine.py"
        ]
        
        errors = []
        
        for file_path in critical_files:
            full_path = os.path.join(self.project_root, file_path)
            if not os.path.exists(full_path):
                error_msg = f"Critical file missing: {file_path}"
                errors.append(error_msg)
                logging.error(error_msg)
        
        if errors:
            return {
                "success": False,
                "errors": errors
            }
        
        return {
            "success": True,
            "validated_files": len(critical_files)
        }
    
    def generate_validation_report(self, validation_results: Dict[str, Any]) -> str:
        """
        Generate a human-readable validation report.
        """
        report = []
        report.append("=" * 60)
        report.append("VALIDATION REPORT")
        report.append("=" * 60)
        report.append(f"\nOVERALL STATUS: {'PASSED' if validation_results.get('success') else 'FAILED'}")
        report.append("\n" + "-" * 60)
        
        # Compilation results
        compilation = validation_results.get("compilation", {})
        report.append(f"\nCOMPILATION:")
        report.append(f"  Status: {'PASSED' if compilation.get('success') else 'FAILED'}")
        report.append(f"  Files Compiled: {compilation.get('compiled_files', 0)}/{compilation.get('total_files', 0)}")
        
        if compilation.get("errors"):
            report.append(f"  Errors: {len(compilation.get('errors'))}")
            for error in compilation.get("errors", [])[:5]:  # Show first 5 errors
                report.append(f"    - {error}")
        
        # Dependencies results
        dependencies = validation_results.get("dependencies", {})
        report.append(f"\nDEPENDENCIES:")
        report.append(f"  Status: {'OK' if dependencies.get('success') else 'WARNINGS'}")
        
        if dependencies.get("missing_dependencies"):
            report.append(f"  Missing: {', '.join(dependencies.get('missing_dependencies'))}")
        
        # File check results
        file_check = validation_results.get("file_check", {})
        report.append(f"\nFILE VALIDATION:")
        report.append(f"  Status: {'PASSED' if file_check.get('success') else 'FAILED'}")
        
        if file_check.get("errors"):
            for error in file_check.get("errors", []):
                report.append(f"    - {error}")
        
        # Summary
        report.append("\n" + "-" * 60)
        report.append(f"\nTOTAL ERRORS: {len(validation_results.get('errors', []))}")
        report.append(f"TOTAL WARNINGS: {len(validation_results.get('warnings', []))}")
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)
