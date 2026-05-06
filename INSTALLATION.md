# 📋 Wednesday - Windows Installation Guide

Complete step-by-step setup instructions for Windows 10/11.

## Prerequisites

Before starting, ensure you have:
- ✅ Windows 10 or 11
- ✅ Python 3.8+ installed ([download here](https://www.python.org/downloads/))
- ✅ Microphone (built-in or USB)
- ✅ Speakers or headphones
- ✅ Internet connection
- ✅ Google account (for API key)

## Step 1: Prepare Your System

### A. Install Python (if not already installed)

1. Download from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT:** Check "Add Python to PATH"
4. Click "Install Now"
5. Wait for installation to complete

**Verify Python installed:**
```bash
python --version
# Should show: Python 3.x.x
```

### B. Update Python Package Manager (pip)

```bash
python -m pip install --upgrade pip
```

### C. Install PortAudio (for microphone support)

**Option 1: Using Chocolatey (recommended)**
```bash
# Install Chocolatey first if you don't have it:
# Open PowerShell as Administrator and run:
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Then install PortAudio:
choco install portaudio -y
```

**Option 2: Manual download**
1. Download from https://www.portaudio.com/download.html
2. Follow the build instructions
3. Or skip - pyaudio will attempt to build from source

---

## Step 2: Get Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikeys)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (keep it private!)
5. Save it somewhere safe - you'll need it soon

⚠️ **Important:** 
- Never share your API key
- Never commit it to GitHub
- Keep it in the `.env` file only

---

## Step 3: Clone/Download Wednesday

### Option A: Using Git (if installed)
```bash
git clone https://github.com/yourusername/wednesday.git
cd wednesday
```

### Option B: Manual Download
1. Download the project as ZIP
2. Extract to a folder (e.g., `C:\Users\YourUsername\WEDNESDAY`)
3. Open Command Prompt or PowerShell
4. Navigate to the folder:
```bash
cd C:\Users\YourUsername\WEDNESDAY
```

---

## Step 4: Set Up Virtual Environment (Recommended)

A virtual environment keeps dependencies isolated.

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Command Prompt:
venv\Scripts\activate

# On PowerShell:
venv\Scripts\Activate.ps1

# If PowerShell gives error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try Activate.ps1 again

# You should see (venv) at start of your prompt
```

---

## Step 5: Install Dependencies

```bash
# Make sure you're in the project directory and venv is activated

pip install -r requirements.txt

# This will install:
# - google-generativeai (Gemini)
# - SpeechRecognition (voice input)
# - pyttsx3 (voice output)
# - And other dependencies

# Wait for installation to complete (may take a few minutes)
```

### Optional: Better Speech Recognition

For faster and better local speech recognition:

```bash
pip install faster-whisper
```

This uses OpenAI's Whisper model locally (no internet required for transcription).

### Optional: Better Text-to-Speech

For better voice quality:

```bash
pip install edge-tts
pip install ffmpeg-python
choco install ffmpeg -y
```

---

## Step 6: Configure Wednesday

### A. Create .env File

In the project folder, find `.env.example` and rename/copy it to `.env`:

```bash
# Using Command Prompt:
copy .env.example .env

# Using PowerShell:
Copy-Item .env.example .env
```

### B. Edit .env with Your API Key

Open `.env` in Notepad:
```bash
notepad .env
```

Find this line:
```
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual API key from Step 2.

**Example:**
```
GEMINI_API_KEY=AIzaSyDxCzK1D-something-secret-here
```

**Other settings you can customize:**
```
GEMINI_MODEL=gemini-1.5-flash        # Model (faster/cheaper)
SPEECH_ENGINE=faster-whisper         # Or: speech_recognition
TTS_ENGINE=pyttsx3                   # Or: edge-tts
SPEECH_TIMEOUT=10                    # Seconds to listen
TTS_SPEED=150                         # Words per minute
```

Save the file (Ctrl+S in Notepad).

---

## Step 7: Test Installation

Run the diagnostic tool:

```bash
python diagnose.py
```

This will check:
- ✓ Python version
- ✓ Project files
- ✓ Environment variables
- ✓ Installed packages
- ✓ Microphone availability

**Example output:**
```
Python: 3.10.5
  ✓ OK

Project files:
  ✓ .env
  ✓ main.py
  ✓ assistant/brain.py
  ...
```

If you see ❌ errors, check the Troubleshooting section below.

---

## Step 8: Run Wednesday

### Option A: Using Python Directly

```bash
# Make sure venv is activated (you should see (venv) in prompt)
python main.py
```

### Option B: Using Batch Script (Windows-specific)

Double-click `run.bat` in the project folder.

This automatically:
- Activates virtual environment
- Checks dependencies
- Verifies .env file
- Runs Wednesday

### Expected Output

```
🤖 Wednesday AI Assistant
==================================================
Listening... (say something or type 'help' for commands)
==================================================
```

**You're ready!** 🎉

Try saying: "What's the capital of France?"

---

## Troubleshooting

### Python not found in PATH

**Problem:** `python: command not found` or `'python' is not recognized`

**Solution:**
1. Reinstall Python
2. Make sure "Add Python to PATH" is checked during installation
3. Or use full path: `C:\Python311\python.exe main.py`

### Virtual Environment Issues

**Problem:** venv activation fails or doesn't work

**Solution:**
```bash
# Delete and recreate venv
rmdir /s venv

# Create new one
python -m venv venv

# Activate (PowerShell):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1

# Or Command Prompt:
venv\Scripts\activate
```

### Microphone Not Working

**Problem:** "No speech detected" or microphone errors

**Solution:**
```bash
# Install PortAudio
choco install portaudio -y

# Reinstall pyaudio
pip uninstall pyaudio -y
pip install pyaudio

# Or use speech_recognition as fallback
# Edit .env: SPEECH_ENGINE=speech_recognition
```

**Verify microphone in Windows:**
1. Settings → Sound → Input devices
2. Check microphone is enabled and recognized
3. Test microphone: Settings → Sound → Input → Test your microphone

### API Key Issues

**Problem:** `GEMINI_API_KEY not set` or `API key invalid`

**Solution:**
1. Open `.env` file
2. Verify GEMINI_API_KEY is set correctly (no extra spaces)
3. Get fresh key from: https://makersuite.google.com/app/apikeys
4. Restart Wednesday

### Missing Dependencies

**Problem:** `ModuleNotFoundError: No module named 'X'`

**Solution:**
```bash
# Reinstall all dependencies
pip install --upgrade -r requirements.txt

# Or specific package
pip install google-generativeai SpeechRecognition pyttsx3
```

### PyAudio Installation Fails on Windows

**This is common!** Alternative solutions:

**Option 1:** Use pre-built wheel
```bash
# Download wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Then install it
pip install PyAudio‑0.2.13‑cp311‑cp311‑win_amd64.whl
```

**Option 2:** Use speech_recognition (doesn't need PyAudio)
```bash
# Edit .env
SPEECH_ENGINE=speech_recognition

# No PyAudio needed, uses Google Speech API instead
```

### No Sound Output (TTS)

**Problem:** No voice output, no errors

**Solution:**
```bash
# Test TTS directly
python -c "import pyttsx3; e = pyttsx3.init(); e.say('Hello'); e.runAndWait()"

# If no sound:
1. Check Windows volume (bottom right)
2. Check application volume (Windows settings)
3. Try edge-tts:
   pip install edge-tts
   Edit .env: TTS_ENGINE=edge-tts
```

### Permission Denied Errors

**Problem:** `PermissionError` or `Access denied`

**Solution:**
1. Run Command Prompt as Administrator
2. Close antivirus/Windows Defender temporarily (it may block PyAudio)
3. Check file permissions on project folder

### Still Having Issues?

Run the diagnostic tool to identify problems:
```bash
python diagnose.py
```

Check logs:
```bash
type logs\actions_*.log
```

---

## Next: First Run

Once set up, try these commands:

1. **"Hello"** - Basic greeting
2. **"Open Google"** - Opens website
3. **"Search for Python"** - Web search
4. **"What time is it?"** - Info query
5. **"Tell me a joke"** - Fun interaction

**Say "help" for more commands.**

---

## Updating Wednesday

To get the latest version:

```bash
# If using Git:
git pull origin main

# Then reinstall dependencies:
pip install --upgrade -r requirements.txt
```

---

## Uninstalling Wednesday

If you no longer need Wednesday:

```bash
# Delete the project folder:
# Right-click folder → Delete

# Or from Command Prompt:
rmdir /s "C:\Path\To\Wednesday"

# Delete Python and venv if desired:
# Settings → Apps → Python → Uninstall
```

---

## Performance Tips

### For Slower Computers

```
# In .env, use:
GEMINI_MODEL=gemini-1.5-flash    # Smaller/faster
SPEECH_ENGINE=speech_recognition  # Lighter than faster-whisper
TTS_ENGINE=pyttsx3               # Offline, local
```

### For Better Quality

```
# In .env, use:
GEMINI_MODEL=gemini-1.5-pro      # More powerful
SPEECH_ENGINE=faster-whisper      # More accurate
TTS_ENGINE=edge-tts              # Better voice
```

---

## Getting Help

**If something goes wrong:**

1. Run: `python diagnose.py`
2. Check logs: `type logs\actions_*.log`
3. Review Troubleshooting section above
4. Read README.md for more info
5. Check QUICK_REFERENCE.md for command examples

---

## 🎉 You're All Set!

Your Windows AI assistant is ready.

Run Wednesday:
```bash
python main.py
```

Or double-click:
```
run.bat
```

**Enjoy your personal AI assistant!** 🤖

For commands and examples, see **QUICK_REFERENCE.md**
