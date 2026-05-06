"""System information skill for Wednesday."""

import platform
import subprocess
import sys

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    """Get system information."""

    name = "System Info"
    description = "Get system information and status"

    def execute(self, args):
        """Execute system info command."""
        query = args.get("query", "status")

        if query == "status":
            return self._get_system_status()
        elif query == "processes":
            return self._get_running_processes()
        elif query == "disk":
            return self._get_disk_info()
        else:
            return f"Unknown query: {query}"

    def _get_system_status(self):
        """Get overall system status."""
        try:
            import psutil

            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk_path = "C:\\" if platform.system() == "Windows" else "/"
            disk = psutil.disk_usage(disk_path)

            return f"""System Status:
- CPU: {cpu_usage}%
- Memory: {memory.percent}% ({memory.available / (1024**3):.1f}GB free)
- Disk: {disk.percent}% used
- Platform: {platform.system()} {platform.release()}"""

        except ImportError:
            return "psutil not installed (pip install psutil for system info)"
        except Exception as e:
            return f"System status error: {e}"

    def _get_running_processes(self):
        """Get top running processes."""
        try:
            import psutil

            processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
            top_procs = sorted(processes, key=lambda p: p.info['cpu_percent'], reverse=True)[:5]

            result = "Top processes:\n"
            for proc in top_procs:
                result += f"- {proc.info['name']}: {proc.info['cpu_percent']}% CPU\n"

            return result
        except Exception as e:
            return f"Process list error: {e}"

    def _get_disk_info(self):
        """Get disk information."""
        try:
            import psutil

            disk_path = "C:\\" if platform.system() == "Windows" else "/"
            disk = psutil.disk_usage(disk_path)
            return f"""Disk Info:
- Total: {disk.total / (1024**3):.1f}GB
- Used: {disk.used / (1024**3):.1f}GB
- Free: {disk.free / (1024**3):.1f}GB
- Usage: {disk.percent}%"""

        except Exception as e:
            return f"Disk info error: {e}"
