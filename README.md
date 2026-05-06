# 🤖 Wednesday - Windows Desktop AI Assistant

A friendly, intelligent AI assistant for Windows that listens to your voice, understands your requests, and helps you control your computer. Powered by Google's Gemini API.

## Features

✨ **Voice I/O**
- Real-time speech recognition (faster-whisper or Google Speech Recognition)
- Natural text-to-speech output (pyttsx3 or Edge TTS)
- Fallback to keyboard input if voice unavailable

🧠 **Gemini-Powered Intelligence**
- Advanced reasoning with Gemini 1.5 Flash
- Conversational memory (recent 20 messages)
- Smart intent detection and tool execution

🖥️ **Windows Control**
- Open/close applications
- Launch websites and web searches
- Type text automatically
- Safe file operations (limited to `assistant_workspace/`)

🔒 **Safety First**
- Confirmation required for risky actions
- Restricted file access (only `assistant_workspace/`)
- All actions logged to `logs/actions.log`
- No raw shell command execution

💬 **Personality**
- Smart, calm, and loyal
- Slightly witty and charming
- Respectful and safety-conscious

## Installation

### Prerequisites
- Windows 10/11
- Python 3.8+
- Microphone (for voice input)
- Speakers/headphones (for voice output)
- Google Gemini API key

### Step 1: Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikeys)
2. Click "Create API Key"
3. Copy your API key

### Step 2: Clone/Download Wednesday

```bash
cd C:\Users\YourUsername\WEDNESDAY
```

### Step 3: Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**Optional: Install additional TTS support**
```bash
# For Edge TTS (better quality)
pip install edge-tts

# For faster-whisper (better speech recognition)
pip install faster-whisper
```

### Step 5: Configure Environment

```bash
# Copy example config
copy .env.example .env

# Edit .env with your API key
# (Open .env in Notepad and add your GEMINI_API_KEY)
```

Your `.env` file should look like:
```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash
SPEECH_ENGINE=faster-whisper
TTS_ENGINE=pyttsx3
```

### Step 6: Run Wednesday

```bash
python main.py
```

You should see:
```
🤖 Wednesday AI Assistant
==================================================
Listening... (say something or type 'help' for commands)
==================================================
```

## Usage

### Voice Commands

Say any of these after "Listening...":

1. **"Open Chrome"** → Opens Google Chrome browser
2. **"Search for machine learning tutorials"** → Google search
3. **"Open Word"** → Opens Microsoft Word
4. **"Close Word"** → Closes Microsoft Word
5. **"Type Hello World"** → Types on screen
6. **"What time is it?"** → Wednesday tells you the current time
7. **"Tell me a joke"** → Wednesday tells you something funny
8. **"Save my notes"** → Can save/read files in assistant_workspace/
9. **"What's the weather?"** → Gets weather info via web search
10. **"Exit"** → Closes Wednesday

### Text Commands (Keyboard)

If voice input times out or fails, you can type instead:

```
help          - Show available commands
exit / quit   - Close Wednesday
[Any question or command]
```

### Safety Confirmations

For risky actions, you'll see:
```
⚠️ Wednesday wants to: open_app with args: {'app_name': 'Chrome'}
Confirm? (yes/no): 
```

Type `yes` or `y` to proceed, anything else to cancel.

### File Operations

Files are automatically saved to `assistant_workspace/`:

**Write:**
- "Save this text to my_notes.txt"
- Wednesday will ask for confirmation, then save

**Read:**
- "Read my_notes.txt"
- Wednesday will read and display the contents

## Project Structure

```
WEDNESDAY/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment config
├── README.md              # This file
│
├── assistant/
│   ├── __init__.py        # Module marker
│   ├── config.py          # Configuration management
│   ├── brain.py           # Gemini API integration
│   ├── speech.py          # Voice input
│   ├── tts.py             # Voice output
│   ├── tools.py           # Windows control
│   ├── memory.py          # Conversation context
│   └── logger.py          # Logging utility
│
├── logs/                  # Action logs (auto-created)
│   └── actions_YYYYMMDD.log
│
└── assistant_workspace/   # Safe file storage (auto-created)
    └── (user files here)
```

## 10 Example Commands

### Information & Conversation
```
1. "What's the capital of France?"
   → Wednesday: "The capital of France is Paris..."

2. "Tell me a programming joke"
   → Wednesday: "Why do Java developers wear glasses?..."

3. "Summarize the history of artificial intelligence"
   → Wednesday: "AI began in the 1950s when researchers..."
```

### Web & Search
```
4. "Open Google"
   → Opens https://google.com

5. "Search for latest Python tutorials"
   → Opens Google search results

6. "Go to GitHub"
   → Opens https://github.com
```

### Application Control
```
7. "Open Notepad"
   → Launches Windows Notepad

8. "Open Excel"
   → Launches Microsoft Excel

9. "Close Chrome"
   → Closes Chrome browser
```

### File Operations
```
10. "Save my project ideas to notes.txt"
    → Saves content to assistant_workspace/notes.txt
    (Wednesday will ask what to save)
```

## Troubleshooting

### 1. Microphone Issues

**Problem:** "No speech detected" or microphone not working

**Solutions:**
```bash
# Install pyaudio for microphone support
pip install pipwin
pipwin install pyaudio

# OR use Chocolatey (Windows)
choco install portaudio

# Test microphone in Windows Settings > Sound > Input devices
```

**Fallback:** Use keyboard input when voice fails

---

### 2. Speech Recognition Errors

**Problem:** "Speech recognition error: [Errno -1]"

**Causes & Solutions:**
- No internet (Google Speech Recognition requires internet)
- Microphone permission denied
  - Go to Settings > Privacy > Microphone > Allow apps to access microphone
- Bad audio quality
  - Speak clearly, reduce background noise

**Test the microphone:**
```bash
# Try a simple test
python -c "from speech_recognition import Microphone; print('Microphone OK')"
```

---

### 3. TTS (Text-to-Speech) Issues

**Problem:** "TTS error" or no sound output

**If using pyttsx3:**
```bash
# Reinstall
pip uninstall pyttsx3 -y
pip install pyttsx3
```

**If using edge-tts:**
```bash
# Install with FFMPEG support
pip install edge-tts
pip install ffmpeg-python

# Install FFMPEG on Windows
choco install ffmpeg
```

**Test TTS:**
```bash
python -c "import pyttsx3; engine = pyttsx3.init(); engine.say('Hello'); engine.runAndWait()"
```

---

### 4. Gemini API Key Issues

**Problem:** "GEMINI_API_KEY not set" or "API key invalid"

**Solutions:**
1. Check `.env` file exists and has GEMINI_API_KEY
2. Get fresh API key from [Google AI Studio](https://makersuite.google.com/app/apikeys)
3. Verify key is pasted without extra spaces
4. Check internet connection

**Debug:**
```bash
# Verify environment variables
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"
```

---

### 5. pyautogui Type Errors

**Problem:** "Type text" command not working

**Solution:**
```bash
# Install pyautogui
pip install pyautogui

# On Windows 11, may need additional permission
# Try typing in Notepad first (simpler target)
```

**Note:** Ensure the text input field is focused before using "type" command.

---

### 6. Module Not Found Errors

**Problem:** "ModuleNotFoundError: No module named 'X'"

**Solution:**
```bash
# Reinstall all dependencies
pip install -r requirements.txt

# Verify virtual environment is activated
# (you should see (venv) at start of command prompt)
```

---

### 7. No Logs Generated

**Problem:** `logs/actions.log` is empty or not created

**Solution:**
- Logs directory is auto-created in first run
- Check `logs/` folder in project directory
- Verify write permissions on project folder

---

## Configuration Tips

### Optimize Speech Recognition

In `.env`:
```
# For better accuracy (slower but accurate)
SPEECH_ENGINE=speech_recognition
SPEECH_TIMEOUT=15

# For faster response (uses local model)
SPEECH_ENGINE=faster-whisper
SPEECH_TIMEOUT=10
```

### Optimize TTS

```
# For offline/no-internet use
TTS_ENGINE=pyttsx3

# For better quality (requires internet)
TTS_ENGINE=edge-tts
TTS_SPEED=150  # Slow down if too fast (default)
```

### Change Gemini Model

```
# Try faster responses
GEMINI_MODEL=gemini-1.5-flash

# Try better reasoning (slower)
GEMINI_MODEL=gemini-1.5-pro
```

## Next Upgrades

### Phase 1: Enhanced Control
- [ ] Wake word detection ("Hey Wednesday")
- [ ] Calendar integration (add events, check schedule)
- [ ] Email integration (read/send emails)
- [ ] Timer and reminders
- [ ] Weather integration

### Phase 2: GUI & UX
- [ ] Tkinter desktop GUI with chat window
- [ ] Visualization of tool execution
- [ ] Settings panel for configuration
- [ ] Real-time transcription display
- [ ] Voice indicator animation

### Phase 3: Advanced Features
- [ ] Multi-language support
- [ ] Custom voice profiles
- [ ] Automation routines ("Morning routine", "Goodnight")
- [ ] Integration with IFTTT / Zapier
- [ ] Learn user preferences and patterns
- [ ] Screenshot analysis ("What's on screen?")

### Phase 4: AI Enhancements
- [ ] Local LLM fallback (Ollama)
- [ ] Fine-tune responses on user feedback
- [ ] Semantic search in file history
- [ ] Voice cloning for personalized TTS
- [ ] Multi-modal input (camera, screen)

## Security Notes

⚠️ **Important:**
- Never commit `.env` file to Git (contains API keys)
- File operations limited to `assistant_workspace/` only
- No direct shell command execution from user input
- All actions logged and auditable
- Confirmation required for system actions
- Microphone access requires OS permission

## Debugging

Enable detailed logging:
```
# View logs in real-time
type logs\actions_*.log

# Or follow logs as they're written
Get-Content -Path logs\actions_*.log -Wait
```

## Common Queries

**Q: Can Wednesday access the internet?**
A: Yes! Wednesday can perform web searches and open websites.

**Q: Is my microphone recording saved?**
A: No. Audio is only processed for real-time speech-to-text and not stored.

**Q: Can Wednesday delete files?**
A: No. File operations are limited to safe read/write in `assistant_workspace/`.

**Q: Does it work offline?**
A: Partially. Local speech recognition works offline, but Gemini API and web search require internet.

**Q: How do I stop Wednesday?**
A: Say "exit" or "quit", or press Ctrl+C.

---

## Support & Contribution

Found a bug? Have a feature request?
- Check the logs in `logs/actions_*.log`
- Review error messages carefully
- Try troubleshooting section above
- Ensure all dependencies are installed

---

## License

MIT License - Feel free to modify and use Wednesday for personal projects.

---

**Enjoy your personal AI assistant! 🚀**
