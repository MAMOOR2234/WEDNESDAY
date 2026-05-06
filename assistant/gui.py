"""
Wednesday AI Assistant - JARVIS-Style GUI
Futuristic UI with animated reactor core
"""

import sys
import json
from datetime import datetime
from pathlib import Path

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTextEdit, QPushButton, QLabel, QScrollArea
    )
    from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QRect
    from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QBrush
    from PyQt6.QtCore import QSize
except ImportError:
    print("PyQt6 not installed. Installing...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6"], check=True)
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTextEdit, QPushButton, QLabel, QScrollArea
    )
    from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QRect
    from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QBrush
    from PyQt6.QtCore import QSize


class ReactorCore(QWidget):
    """Animated reactor core visualization."""

    def __init__(self):
        super().__init__()
        self.rotation = 0
        self.setMinimumSize(400, 400)

        # Start animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.timer.start(30)

    def rotate(self):
        """Animate rotation."""
        self.rotation = (self.rotation + 2) % 360
        self.update()

    def paintEvent(self, event):
        """Draw reactor core."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Dark background
        painter.fillRect(self.rect(), QColor(10, 10, 20))

        # Get center
        center_x = self.width() // 2
        center_y = self.height() // 2
        center = (center_x, center_y)

        # Draw concentric circles (blue glow effect)
        painter.setPen(QPen(QColor(0, 150, 255), 2))
        for i in range(15, 100, 7):
            painter.drawEllipse(center_x - i, center_y - i, i * 2, i * 2)

        # Draw rotating rays
        painter.setPen(QPen(QColor(0, 200, 255), 3))
        for angle in range(0, 360, 45):
            rad = (angle + self.rotation) * 3.14159 / 180
            x1 = center_x
            y1 = center_y
            x2 = center_x + int(80 * __import__('math').cos(rad))
            y2 = center_y + int(80 * __import__('math').sin(rad))
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        # Draw center circle
        painter.fillEllipse(center_x - 20, center_y - 20, 40, 40)

        # Draw "WEDNESDAY" text in center
        painter.setPen(QColor(0, 200, 255))
        font = QFont("Arial", 16, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(
            center_x - 60, center_y - 5, 120, 20,
            Qt.AlignmentFlag.AlignCenter, "WEDNESDAY"
        )


class ProcessingThread(QThread):
    """Thread for processing AI requests."""
    response_ready = pyqtSignal(str, list)
    error_occurred = pyqtSignal(str)

    def __init__(self, user_input, core):
        super().__init__()
        self.user_input = user_input
        self.core = core

    def run(self):
        """Process input with AI."""
        try:
            response, skills = self.core.process_input(self.user_input)
            self.response_ready.emit(response, skills)
        except Exception as e:
            self.error_occurred.emit(str(e))


class WednesdayGUI(QMainWindow):
    """JARVIS-style GUI for Wednesday."""

    def __init__(self, core):
        super().__init__()
        self.core = core
        self.init_ui()

    def init_ui(self):
        """Initialize UI."""
        self.setWindowTitle("WEDNESDAY - AI Assistant")
        self.setGeometry(100, 100, 1000, 800)

        # Set dark stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a14;
            }
            QWidget {
                background-color: #0a0a14;
                color: #00d8ff;
            }
            QTextEdit {
                background-color: #1a1a2e;
                color: #00d8ff;
                border: 2px solid #0099ff;
                font-family: 'Courier New';
                font-size: 11px;
            }
            QPushButton {
                background-color: #0099ff;
                color: #0a0a14;
                border: none;
                padding: 10px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #00d8ff;
            }
            QLabel {
                color: #00d8ff;
            }
        """)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        # Top: Reactor core
        self.reactor = ReactorCore()
        layout.addWidget(self.reactor)

        # Middle: Chat display
        chat_layout = QHBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setMinimumHeight(200)
        self.add_system_message("WEDNESDAY ONLINE")
        self.add_system_message("Status: Functional. How can I assist you today?")
        chat_layout.addWidget(self.chat_display)

        layout.addLayout(chat_layout)

        # Bottom: Input area
        input_layout = QHBoxLayout()

        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(60)
        self.input_field.setPlaceholderText("Enter command or question...")
        input_layout.addWidget(self.input_field)

        self.send_button = QPushButton("SEND")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)

        # Time label
        self.time_label = QLabel()
        layout.addWidget(self.time_label)

        # Update time
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        main_widget.setLayout(layout)

    def add_system_message(self, message):
        """Add system message to chat."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] SYSTEM: {message}\n"
        self.chat_display.append(formatted)

    def add_user_message(self, message):
        """Add user message to chat."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] YOU: {message}\n"
        self.chat_display.append(formatted)

    def add_wednesday_message(self, message):
        """Add Wednesday message to chat."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] WEDNESDAY: {message}\n"
        self.chat_display.append(formatted)

    def send_message(self):
        """Send message to Wednesday."""
        user_input = self.input_field.toPlainText().strip()
        if not user_input:
            return

        self.add_user_message(user_input)
        self.input_field.clear()

        # Process in thread
        self.thread = ProcessingThread(user_input, self.core)
        self.thread.response_ready.connect(self.on_response)
        self.thread.error_occurred.connect(self.on_error)
        self.thread.start()

    def on_response(self, response, skills):
        """Handle response from AI."""
        self.add_wednesday_message(response)

        if skills:
            for skill in skills:
                skill_info = f"[SKILL EXECUTED] {skill.get('skill', 'unknown')}"
                self.add_system_message(skill_info)

    def on_error(self, error):
        """Handle error."""
        self.add_system_message(f"ERROR: {error}")

    def update_time(self):
        """Update time display."""
        now = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(f"SYSTEM TIME: {now}")

    def keyPressEvent(self, event):
        """Handle key press."""
        if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.send_message()
        else:
            super().keyPressEvent(event)


def launch_gui(core):
    """Launch Wednesday GUI."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    gui = WednesdayGUI(core)
    gui.show()
    sys.exit(app.exec())
