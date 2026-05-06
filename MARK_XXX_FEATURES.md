# 🚀 Wednesday - Mark-XXX Enhanced Edition

## What's New (Based on Mark-XXX)

I've upgraded Wednesday with **advanced features** inspired by Mark-XXX:

### ✨ New Features

**1. Persistent Memory with Preferences** ✅
- Remembers conversation history
- Learns user preferences
- Stores user profile information
- Auto-saves to disk

**2. Advanced Skills System** ✅
- **Weather** - Get weather for any location
- **Reminders & Notes** - Create and manage reminders
- **Visual Awareness** - Take screenshots, analyze screen
- **Autonomous Workflows** - Multi-step task execution
- **System Info** - Monitor CPU, memory, disk usage

**3. User Learning** ✅
- Remembers what you like
- Learns preferences over time
- Personalizes responses
- Adapts to your style

**4. Multi-Step Automation** ✅
- Execute workflows automatically
- Chain multiple actions
- Save custom workflows
- Built-in workflow templates

---

## New Skills Available

### 📊 Weather Skill
```
You: "What's the weather?"
Wednesday: "It's 22°C with partly cloudy. Humidity: 65%"
```

### 📝 Reminders & Notes
```
You: "Remind me to call mom tomorrow"
Wednesday: "Reminder set: call mom tomorrow"

You: "List my reminders"
Wednesday: [Shows all reminders]
```

### 📸 Visual Awareness
```
You: "Take a screenshot"
Wednesday: "Screenshot saved!"

You: "What's on my screen?"
Wednesday: [Analyzes and describes screen content]
```

### ⚙️ Autonomous Workflows
```
You: "Run morning routine"
Wednesday: [Executes: get time → weather → news]
"Morning routine complete!"
```

### 💻 System Info
```
You: "How's my computer doing?"
Wednesday: "CPU: 15%, Memory: 42%, Disk: 68%"
```

---

## Enhanced Architecture

```
Wednesday (Enhanced)
├── Core Engine (core.py)
├── Advanced Memory (advanced_memory.py) - NEW
├── Skills Registry (skills_registry.py)
└── Skills/
    ├── app_control.py
    ├── web_operations.py
    ├── file_operations.py
    ├── keyboard_control.py
    ├── information.py
    ├── weather.py                  ✨ NEW
    ├── reminders_notes.py          ✨ NEW
    ├── visual_awareness.py         ✨ NEW
    ├── workflows.py                ✨ NEW
    └── system_info.py              ✨ NEW
```

---

## Persistent Storage

Wednesday now saves to `assistant_workspace/`:

```
assistant_workspace/
├── memory.json          - Conversation history
├── preferences.json     - User preferences
├── reminders.json       - All reminders
├── notes.json           - All notes
└── screenshots/         - Screenshot storage
```

---

## New Files Created

1. **`assistant/advanced_memory.py`** - Enhanced memory system
2. **`skills/weather.py`** - Weather info
3. **`skills/reminders_notes.py`** - Reminders & notes
4. **`skills/visual_awareness.py`** - Screenshots & screen analysis
5. **`skills/workflows.py`** - Autonomous workflows
6. **`skills/system_info.py`** - System monitoring

---

## Usage Examples

### Learning Preferences
```python
from assistant.advanced_memory import EnhancedMemory

memory = EnhancedMemory()
memory.set_preference("favorite_browser", "Chrome")
memory.set_preference("preferred_language", "casual")
memory.set_user_info("name", "Alex")

# Later, Wednesday remembers:
"Yo Alex, I remember you like Chrome!"
```

### Creating Reminders
```
You: "Remind me to drink water in 2 hours"
Wednesday: "Got it! Reminder set for 2 hours from now"

You: "Show my reminders"
Wednesday: "1. Drink water - 2 hours from now
           2. Call mom - Tomorrow"
```

### Autonomous Workflows
```
You: "Do my morning routine"
Wednesday: [Runs workflow]
"1. Current time: 8:00 AM
 2. Weather: 22°C, sunny
 3. Today's headlines loaded
 All done, have a great day!"
```

### System Monitoring
```
You: "How's my computer?"
Wednesday: "CPU: 18%, Memory: 45%, Disk: 62%
           Everything looks good, mate!"
```

---

## Feature Comparison

| Feature | JARVIS | Mark-XXX | Wednesday |
|---------|--------|----------|-----------|
| Voice I/O | ✅ | ✅ | ✅ |
| Modular Skills | ✅ | ✅ | ✅ |
| System Control | ✅ | ✅ | ✅ |
| Web Search | ✅ | ✅ | ✅ |
| **Persistent Memory** | ❌ | ✅ | ✅ |
| **Learn Preferences** | ❌ | ✅ | ✅ |
| **Visual Awareness** | ❌ | ✅ | ✅ |
| **Workflows** | ❌ | ✅ | ✅ |
| **System Monitoring** | ❌ | ✅ | ✅ |
| Friendly Personality | ⭐ | ✅ | ✅✅ |

---

## Installation

New optional dependencies (already in requirements.txt):

```bash
pip install psutil    # System monitoring
pip install pillow    # Screenshot capability
pip install pytesseract  # OCR (optional)
```

---

## Next: Get Fresh API Key & Run

1. **Get API Key:** https://makersuite.google.com/app/apikeys
2. **Update .env:**
   ```
   GEMINI_API_KEY=your_new_key_here
   ```
3. **Run:**
   ```bash
   python main.py
   ```

---

## Command Examples

```
"What's the weather in London?"
→ Shows weather for London

"Create a reminder to exercise"
→ Saves reminder

"Take a screenshot"
→ Captures screen to workspace

"Run morning routine"
→ Executes workflow

"How's my computer?"
→ Shows system stats

"What do you remember about me?"
→ Shows user profile

"Tell me about my reminders"
→ Lists all reminders
```

---

## Advanced Features Still Coming

- 🎥 Webcam integration
- 🧠 Deeper learning from interactions
- 📧 Email integration
- 📱 SMS/messaging
- 🎮 Code assistant
- 🤖 More autonomous workflows
- 🔔 Push notifications
- ⏰ Scheduled tasks

---

## Architecture Comparison

**JARVIS:**
```
GUI Layer
  ↓
Core Engine
  ↓
Skills
```

**Mark-XXX:**
```
Agent (Reasoning)
  ↓
Core Engine
  ↓
Actions + Memory
```

**Wednesday (Combined Best):**
```
Brain (Gemini) ← Modern LLM
  ↓
Core Engine ← Orchestrator
  ↓
Skills Registry ← Modular
  ↓
Skills + Memory ← Persistent & Learning
  ↓
System Actions ← Multi-step automation
```

---

## Configuration Tips

### Learning Speed
Wednesday learns fastest when you:
- Tell her your preferences explicitly
- Correct her when she's wrong
- Praise her when she gets it right
- Use her regularly

### Memory Management
```python
# View what Wednesday remembers
memory = EnhancedMemory()
print(memory.get_summary())
# Output: {'messages': 47, 'preferences': 5, 'user_info_fields': 3}
```

### Workflow Creation
Create custom workflows by:
1. Telling Wednesday the steps
2. She saves as a workflow
3. Run anytime: "Do [workflow name]"

---

## Performance

✅ **Fast:** Persistent memory loads instantly
✅ **Smart:** Learns from every interaction
✅ **Responsive:** Multi-step workflows run seamlessly
✅ **Reliable:** All data auto-saved

---

**Wednesday is now a full-featured AI assistant with learning, memory, and autonomous workflows!** 🤖✨

Get your API key and start using her now! 💯
