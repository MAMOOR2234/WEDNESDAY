# 🎮 Wednesday - JARVIS-Style GUI Interface

## What You Get

A **futuristic GUI** just like JARVIS with:

✨ **Animated Reactor Core**
- Blue glowing concentric circles
- Smooth rotating animation
- Real-time visual feedback

🖥️ **Dark Futuristic Theme**
- Black background with blue accents
- Monospace terminal font
- Professional sci-fi aesthetic

💬 **Real-Time Chat**
- System messages
- User input display
- Wednesday responses
- Timestamped log

⏰ **System Status**
- Current time display
- Status indicators
- Real-time updates

---

## Installation

### Step 1: Install GUI Framework

```bash
pip install PyQt6
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### Step 2: Launch GUI

```bash
python gui_launcher.py
```

Or with your Python:
```bash
python3 gui_launcher.py
```

---

## How to Use GUI

1. **Start the GUI:**
   ```bash
   python gui_launcher.py
   ```

2. **Type your command** in the input box at the bottom

3. **Click SEND** or press `Ctrl+Enter`

4. **Watch the reactor core animate** while processing

5. **See response appear** in the chat area

---

## Example Interaction

```
[12:34:56] SYSTEM: WEDNESDAY ONLINE
[12:34:56] SYSTEM: Status: Functional. How can I assist you today?

[12:35:10] YOU: Open Chrome
[12:35:11] WEDNESDAY: Yo, opening Chrome now!
[12:35:11] SYSTEM: [SKILL EXECUTED] app_control

[12:35:15] YOU: Tell me a joke
[12:35:16] WEDNESDAY: Why do Java developers wear glasses? Because they don't C#! 😂

[12:35:20] YOU: What's the weather?
[12:35:21] WEDNESDAY: It's 22°C and sunny out there! Perfect day!
```

---

## GUI Features

### 1. Reactor Core
- **Animated blue circles** that rotate smoothly
- Shows "WEDNESDAY" in the center
- Pure visualization - adds life to the interface

### 2. Chat Display
- All messages timestamped
- Color-coded (System/User/Wednesday)
- Scrollable history
- Monospace font for clarity

### 3. Input Area
- Large text box for typing commands
- SEND button for submission
- Auto-clears after send

### 4. System Status
- Real-time clock display
- System status messages
- Connection indicators

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+Enter` | Send message |
| Regular Enter | New line |
| `Ctrl+C` (terminal) | Exit |

---

## Comparison: CLI vs GUI

| Aspect | CLI | GUI |
|--------|-----|-----|
| **Setup** | Instant | 2 minutes |
| **Visuals** | Text-only | Futuristic |
| **Interaction** | Terminal | Windows |
| **Appeal** | Hackers | Everyone |
| **Features** | Same | Same |
| **Speed** | Fast | Same speed |

---

## Running Both Modes

### CLI Mode (Terminal)
```bash
python main.py
```

### GUI Mode (Graphical)
```bash
python gui_launcher.py
```

**Both work with same brain (Gemini/OpenAI)!**

---

## Troubleshooting GUI

### Error: "PyQt6 not installed"
**Solution:**
```bash
pip install PyQt6
```

### GUI window not appearing
**Solution:**
- Make sure you're running with Python GUI support
- Try: `python -m pip install PyQt6`
- Restart your system if needed

### Reactor core not animating
**Solution:**
- This is normal - just visual
- Try clicking in window to focus

### Can't type in input box
**Solution:**
- Click in the input area first
- Make sure it's focused (blue border)

### Program crashes on startup
**Solution:**
```bash
# Reinstall PyQt6
pip uninstall PyQt6 -y
pip install PyQt6
```

---

## Customization

You can customize the GUI by editing `assistant/gui.py`:

### Change Colors
```python
# Around line 150, find:
self.setStyleSheet("""
    QWidget {
        background-color: #0a0a14;    # Dark background
        color: #00d8ff;               # Cyan text
    }
    QPushButton {
        background-color: #0099ff;    # Blue button
    }
""")
```

### Change Font
```python
# Find:
font = QFont("Arial", 16, QFont.Weight.Bold)
# Change to your favorite font
```

### Change Reactor Size
```python
# Find:
self.setMinimumSize(400, 400)
# Change to larger/smaller
```

### Change Colors More
- `#0a0a14` - Background (very dark blue)
- `#00d8ff` - Cyan/bright blue text
- `#0099ff` - Bright blue elements

---

## Performance

✅ **Smooth animations** - 30FPS reactor core
✅ **Responsive** - UI doesn't freeze during AI processing
✅ **Fast** - No noticeable lag
✅ **Efficient** - Uses threading for long operations

---

## Feature Completeness

Both CLI and GUI support:
✅ All 10 skills
✅ Persistent memory
✅ Dual brain (Gemini + OpenAI)
✅ Voice output (TTS)
✅ Real-time responses
✅ Conversation history

**Zero difference in functionality!**

---

## Next Steps

### Launch GUI Now
```bash
python gui_launcher.py
```

### Or Keep Using CLI
```bash
python main.py
```

### Or Use Both
Switch between them anytime!

---

## Screenshots (Visual Style)

The GUI features:
- Dark background with blue accents
- Animated reactor core (blue concentric circles)
- Real-time chat display
- Timestamped messages
- System status bar
- Professional sci-fi aesthetic

**Exactly like JARVIS!** 🤖

---

## Files Created

1. `assistant/gui.py` - Full GUI implementation
2. `gui_launcher.py` - GUI entry point

---

## Summary

**Wednesday now has TWO interfaces:**

1. **CLI** - `python main.py`
   - Terminal-based
   - Fast setup
   - Text interaction

2. **GUI** - `python gui_launcher.py`
   - Futuristic interface
   - Animated reactor core
   - Professional look
   - Same full functionality

**Choose whichever you prefer!** 🎮✨

---

**Ready to use the GUI?**
```bash
pip install PyQt6
python gui_launcher.py
```

Enjoy your JARVIS-style AI assistant! 🚀
