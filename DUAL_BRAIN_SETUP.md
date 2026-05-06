# 🔌 Wednesday - Dual Brain Setup (Gemini + OpenAI)

## Quick Start: Choose Your Brain

### Option 1: Use Gemini (Current Setup) ✅
Already configured! Your Gemini API key is ready.
```bash
python main.py
```

### Option 2: Switch to OpenAI

**Step 1: Get OpenAI Key**
👉 https://platform.openai.com/api-keys

**Step 2: Update `.env`**
```env
BRAIN_TYPE=openai
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

**Step 3: Install OpenAI**
```bash
pip install openai
```

**Step 4: Run**
```bash
python main.py
```

---

## Side-by-Side Comparison

| Feature | Gemini | OpenAI |
|---------|--------|--------|
| **Setup** | ✅ Already done | Need API key |
| **Cost** | FREE (60req/min) | Cheap ($0.15 per 1M tokens) |
| **Speed** | Fast | Very fast |
| **Intelligence** | Great | Excellent |
| **Personality** | Same friendly | Same friendly |
| **All Features** | ✅ Yes | ✅ Yes |
| **Status** | ✅ Ready | 🔧 Optional |

---

## Current Status

```
✅ Gemini Brain:        ACTIVE & WORKING
✅ OpenAI Brain:        INSTALLED & READY
✅ Dual Support:        ENABLED
✅ Easy Switching:      SUPPORTED
```

**Both brains are fully integrated!**

---

## Switching Brains

To switch, just change `.env`:

**Use Gemini:**
```env
BRAIN_TYPE=gemini
```

**Use OpenAI:**
```env
BRAIN_TYPE=openai
```

Then restart Wednesday.

---

## Files Updated

✅ `assistant/openai_brain.py` - OpenAI integration
✅ `assistant/core.py` - Dual brain support
✅ `assistant/config.py` - Configurable brain type
✅ `.env` - Brain type selector
✅ `requirements.txt` - OpenAI package added
✅ `OPENAI_SETUP.md` - Full OpenAI guide

---

## What's the Same?

Both brains have **identical personality**:
- Casual & friendly
- Same joke style
- Same memory system
- Same skills
- Same workflows

**No difference in experience!** Just different underlying AI.

---

## Which Should I Use?

### Use Gemini If:
- You want it 100% free (Google Free Tier)
- You want faster response times
- You don't want to pay per token

### Use OpenAI If:
- You want slightly better reasoning
- You prefer ChatGPT interface
- You want to try different models
- You like GPT-4

**Recommendation:** Try both! They both work great.

---

## Next Steps

### To Try Gemini (Current)
```bash
python main.py
```
Done! Already working.

### To Try OpenAI

1. **Get API key:** https://platform.openai.com/api-keys
2. **Install:** `pip install openai`
3. **Update .env:**
   ```env
   BRAIN_TYPE=openai
   OPENAI_API_KEY=sk-proj-...
   OPENAI_MODEL=gpt-4o-mini
   ```
4. **Run:** `python main.py`

---

## Testing Both

**Test Gemini:**
```bash
# In .env:
# BRAIN_TYPE=gemini
python main.py
# Type: "Tell me a joke"
```

**Test OpenAI:**
```bash
# In .env:
# BRAIN_TYPE=openai
# OPENAI_API_KEY=sk-proj-...
python main.py
# Type: "Tell me a joke"
# Notice different joke but same personality!
```

---

## Architecture Overview

```
Wednesday
├── Core Engine (Orchestrator)
├── Skills Registry (10 skills)
├── Memory System (Persistent)
└── Brain Selection
    ├── Gemini Brain (Google)
    │   └── Using: google-generativeai
    └── OpenAI Brain (ChatGPT)
        └── Using: openai
```

**Both brains can access all 10 skills!**

---

## Pricing Quick Reference

### Gemini (Google)
- Free: 60 requests/minute
- Paid: $0.075 per 1M input tokens

### OpenAI
- gpt-4o-mini: $0.15 per 1M input tokens
- gpt-4o: $5 per 1M input tokens
- gpt-3.5-turbo: $0.50 per 1M input tokens

**For casual use, both are very cheap!**

---

## API Key Safety

⚠️ **Important:**
- Never commit `.env` to GitHub
- Never share your API keys
- `.env` is in `.gitignore` (protected)
- Keys are kept private in environment variables

---

## Troubleshooting

**"BRAIN_TYPE not recognized"**
→ Update `.env` and save

**"OpenAI API error"**
→ Check your API key is correct
→ Make sure OpenAI is installed: `pip install openai`

**"Both keys missing"**
→ Get Gemini: https://makersuite.google.com/app/apikeys
→ Get OpenAI: https://platform.openai.com/api-keys

**"Brain not switching"**
→ Restart Wednesday: `python main.py`

---

## Advanced: Custom Models

Edit `.env` to use different models:

**OpenAI Options:**
```env
OPENAI_MODEL=gpt-4o-mini        # Recommended (smart & cheap)
OPENAI_MODEL=gpt-4o             # More powerful
OPENAI_MODEL=gpt-4-turbo        # Very powerful but slower
OPENAI_MODEL=gpt-3.5-turbo      # Fastest & cheapest
```

**Gemini Options:**
```env
GEMINI_MODEL=gemini-2.0-flash   # Latest (recommended)
GEMINI_MODEL=gemini-1.5-pro     # Older but solid
```

---

## Summary

**Wednesday now has:**
✅ Gemini Brain (Ready to use)
✅ OpenAI Brain (Ready to switch to)
✅ Easy brain switching (One .env change)
✅ Same personality on both
✅ All 10 skills work with both
✅ Persistent memory on both

**You're all set!** 🚀

**Start with Gemini (already working), or try OpenAI whenever you want.**

---

For detailed OpenAI setup, see: **OPENAI_SETUP.md**
