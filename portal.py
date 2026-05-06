"""
Wednesday AI Assistant - Web Portal
Run with: .venv\\Scripts\\python.exe portal.py
Then open: http://localhost:5000
"""
import os
import sys
import json
import asyncio
import threading
import tempfile
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response, send_file

os.environ["PYTHONUTF8"] = "1"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assistant.core import WednesdayCore
from assistant.logger import setup_logger

logger = setup_logger(__name__)

app = Flask(__name__)
app.secret_key = "wednesday-portal-secret"

# Single shared core instance
core = WednesdayCore()
print("\n[Wednesday Portal] Ready at http://localhost:5000\n")


@app.route("/")
def index():
    return render_template("portal.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = (data.get("message") or "").strip()
    if not user_input:
        return jsonify({"error": "empty message"}), 400

    try:
        response, skill_results = core.process_input(user_input)
        skills_display = []
        for r in skill_results:
            skills_display.append({
                "skill": r.get("skill", ""),
                "status": r.get("status", ""),
                "result": str(r.get("result", r.get("error", "")))[:1200],
            })
        return jsonify({
            "response": response,
            "skills": skills_display,
            "timestamp": datetime.now().strftime("%I:%M %p"),
        })
    except Exception as e:
        logger.error(f"Portal chat error: {e}")
        return jsonify({"response": f"Something broke: {e}", "skills": []}), 500


@app.route("/api/status")
def status():
    """Live system stats for the sidebar."""
    try:
        import psutil, platform
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory()
        disk_path = "C:\\" if platform.system() == "Windows" else "/"
        disk = psutil.disk_usage(disk_path)

        # Get what user is working on
        try:
            working_on = core.skills.execute("daily_tracker", {"action": "get_working_on"})
        except Exception:
            working_on = "Not set"

        # Get current mood
        try:
            mood_data = core.memory.get_mood()
            mood = mood_data.get("mood", "") if mood_data else ""
        except Exception:
            mood = ""

        return jsonify({
            "cpu": round(cpu, 1),
            "memory": round(mem.percent, 1),
            "memory_free_gb": round(mem.available / (1024**3), 1),
            "disk": round(disk.percent, 1),
            "working_on": working_on,
            "mood": mood,
            "time": datetime.now().strftime("%I:%M %p"),
            "date": datetime.now().strftime("%A, %B %d"),
            "messages": core.memory.get_summary().get("messages", 0),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/today")
def today():
    """Today's activity summary."""
    try:
        summary = core.skills.execute("daily_tracker", {"action": "summary"})
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"summary": f"Error: {e}"}), 500


@app.route("/api/project-status")
def project_status():
    """Return loaded project info for the sidebar."""
    try:
        from pathlib import Path
        import json
        pf = Path(__file__).parent / "assistant_workspace" / "loaded_project.json"
        if pf.exists():
            data = json.loads(pf.read_text(encoding="utf-8"))
            return jsonify({"loaded": True, "name": data.get("name","?"), "files": data.get("file_count", 0)})
        return jsonify({"loaded": False})
    except Exception as e:
        return jsonify({"loaded": False, "error": str(e)})


@app.route("/api/speak", methods=["POST"])
def speak():
    """Convert text to speech using edge-tts and return MP3."""
    data = request.get_json()
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "no text"}), 400

    try:
        import edge_tts

        async def _synth(t, path):
            communicate = edge_tts.Communicate(t, voice="en-US-JennyNeural")
            await communicate.save(path)

        tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tmp.close()
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(_synth(text, tmp.name))
        finally:
            loop.close()
        return send_file(tmp.name, mimetype="audio/mpeg", as_attachment=False)
    except Exception as e:
        logger.error(f"TTS error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
