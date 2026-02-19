# Path: security/security_sentinel.py
import asyncio
import logging
import subprocess
import os
from typing import Any, List, Set

class SecuritySentinel:
    """
    LUNA-ULTRA Security Sentinel: Proactively monitors ports and logs.
    """
    def __init__(self, controller: Any):
        self.controller = controller
        self.config = controller.config.get("security", {}) if controller.config.get("security") else {}
        self.enabled = self.config.get("sentinel_enabled", True) if self.config else True
        self.interval = self.config.get("sentinel_interval", 30) # Seconds
        self.known_ports: Set[int] = set()
        self.running = False

    async def start(self):
        if not self.enabled: return
        self.running = True
        logging.info(f"SecuritySentinel: Started with interval {self.interval}s")
        # Initialize known ports
        self.known_ports = self.get_open_ports()
        
        while self.running:
            try:
                await self.scan_step()
            except Exception as e:
                logging.error(f"SecuritySentinel: Error during scan: {e}")
            await asyncio.sleep(self.interval)

    async def stop(self):
        self.running = False
        logging.info("SecuritySentinel: Stopped.")

    def get_open_ports(self) -> Set[int]:
        """Gets currently open TCP ports using netstat."""
        ports = set()
        try:
            # Hardened: Using list for subprocess to avoid shell=True
            p1 = subprocess.Popen(["netstat", "-tunlp"], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(["grep", "LISTEN"], stdin=p1.stdout, stdout=subprocess.PIPE)
            p1.stdout.close()
            output = p2.communicate()[0].decode()
            for line in output.splitlines():
                parts = line.split()
                if len(parts) > 3:
                    address = parts[3]
                    port = int(address.split(':')[-1])
                    ports.add(port)
        except Exception as e:
            logging.error(f"SecuritySentinel: Failed to get ports: {e}")
        return ports

    async def scan_step(self):
        # 1. Port Monitoring
        current_ports = self.get_open_ports()
        new_ports = current_ports - self.known_ports
        
        if new_ports:
            msg = f"🚨 SECURITY ALERT: New unauthorized port(s) detected: {new_ports}"
            logging.warning(msg)
            await self.notify(msg)
            # We don't automatically add to known_ports to keep alerting until user acknowledges
        
        # 2. Process Monitoring (Check for suspicious processes)
        await self.check_suspicious_processes()
        
        # 3. Log Monitoring (Simplified for demo, targets auth.log)
        if os.path.exists("/var/log/auth.log"):
            await self.check_auth_logs()

    async def check_suspicious_processes(self):
        """Checks for common suspicious process names or high resource usage."""
        import psutil
        suspicious_names = ["miner", "nc", "netcat", "nmap", "wireshark", "tcpdump"]
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                pinfo = proc.info
                if any(name in pinfo['name'].lower() for name in suspicious_names):
                    msg = f"🚨 SECURITY ALERT: Suspicious process detected: {pinfo['name']} (PID: {pinfo['pid']})"
                    await self.notify(msg)
                
                # High CPU usage alert (e.g., > 90%)
                if pinfo['cpu_percent'] > 90.0:
                    msg = f"⚠️ PERFORMANCE ALERT: High CPU usage by {pinfo['name']} (PID: {pinfo['pid']}): {pinfo['cpu_percent']}%"
                    await self.notify(msg)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    async def check_auth_logs(self):
        """Scans auth logs for suspicious login attempts."""
        try:
            # Hardened: Using list for subprocess to avoid shell=True
            p1 = subprocess.Popen(["tail", "-n", "10", "/var/log/auth.log"], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(["grep", "Failed password"], stdin=p1.stdout, stdout=subprocess.PIPE)
            p1.stdout.close()
            output = p2.communicate()[0].decode()
            if output:
                msg = "🚨 SECURITY ALERT: Multiple failed login attempts detected in auth.log!"
                await self.notify(msg)
        except subprocess.CalledProcessError:
            pass # No failed passwords found

    async def notify(self, message: str):
        if hasattr(self.controller, 'gui') and self.controller.gui:
            self.controller.gui.update_activity(f"🛡️ {message}")
        
        if self.controller.telegram and self.controller.telegram.enabled:
            await self.controller.telegram.send_notification(message)
