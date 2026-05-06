"""Desktop notification skill - Windows toast notifications."""

import subprocess
import sys

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    name = "Notifications"
    description = "Send Windows desktop toast notifications"

    def execute(self, args):
        title = args.get("title", "Wednesday")
        message = args.get("message", "")
        if not message:
            return "No message provided"
        return self._toast(title, message)

    def _toast(self, title, message):
        try:
            # Use PowerShell BurntToast / fallback to msg command
            ps = f"""
Add-Type -AssemblyName System.Windows.Forms
$notify = New-Object System.Windows.Forms.NotifyIcon
$notify.Icon = [System.Drawing.SystemIcons]::Information
$notify.Visible = $true
$notify.ShowBalloonTip(4000, '{title}', '{message}', [System.Windows.Forms.ToolTipIcon]::Info)
Start-Sleep -Seconds 4
$notify.Dispose()
"""
            subprocess.Popen(
                ["powershell", "-WindowStyle", "Hidden", "-Command", ps],
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            return f"Notification sent: {message}"
        except Exception as e:
            return f"Notification failed: {e}"
