# Path: security/audit_logger.py
import logging
import os

class AuditLogger:
    """
    LUNA-ULTRA Audit Logger: Security logging for all actions.
    """
    def __init__(self, log_file: str = "logs/audit.log"):
        self.log_file = log_file
        self.setup_logger()

    def setup_logger(self):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def log_action(self, action: str, details: str, status: str):
        logging.info(f"Action: {action} | Details: {details} | Status: {status}")

    def log_warning(self, message: str):
        logging.warning(message)
