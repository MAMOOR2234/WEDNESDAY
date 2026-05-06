# Wednesday - JARVIS-Style Modular Architecture

## Overview

Wednesday now uses a modular architecture inspired by Project_JARVIS, featuring:

- **Core Engine** - Brain orchestration
- **Skills Registry** - Dynamic skill loading
- **Modular Skills** - Independent capability modules
- **Memory System** - Conversation context
- **Brain (Gemini)** - LLM integration

## Architecture

```
Wednesday/
├── main.py                          # CLI Interface
├── assistant/
│   ├── core.py                      # Core Engine (NEW)
│   ├── skills_registry.py           # Skills Manager (NEW)
│   ├── brain.py                     # Gemini Integration
│   ├── speech.py                    # Voice Input
│   ├── tts.py                       # Voice Output
│   ├── memory.py                    # Conversation Context
│   ├── config.py                    # Configuration
│   └── logger.py                    # Logging
│
├── skills/                          # Modular Skills (NEW)
│   ├── __init__.py                  # Base Skill Class
│   ├── app_control.py               # Open/close apps
│   ├── web_operations.py            # Web search & browsing
│   ├── file_operations.py           # File I/O
│   ├── keyboard_control.py          # Type text
│   ├── information.py               # Time/date/info
│   └── [more skills can be added]
│
├── logs/                            # Action logs
└── assistant_workspace/             # Safe file storage
```

## Core Components

### 1. **Core Engine** (`assistant/core.py`)
Orchestrates all operations:
- Processes user input
- Calls Gemini brain for reasoning
- Manages skill execution
- Maintains conversation memory

```python
# Usage
core = WednesdayCore()
response, skill_results = core.process_input("Open Chrome")
```

### 2. **Skills Registry** (`assistant/skills_registry.py`)
Dynamically loads and manages skills:
- Auto-discovers skills in `skills/` directory
- Instantiates skill classes
- Executes skills by name

```python
# Usage
skills = SkillsRegistry()
result = skills.execute("app_control", {"action": "open", "app_name": "chrome"})
available = skills.list_skills()
```

### 3. **Individual Skills** (`skills/*.py`)
Each skill is an independent module with a `Skill` class:

**Base Structure:**
```python
from skills import BaseSkill

class Skill(BaseSkill):
    name = "Skill Name"
    description = "What it does"
    
    def execute(self, args):
        # Do something
        return result
```

**Example Skills:**
- `app_control.py` - Open/close applications
- `web_operations.py` - Search and browsing
- `file_operations.py` - File read/write
- `keyboard_control.py` - Type text
- `information.py` - Time/date

### 4. **Brain** (`assistant/brain.py`)
Gemini API integration:
- Receives user input + context
- Returns response + skill recommendations
- Parses `<skills>` tags from response

### 5. **Memory** (`assistant/memory.py`)
Conversation context:
- Stores recent messages (last 20)
- Provides context to brain
- Maintains conversation state

## Adding New Skills

### Step 1: Create Skill File
Create `skills/my_skill.py`:

```python
from skills import BaseSkill

class Skill(BaseSkill):
    name = "My Skill"
    description = "What my skill does"
    
    def execute(self, args):
        # Get arguments
        action = args.get("action")
        param = args.get("param")
        
        # Do work
        result = f"Did {action} with {param}"
        
        # Return result
        return result
```

### Step 2: Register Automatically
Skills are auto-loaded! The registry scans `skills/` directory.

### Step 3: Tell Gemini About It
Update `SYSTEM_PROMPT` in `brain.py` to mention the new skill.

### Step 4: Test
```python
skills = SkillsRegistry()
result = skills.execute("my_skill", {"action": "test", "param": "value"})
print(result)
```

## Data Flow

```
User Input
    ↓
[Core Engine] (core.py)
    ↓
[Gemini Brain] (brain.py)
    ├→ Analyzes intent
    ├→ Suggests skills
    └→ Returns response
    ↓
[Skills Registry] (skills_registry.py)
    ├→ Looks up skill
    └→ Executes with args
    ↓
[Skill Execution] (skills/*.py)
    └→ Returns result
    ↓
[Response to User]
    ├→ Display text
    ├→ Speak output
    └→ Log action
```

## Skill Response Format

Skills return strings or structured data:

```python
# Simple string
return "Done"

# Structured data
return {
    "status": "success",
    "data": {...}
}
```

## Gemini Skill Calling

Gemini recommends skills in responses using `<skills>` tags:

```
Wednesday: I'll open Chrome for you.
<skills>
{"skill": "app_control", "action": "open", "args": {"app_name": "chrome"}}
</skills>
```

The core engine:
1. Extracts `<skills>` tags
2. Calls registry.execute() for each
3. Returns results to user

## Benefits of Modular Architecture

✅ **Extensibility** - Add skills without touching core
✅ **Maintainability** - Each skill is independent
✅ **Reusability** - Skills can be shared/reused
✅ **Testing** - Skills can be tested individually
✅ **Scalability** - Add hundreds of skills easily
✅ **Safety** - Centralized security in registry

## Future Skills to Add

- **Communication**: Email, SMS, messaging
- **Productivity**: Calendar, reminders, notes
- **Media**: Screenshots, video capture, image processing
- **System**: Volume, brightness, battery status
- **Internet**: Download files, API calls
- **AI**: Image recognition, sentiment analysis

## Configuration

Edit `assistant/config.py` to customize behavior:
- Gemini model
- Speech engine
- TTS engine
- Workspace directory
- Timeout values

## Logging

All actions logged to `logs/actions_YYYYMMDD.log`:
- User inputs
- Skill executions
- Brain responses
- Errors

## Performance Tips

1. **Skills Registry Cache** - Already caches loaded skills
2. **Lazy Loading** - Skills loaded once at startup
3. **Async Skills** - Can be added for long operations
4. **Batch Operations** - Execute multiple skills in sequence

## Security

✅ **Sandboxed File Operations** - Only `assistant_workspace/`
✅ **Input Validation** - Skills validate arguments
✅ **Logging** - All actions tracked
✅ **No Shell Injection** - No eval/exec used
✅ **Confirmation** - Risky actions can require approval

---

**Wednesday is now modular, scalable, and extensible like JARVIS!** 🤖
