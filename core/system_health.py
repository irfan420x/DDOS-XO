# Path: core/system_health.py
import psutil
import logging
from typing import Dict, Any, List, Optional

class SystemHealth:
    """
    LUNA-ULTRA System Health: Predictive maintenance and hardware monitoring.
    """
    def __init__(self, controller):
        self.controller = controller
        self.thresholds = {
            "cpu_percent": 85.0,
            "memory_percent": 90.0,
            "disk_percent": 95.0,
            "temp_celsius": 80.0
        }

    def get_status(self) -> Dict[str, Any]:
        """
        Collects current system health metrics.
        """
        status = {
            "cpu": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "battery": psutil.sensors_battery().percent if hasattr(psutil, "sensors_battery") and psutil.sensors_battery() else None,
            "temp": self._get_cpu_temp()
        }
        return status

    def _get_cpu_temp(self) -> Optional[float]:
        """
        Attempts to get CPU temperature (platform dependent).
        """
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if "coretemp" in temps:
                    return temps["coretemp"][0].current
                elif "cpu_thermal" in temps:
                    return temps["cpu_thermal"][0].current
            return None
        except Exception:
            return None

    async def check_health(self) -> List[str]:
        """
        Checks for potential hardware or performance issues.
        """
        status = self.get_status()
        alerts = []
        
        if status["cpu"] > self.thresholds["cpu_percent"]:
            alerts.append(f"⚠️ High CPU usage detected: {status['cpu']}%")
        
        if status["memory"] > self.thresholds["memory_percent"]:
            alerts.append(f"⚠️ Critical memory usage: {status['memory']}%")
            
        if status["temp"] and status["temp"] > self.thresholds["temp_celsius"]:
            alerts.append(f"🔥 CPU Temperature is high: {status['temp']}°C. Consider cooling down.")
            
        if status["disk"] > self.thresholds["disk_percent"]:
            alerts.append(f"💾 Disk space is almost full: {status['disk']}%")
            
        return alerts

    async def predictive_maintenance(self) -> str:
        """
        Analyzes system trends and provides maintenance suggestions.
        """
        status = self.get_status()
        prompt = (
            f"System Health Data: {json.dumps(status)}\n"
            f"As LUNA-ULTRA, analyze this data and provide a brief predictive maintenance report for IRFAN.\n"
            f"Suggest actions if any metrics are concerning."
        )
        import json
        return await self.controller.llm_router.generate_response(prompt)
