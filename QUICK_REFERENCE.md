# Wednesday Quick Reference

## 🎤 Voice Commands Examples

### Information & Help
- "What is machine learning?"
- "Tell me a joke"
- "What's the weather like?"
- "Current time"
- "Summarize Python best practices"

### Web & Search
- "Open Google"
- "Search for climate change"
- "Go to GitHub"
- "Open Facebook"
- "Search for Python tutorials"

### Applications
- "Open Chrome"
- "Open Word"
- "Open Notepad"
- "Open Excel"
- "Open VS Code"
- "Close Chrome"
- "Close Word"

### Text Input
- "Type hello world"
- "Type my email is test@example.com"
- "Type: The quick brown fox"

### File Operations
- "Save this text to notes.txt"
- "Read notes.txt"
- "Create file: my_ideas.txt with [content]"
- "Read my workspace"

### System
- "What time is it?"
- "Help"
- "Exit"
- "Quit"

---

## 🖥️ Keyboard Commands

When voice is unavailable, type:

```
help     → Show available commands
exit     → Close Wednesday
quit     → Close Wednesday
[text]   → Any question or request
```

---

## ⚙️ Keyboard Shortcuts

- `Ctrl+C` → Skip voice recording / Exit
- `Tab` → Answer yes/no prompts
- `Enter` → Confirm action

---

## 🚨 Safety Features

Before risky actions, you'll see:
```
⚠️ Wednesday wants to: [action]
Confirm? (yes/no): 
```

Type: `yes` or `y` to proceed
Type: `no` or `n` to cancel

**Risky actions requiring confirmation:**
- Opening applications
- Typing text
- Web searches
- File operations

---

## 📁 File Operations

Files automatically save to: `assistant_workspace/`

**Safe:**
- Read/write .txt, .md, .json files
- Organized in dedicated folder

**Restricted:**
- Cannot access system files
- Cannot escape workspace directory
- Cannot delete files (only read/write)

---

## 🐛 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| No speech detected | Speak louder, reduce background noise |
| No TTS sound | Check volume, try: `python diagnose.py` |
| API key error | Edit .env with your GEMINI_API_KEY |
| Microphone error | Run: `python diagnose.py` |
| Module not found | Run: `pip install -r requirements.txt` |

---

## 📊 Configuration

Edit `.env` file:

```
GEMINI_MODEL=gemini-1.5-flash      # Model to use
SPEECH_ENGINE=faster-whisper       # Voice recognition
TTS_ENGINE=pyttsx3                 # Text-to-speech
SPEECH_TIMEOUT=10                  # Listening duration (seconds)
TTS_SPEED=150                       # Speech speed (50-300)
```

---

## 🔍 Checking Status

View today's action log:
```bash
type logs\actions_*.log
```

Run diagnostic:
```bash
python diagnose.py
```

---

## 🎯 10 Quick Examples

1. `"What's the capital of France?"` → Factual question
2. `"Open Chrome"` → App control
3. `"Search for AI news"` → Web search
4. `"Type Hello Wednesday"` → Text input
5. `"Save my ideas"` → File save
6. `"Close Word"` → App close
7. `"Tell me a programming joke"` → Humor
8. `"Go to Google"` → Website
9. `"Read my notes"` → File read
10. `"Exit"` → Close assistant

---

## 🚀 Getting Started

```bash
# 1. Run setup
python setup.py

# 2. Edit .env with your API key
# 3. Run Wednesday
python main.py

# OR use batch script
run.bat
```

---

**Wednesday is ready to help! 🤖**
