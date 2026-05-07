"""
Wednesday AI — Full JARVIS-style GUI
Iron Man inspired HUD interface
"""

import sys
import math
import threading
import queue
import html
from datetime import datetime

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTextEdit, QPushButton, QLabel, QLineEdit, QSizePolicy
    )
    from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QRectF, QPointF
    from PyQt6.QtGui import (
        QPainter, QColor, QPen, QFont, QBrush, QRadialGradient,
        QPainterPath, QLinearGradient
    )
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6"], check=True)
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTextEdit, QPushButton, QLabel, QLineEdit, QSizePolicy
    )
    from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QRectF, QPointF
    from PyQt6.QtGui import (
        QPainter, QColor, QPen, QFont, QBrush, QRadialGradient,
        QPainterPath, QLinearGradient
    )

# ── Palette ───────────────────────────────────────────────────────────────────
BG       = "#05050f"
CYAN     = QColor(0,  210, 255)
CYAN2    = QColor(0,  160, 220)
CYAN_DIM = QColor(0,   80, 120)
GREEN    = QColor(0,  255, 136)
ORANGE   = QColor(255, 160,  0)
RED_C    = QColor(255,  60, 60)
WHITE    = QColor(220, 230, 255)


# ── Animated reactor widget ───────────────────────────────────────────────────
class ReactorWidget(QWidget):
    """Iron Man arc reactor animation."""

    def __init__(self):
        super().__init__()
        self.setMinimumSize(260, 260)
        self._a1 = 0.0     # outer ring rotation
        self._a2 = 0.0     # inner ring counter-rotation
        self._pulse = 0.0  # speaking pulse 0-1
        self._pdir  = 1
        self._speaking = False
        self._flash = 0    # clap flash countdown

        t = QTimer(self)
        t.timeout.connect(self._tick)
        t.start(18)        # ~55 fps

    def set_speaking(self, on: bool):
        self._speaking = on

    def flash_clap(self):
        self._flash = 18

    def _tick(self):
        self._a1 = (self._a1 + 1.2) % 360
        self._a2 = (self._a2 - 0.7) % 360
        if self._speaking:
            self._pulse += 0.06 * self._pdir
            if self._pulse >= 1.0:
                self._pulse, self._pdir = 1.0, -1
            elif self._pulse <= 0.0:
                self._pulse, self._pdir = 0.0, 1
        else:
            self._pulse = max(0.0, self._pulse - 0.04)
        if self._flash > 0:
            self._flash -= 1
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor(BG))

        cx = self.width()  / 2
        cy = self.height() / 2
        R  = min(cx, cy) - 12

        # Clap flash
        if self._flash > 0:
            alpha = int(180 * self._flash / 18)
            p.fillRect(self.rect(), QColor(0, 210, 255, alpha))

        # Static glow halos
        for i, (r, a) in enumerate([(R, 25), (R-14, 35), (R-28, 50)]):
            p.setPen(QPen(QColor(0, 210, 255, a), 1))
            p.drawEllipse(QPointF(cx, cy), r, r)

        # Outer rotating arc segments
        p.save()
        p.translate(cx, cy)
        p.rotate(self._a1)
        pen = QPen(CYAN, 3)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        rect_o = QRectF(-(R-4), -(R-4), (R-4)*2, (R-4)*2)
        for i in range(8):
            p.save()
            p.rotate(i * 45)
            p.drawArc(rect_o, 4*16, 22*16)
            p.restore()
        p.restore()

        # Middle counter-rotating ring
        p.save()
        p.translate(cx, cy)
        p.rotate(self._a2)
        p.setPen(QPen(CYAN2, 2))
        rect_m = QRectF(-(R-26), -(R-26), (R-26)*2, (R-26)*2)
        for i in range(6):
            p.save()
            p.rotate(i * 60)
            p.drawArc(rect_m, 8*16, 38*16)
            p.restore()
        p.restore()

        # Speaking pulse ring
        if self._pulse > 0:
            pr = (R - 48) + self._pulse * 18
            p.setPen(QPen(QColor(0, 255, 200, int(200 * self._pulse)), 2))
            p.drawEllipse(QPointF(cx, cy), pr, pr)

        # Inner hexagon (slow drift)
        p.save()
        p.translate(cx, cy)
        p.rotate(self._a1 * 0.25)
        hr = R - 52
        path = QPainterPath()
        for i in range(6):
            ang = math.radians(i * 60 - 30)
            x, y = hr * math.cos(ang), hr * math.sin(ang)
            path.moveTo(x, y) if i == 0 else path.lineTo(x, y)
        path.closeSubpath()
        p.setPen(QPen(CYAN, 2))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawPath(path)
        p.restore()

        # Core radial glow
        core_r = R - 74
        grad = QRadialGradient(QPointF(cx, cy), core_r)
        grad.setColorAt(0.0, QColor(0, 220, 255, 255))
        grad.setColorAt(0.5, QColor(0, 140, 210, 160))
        grad.setColorAt(1.0, QColor(0,  40,  80,   0))
        p.setBrush(QBrush(grad))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QPointF(cx, cy), core_r, core_r)

        # Labels
        p.setPen(QPen(WHITE))
        f1 = QFont("Consolas", 9, QFont.Weight.Bold)
        p.setFont(f1)
        p.drawText(QRectF(cx-55, cy-9, 110, 18), Qt.AlignmentFlag.AlignCenter, "WEDNESDAY")

        p.setPen(QPen(QColor(0, 210, 255, 170)))
        f2 = QFont("Consolas", 7)
        p.setFont(f2)
        status = "SPEAKING" if self._speaking else "STANDBY"
        p.drawText(QRectF(cx-55, cy+7, 110, 14), Qt.AlignmentFlag.AlignCenter, status)

        p.end()


# ── AI processing thread ──────────────────────────────────────────────────────
class ProcessingThread(QThread):
    response_ready = pyqtSignal(str, list)
    error_occurred = pyqtSignal(str)

    def __init__(self, user_input, core):
        super().__init__()
        self.user_input = user_input
        self.core = core

    def run(self):
        try:
            response, skills = self.core.process_input(self.user_input)
            self.response_ready.emit(response, skills)
        except Exception as e:
            self.error_occurred.emit(str(e))


# ── Voice input thread ────────────────────────────────────────────────────────
class VoiceThread(QThread):
    heard      = pyqtSignal(str)   # successfully transcribed text
    listening  = pyqtSignal()      # mic is open and recording
    failed     = pyqtSignal()      # nothing heard / error

    def run(self):
        try:
            from assistant.speech import listen
            self.listening.emit()
            text = listen(wait_for_speech=8, max_duration=20, pause_threshold=2.5)
            if text:
                self.heard.emit(text)
            else:
                self.failed.emit()
        except Exception:
            self.failed.emit()


# ── Main window ───────────────────────────────────────────────────────────────
STYLE = f"""
QMainWindow, QWidget  {{ background: {BG}; color: #00d2ff; }}
QTextEdit {{
    background: #080820;
    color: #00d2ff;
    border: 1px solid #003a55;
    font-family: Consolas, "Courier New", monospace;
    font-size: 12px;
}}
QLineEdit {{
    background: #080820;
    color: #00e8ff;
    border: 2px solid #0077aa;
    border-radius: 2px;
    font-family: Consolas, monospace;
    font-size: 13px;
    padding: 6px 10px;
}}
QLineEdit:focus {{ border: 2px solid #00d2ff; }}
QPushButton {{
    background: #002a44;
    color: #00d2ff;
    border: 1px solid #006688;
    border-radius: 2px;
    padding: 7px 16px;
    font-family: Consolas;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
}}
QPushButton:hover  {{ background: #003d5c; border-color: #00d2ff; }}
QPushButton:pressed {{ background: #00d2ff; color: {BG}; }}
QPushButton:disabled {{ background: #111130; color: #224; border-color: #224; }}
QLabel {{ color: #00d2ff; font-family: Consolas; }}
QScrollBar:vertical {{ background: #080820; width: 5px; }}
QScrollBar::handle:vertical {{ background: #003355; border-radius: 2px; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
"""


class WednesdayGUI(QMainWindow):
    clap_signal = pyqtSignal()

    def __init__(self, core):
        super().__init__()
        self.core = core
        self._busy = False
        self._listening = False
        self._start_time = datetime.now()
        self.clap_signal.connect(self._on_clap)
        self._build_ui()
        self._init_tts_thread()
        self._start_clap()
        self._start_stats_timer()
        QTimer.singleShot(400, self._boot)

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        self.setWindowTitle("WEDNESDAY — AI SYSTEM")
        self.setMinimumSize(1080, 700)
        self.setStyleSheet(STYLE)

        root_w = QWidget()
        self.setCentralWidget(root_w)
        root = QVBoxLayout(root_w)
        root.setSpacing(0)
        root.setContentsMargins(8, 8, 8, 6)

        root.addWidget(self._header())
        root.addWidget(self._hline("#002233"))

        body = QHBoxLayout()
        body.setSpacing(8)

        # Left — reactor
        left = QWidget()
        left.setFixedWidth(280)
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 6, 0, 0)
        self.reactor = ReactorWidget()
        ll.addWidget(self.reactor)
        ll.addStretch()
        body.addWidget(left)

        body.addWidget(self._hline_v(), 0)
        body.addWidget(self._chat_panel(), 1)
        body.addWidget(self._hline_v(), 0)
        body.addWidget(self._stats_panel(), 0)

        root.addLayout(body, 1)
        root.addWidget(self._hline("#002233"))
        root.addLayout(self._input_bar())

        foot = QLabel("ENTER · send    DOUBLE-CLAP · activate    WEDNESDAY AI v2.0")
        foot.setStyleSheet("color: #003355; font-size: 9px; padding: 3px 0;")
        foot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(foot)

    def _header(self):
        w = QWidget()
        w.setFixedHeight(46)
        w.setStyleSheet(f"background: #080820; border-bottom: 1px solid #002233;")
        h = QHBoxLayout(w)
        h.setContentsMargins(14, 0, 14, 0)

        title = QLabel("◈   W E D N E S D A Y   A I   S Y S T E M")
        title.setStyleSheet("color: #00d2ff; font-size: 14px; font-weight: bold; letter-spacing: 2px;")
        h.addWidget(title)
        h.addStretch()

        self.badge = QLabel("●  ONLINE")
        self.badge.setStyleSheet("color: #00ff88; font-size: 11px; font-weight: bold;")
        h.addWidget(self.badge)
        h.addSpacing(24)

        self.clock_lbl = QLabel()
        self.clock_lbl.setStyleSheet("color: #006688; font-size: 11px;")
        h.addWidget(self.clock_lbl)
        self._tick_clock()
        t = QTimer(self); t.timeout.connect(self._tick_clock); t.start(1000)
        return w

    def _tick_clock(self):
        self.clock_lbl.setText(datetime.now().strftime("%A   %Y-%m-%d   %H:%M:%S"))

    def _chat_panel(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 4, 0, 0)
        v.setSpacing(3)

        lbl = QLabel("  ▸  CONVERSATION INTERFACE")
        lbl.setStyleSheet("color: #003a55; font-size: 9px; letter-spacing: 1px;")
        v.addWidget(lbl)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.document().setDefaultStyleSheet("""
            .ts   { color: #002d44; }
            .sys  { color: #005577; }
            .user { color: #00ffaa; }
            .wed  { color: #00d2ff; }
            .sk   { color: #887700; }
            .err  { color: #ff4444; }
        """)
        v.addWidget(self.chat)
        return w

    def _stats_panel(self):
        w = QWidget()
        w.setFixedWidth(210)
        w.setStyleSheet("background: #070718; border: 1px solid #002233;")
        v = QVBoxLayout(w)
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(7)

        def section(text):
            l = QLabel(text)
            l.setStyleSheet("color: #004466; font-size: 9px; letter-spacing: 2px;")
            return l

        v.addWidget(section("SYSTEM DIAGNOSTICS"))
        v.addWidget(self._hline("#002233"))

        self.s_cpu  = QLabel(); self.s_cpu.setTextFormat(Qt.TextFormat.RichText)
        self.s_ram  = QLabel(); self.s_ram.setTextFormat(Qt.TextFormat.RichText)
        self.s_disk = QLabel(); self.s_disk.setTextFormat(Qt.TextFormat.RichText)
        for lbl in (self.s_cpu, self.s_ram, self.s_disk):
            lbl.setStyleSheet("font-size: 11px;")
            v.addWidget(lbl)

        v.addWidget(self._hline("#002233"))
        v.addWidget(section("STATUS"))

        self.s_skills = QLabel()
        self.s_clap   = QLabel("CLAP DETECT  ●  ON")
        self.s_mem    = QLabel("MEMORY       ●  ACTIVE")
        for lbl in (self.s_skills, self.s_clap, self.s_mem):
            lbl.setStyleSheet("font-size: 10px; color: #006688;")
            v.addWidget(lbl)

        v.addWidget(self._hline("#002233"))
        self.s_uptime = QLabel()
        self.s_uptime.setStyleSheet("font-size: 10px; color: #003d55;")
        v.addWidget(self.s_uptime)
        v.addStretch()
        return w

    def _input_bar(self):
        h = QHBoxLayout()
        h.setSpacing(6)
        h.setContentsMargins(0, 6, 0, 0)

        arrow = QLabel("▶")
        arrow.setStyleSheet("color: #00d2ff; font-size: 18px; padding: 0 4px;")
        h.addWidget(arrow)

        self.inp = QLineEdit()
        self.inp.setPlaceholderText("Type or press MIC to speak...")
        self.inp.returnPressed.connect(self.send_message)
        h.addWidget(self.inp, 1)

        self.mic_btn = QPushButton("⏺ MIC")
        self.mic_btn.setFixedWidth(82)
        self.mic_btn.setStyleSheet("""
            QPushButton { background: #002a44; color: #00ffaa; border: 1px solid #00aa66; }
            QPushButton:hover { background: #003d5c; }
            QPushButton:checked { background: #004422; color: #00ff88; border: 1px solid #00ff88; }
        """)
        self.mic_btn.clicked.connect(self.start_listening)
        h.addWidget(self.mic_btn)

        self.send_btn = QPushButton("SEND")
        self.send_btn.setFixedWidth(82)
        self.send_btn.clicked.connect(self.send_message)
        h.addWidget(self.send_btn)

        return h

    def _hline(self, color="#002233"):
        w = QWidget(); w.setFixedHeight(1)
        w.setStyleSheet(f"background: {color};")
        return w

    def _hline_v(self):
        w = QWidget(); w.setFixedWidth(1)
        w.setStyleSheet("background: #002233;")
        return w

    # ── Chat helpers ──────────────────────────────────────────────────────────

    def _ts(self):
        return datetime.now().strftime("%H:%M:%S")

    def _append(self, html):
        c = self.chat.textCursor()
        c.movePosition(c.MoveOperation.End)
        self.chat.setTextCursor(c)
        self.chat.insertHtml(html + "<br>")
        c.movePosition(c.MoveOperation.End)
        self.chat.setTextCursor(c)
        self.chat.ensureCursorVisible()

    def log_sys(self, msg):
        self._append(f'<span class="ts">[{self._ts()}]</span>&nbsp;<span class="sys">◈ {html.escape(msg)}</span>')

    def log_user(self, msg):
        self._append(f'<span class="ts">[{self._ts()}]</span>&nbsp;<span class="user">▶ YOU:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{html.escape(msg)}</span>')

    def log_wed(self, msg):
        self._append(f'<span class="ts">[{self._ts()}]</span>&nbsp;<span class="wed">◈ WEDNESDAY: {html.escape(msg)}</span>')

    def log_skill(self, name, result):
        self._append(f'<span class="ts">[{self._ts()}]</span>&nbsp;<span class="sk">⚙ [{html.escape(name.upper())}] {html.escape(str(result))}</span>')

    def log_err(self, msg):
        self._append(f'<span class="ts">[{self._ts()}]</span>&nbsp;<span class="err">✕ ERROR: {html.escape(msg)}</span>')

    # ── Boot sequence ─────────────────────────────────────────────────────────

    def _boot(self):
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good morning! I'm Wednesday — what's on your plate today?"
        elif hour < 18:
            greeting = "Good afternoon! I'm Wednesday — what do you need?"
        else:
            greeting = "Good evening! I'm Wednesday — how can I help?"

        msgs = [
            ("sys",  "WEDNESDAY AI SYSTEM — BOOT SEQUENCE INITIATED"),
            ("sys",  "CORE ENGINE          ●  ONLINE"),
            ("sys",  "MEMORY MODULE        ●  LOADED"),
            ("sys",  "SKILLS REGISTRY      ●  ACTIVE"),
            ("sys",  "CLAP DETECTOR        ●  LISTENING"),
            ("sys",  "VOICE I/O            ●  READY"),
            ("sys",  "ALL SYSTEMS NOMINAL  ●  READY"),
            ("wed",  greeting),
        ]
        for i, (kind, text) in enumerate(msgs):
            QTimer.singleShot(i * 380, lambda k=kind, t=text: self._boot_line(k, t))

    def _boot_line(self, kind, text):
        if kind == "sys":
            self.log_sys(text)
        else:
            self.log_wed(text)
            QTimer.singleShot(300, lambda: self._speak(text))

    # ── Sending messages ──────────────────────────────────────────────────────

    def send_message(self):
        if self._busy:
            return
        text = self.inp.text().strip()
        if not text:
            return
        if text.lower() in ("exit", "quit", "bye", "peace"):
            self.log_sys("SHUTDOWN COMMAND RECEIVED")
            QTimer.singleShot(800, self.close)
            return

        self.inp.clear()
        self.log_user(text)
        self._set_busy(True)

        self._thread = ProcessingThread(text, self.core)
        self._thread.response_ready.connect(self._on_response)
        self._thread.error_occurred.connect(self._on_error)
        self._thread.start()

    def _on_response(self, response, skills):
        self.log_wed(response)
        for s in skills:
            if s.get("status") == "success":
                self.log_skill(s.get("skill", "?"), str(s.get("result", "done"))[:120])
            else:
                self.log_err(f"{s.get('skill','?')}: {s.get('error','?')}")
        self._set_busy(False)
        self._speak(response)

    def _on_error(self, err):
        self.log_err(err)
        self._set_busy(False)

    def _set_busy(self, busy):
        self._busy = busy
        self.send_btn.setEnabled(not busy)
        if busy:
            self._set_badge("● PROCESSING", "#ffaa00")
        else:
            self._set_badge("● ONLINE", "#00ff88")

    def _set_badge(self, text, color):
        self.badge.setText(text)
        self.badge.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: bold;")

    # ── TTS ───────────────────────────────────────────────────────────────────

    def _init_tts_thread(self):
        self._speaking = False
        self._after_speak = None

    def _mute_clap(self):
        try: self._clap_det.muted = True
        except Exception: pass

    def _maybe_unmute_clap(self):
        # Only unmute when neither TTS nor mic are active
        if not self._speaking and not self._listening:
            try: self._clap_det.muted = False
            except Exception: pass

    def _speak(self, text, after=None):
        if not text:
            if after: after()
            return
        self._speaking = True
        self._after_speak = after
        self._mute_clap()
        self.reactor.set_speaking(True)
        self._set_badge("● SPEAKING", "#00d2ff")

        def _run():
            try:
                import subprocess, os
                helper = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "speak_helper.py"
                )
                subprocess.run(
                    [sys.executable, helper],
                    input=text[:600].encode("utf-8"),
                    timeout=60,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                )
            except Exception:
                pass
            finally:
                QTimer.singleShot(0, self._done_speaking)

        threading.Thread(target=_run, daemon=True).start()

    def _done_speaking(self):
        self._speaking = False
        self.reactor.set_speaking(False)
        if not self._busy:
            self._set_badge("● ONLINE", "#00ff88")
        # Small grace period so any speaker echo dies down before unmuting
        QTimer.singleShot(400, self._maybe_unmute_clap)
        # Run any pending callback (e.g. start mic after TTS finishes)
        if self._after_speak:
            cb = self._after_speak
            self._after_speak = None
            QTimer.singleShot(450, cb)

    # ── Voice input ───────────────────────────────────────────────────────────

    def start_listening(self):
        if self._busy or self._listening or self._speaking:
            return
        self._listening = True
        self._mute_clap()
        self._voice_thread = VoiceThread()
        self._voice_thread.listening.connect(self._on_mic_open)
        self._voice_thread.heard.connect(self._on_voice_heard)
        self._voice_thread.failed.connect(self._on_voice_failed)
        self._voice_thread.start()

    def _on_mic_open(self):
        self.mic_btn.setText("● REC")
        self.mic_btn.setStyleSheet("QPushButton { background: #003300; color: #00ff44; border: 2px solid #00ff44; font-weight: bold; }")
        self.log_sys("LISTENING — speak now...")
        self._set_badge("● LISTENING", "#00ff88")

    def _reset_mic_btn(self):
        self._listening = False
        self.mic_btn.setText("⏺ MIC")
        self.mic_btn.setStyleSheet("QPushButton { background: #002a44; color: #00ffaa; border: 1px solid #00aa66; } QPushButton:hover { background: #003d5c; }")
        self._maybe_unmute_clap()

    def _on_voice_heard(self, text):
        self._reset_mic_btn()
        self.inp.setText(text)
        self._set_badge("● ONLINE", "#00ff88")
        self.send_message()

    def _on_voice_failed(self):
        self._reset_mic_btn()
        self.log_sys("Didn't catch that — try again")
        self._set_badge("● ONLINE", "#00ff88")

    # ── Clap detection ────────────────────────────────────────────────────────

    def _start_clap(self):
        try:
            from assistant.clap_detector import ClapDetector
            self._clap_det = ClapDetector(on_double_clap=lambda: self.clap_signal.emit())
            self._clap_det.start()
        except Exception:
            pass

    def _on_clap(self):
        # Ignore clap if already speaking, listening, or processing
        if self._speaking or self._listening or self._busy:
            return
        self.reactor.flash_clap()
        self.log_sys("CLAP DETECTED — WEDNESDAY ACTIVATED")
        self.log_wed("Sup? I'm listening.")
        # Speak first, then start listening when TTS finishes
        self._speak("Sup? I'm listening.", after=self.start_listening)

    # ── System stats ──────────────────────────────────────────────────────────

    def _start_stats_timer(self):
        self._update_stats()
        t = QTimer(self); t.timeout.connect(self._update_stats); t.start(2000)

    def _update_stats(self):
        try:
            import psutil
            cpu  = psutil.cpu_percent()
            ram  = psutil.virtual_memory().percent
            disk = psutil.disk_usage("C:\\").percent

            def bar(pct):
                n = int(pct / 10)
                col = "#00ff88" if pct < 60 else "#ffaa00" if pct < 85 else "#ff4444"
                return f'<span style="color:{col}">{"█"*n}{"░"*(10-n)}</span> <span style="color:#006688">{pct:.0f}%</span>'

            self.s_cpu.setText(f'CPU&nbsp;&nbsp;{bar(cpu)}')
            self.s_ram.setText(f'RAM&nbsp;&nbsp;{bar(ram)}')
            self.s_disk.setText(f'DISK&nbsp;{bar(disk)}')
        except Exception:
            self.s_cpu.setText("CPU  —")
            self.s_ram.setText("RAM  —")
            self.s_disk.setText("DISK —")

        try:
            count = len(self.core.get_available_skills())
            self.s_skills.setText(f"SKILLS LOADED  ●  {count}")
        except Exception:
            pass

        up = datetime.now() - self._start_time
        h, r = divmod(int(up.total_seconds()), 3600)
        m, s = divmod(r, 60)
        self.s_uptime.setText(f"UPTIME  {h:02d}:{m:02d}:{s:02d}")

    def closeEvent(self, event):
        try:
            self._clap_det.stop()
        except Exception:
            pass
        event.accept()


# ── Entry point ───────────────────────────────────────────────────────────────
def launch_gui(core):
    app = QApplication.instance() or QApplication(sys.argv)
    win = WednesdayGUI(core)
    win.show()
    sys.exit(app.exec())
