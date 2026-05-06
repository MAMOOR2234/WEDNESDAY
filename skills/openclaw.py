"""OpenClaw gateway bridge skill for Wednesday."""

import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
import sys

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    """Connect Wednesday to a local OpenClaw gateway."""

    name = "OpenClaw Bridge"
    description = "Query and invoke the local OpenClaw gateway"

    def __init__(self):
        self.config_path = Path.home() / ".openclaw" / "openclaw.json"
        self.gateway_url, self.gateway_token = self._load_gateway_config()

    def execute(self, args):
        """Execute an OpenClaw gateway action."""
        action = args.get("action", "status")

        if action == "status":
            return self.get_status()
        if action == "health":
            return self.invoke_tool("health")
        if action == "search":
            query = args.get("query", "").strip()
            if not query:
                return "OpenClaw search query is required"
            return self.invoke_tool("ollama_web_search", tool_args={"query": query})
        if action == "fetch":
            url = args.get("url", "").strip()
            if not url:
                return "OpenClaw fetch URL is required"
            return self.invoke_tool("ollama_web_fetch", tool_args={"url": url})
        if action == "send":
            message = args.get("message", "").strip()
            if not message:
                return "OpenClaw send message is required"
            return self.send_message(
                message=message,
                target=args.get("target"),
                channel=args.get("channel"),
                agent=args.get("agent"),
                session_id=args.get("session_id"),
                deliver=bool(args.get("deliver", False)),
            )
        if action == "invoke":
            tool = args.get("tool")
            if not tool:
                return "OpenClaw tool name is required"
            return self.invoke_tool(
                tool,
                tool_action=args.get("tool_action"),
                tool_args=args.get("tool_args", {}),
                session_key=args.get("sessionKey", "main"),
                dry_run=bool(args.get("dryRun", False)),
            )
        if action == "info":
            return self.get_gateway_info()

        return f"Unknown OpenClaw action: {action}"

    def _load_gateway_config(self):
        """Load the local OpenClaw gateway URL and token."""
        gateway_url = os.getenv("OPENCLAW_GATEWAY_URL")
        gateway_token = os.getenv("OPENCLAW_GATEWAY_TOKEN")

        if self.config_path.exists():
            try:
                config = json.loads(self.config_path.read_text(encoding="utf-8"))
                gateway = config.get("gateway", {})

                if not gateway_url:
                    port = gateway.get("port", 18789)
                    gateway_url = f"http://127.0.0.1:{port}"

                if not gateway_token:
                    gateway_token = gateway.get("auth", {}).get("token")
            except Exception:
                pass

        if not gateway_url:
            gateway_url = "http://127.0.0.1:18789"

        return gateway_url.rstrip("/"), gateway_token

    def _request(self, path, payload=None):
        """Send an authenticated request to the gateway."""
        if not self.gateway_token:
            return {"ok": False, "error": "OpenClaw token not found in ~/.openclaw/openclaw.json"}

        url = f"{self.gateway_url}{path}"
        data = None
        headers = {
            "Authorization": f"Bearer {self.gateway_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if payload is not None:
            data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                body = response.read().decode("utf-8")
                if not body:
                    return {"ok": True, "result": None}
                return json.loads(body)
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            return {"ok": False, "error": f"HTTP {error.code}: {body}"}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def invoke_tool(self, tool, tool_action=None, tool_args=None, session_key="main", dry_run=False):
        """Invoke a single OpenClaw gateway tool."""
        payload = {
            "tool": tool,
            "args": tool_args or {},
            "sessionKey": session_key,
            "dryRun": dry_run,
        }

        if tool_action:
            payload["action"] = tool_action

        result = self._request("/tools/invoke", payload)
        return json.dumps(result, indent=2, ensure_ascii=False)

    def get_status(self):
        """Check whether the OpenClaw gateway is reachable."""
        request = urllib.request.Request(self.gateway_url, method="GET")

        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                body = response.read().decode("utf-8", errors="replace")
                preview = body[:240].strip()
                payload = {
                    "ok": True,
                    "gateway_url": self.gateway_url,
                    "http_status": response.status,
                    "token_present": bool(self.gateway_token),
                    "preview": preview,
                }
        except Exception as error:
            payload = {
                "ok": False,
                "gateway_url": self.gateway_url,
                "token_present": bool(self.gateway_token),
                "error": str(error),
            }

        return json.dumps(payload, indent=2, ensure_ascii=False)

    def get_gateway_info(self):
        """Return the discovered OpenClaw gateway connection details."""
        info = {
            "gateway_url": self.gateway_url,
            "config_path": str(self.config_path),
            "token_present": bool(self.gateway_token),
        }
        return json.dumps(info, indent=2, ensure_ascii=False)

    def send_message(self, message, target=None, channel=None, agent=None, session_id=None, deliver=False):
        """Send a message through OpenClaw CLI agent command."""
        node_exe = Path("C:/Program Files/nodejs/node.exe")
        cli_mjs = Path.home() / "AppData" / "Roaming" / "npm" / "node_modules" / "openclaw" / "openclaw.mjs"

        if not node_exe.exists() or not cli_mjs.exists():
            return json.dumps(
                {
                    "ok": False,
                    "error": "OpenClaw CLI runtime not found (node or openclaw.mjs missing)",
                },
                indent=2,
                ensure_ascii=False,
            )

        cmd = [
            str(node_exe),
            str(cli_mjs),
            "agent",
            "--message",
            message,
            "--json",
        ]

        if not target and not agent and not session_id:
            return json.dumps(
                {
                    "ok": False,
                    "error": "Provide a target, agent, or session_id. Example: openclaw send to +1234567890: hello",
                },
                indent=2,
                ensure_ascii=False,
            )

        if target:
            cmd.extend(["--to", str(target), "--deliver"])
        if agent:
            cmd.extend(["--agent", str(agent)])
        if session_id:
            cmd.extend(["--session-id", str(session_id)])
        if channel:
            cmd.extend(["--reply-channel", str(channel), "--deliver"])
        if deliver and "--deliver" not in cmd:
            cmd.append("--deliver")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        except Exception as error:
            return json.dumps({"ok": False, "error": str(error)}, indent=2, ensure_ascii=False)

        output = (result.stdout or "").strip()
        error_output = (result.stderr or "").strip()
        response = {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": output,
            "stderr": error_output,
        }
        return json.dumps(response, indent=2, ensure_ascii=False)