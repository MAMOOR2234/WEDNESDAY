# 🚀 Wednesday - OpenAI Integration Guide

## Overview

Wednesday now supports **two AI brains**:
- 🔵 **Gemini** (Google) - Default
- 🟢 **OpenAI** (ChatGPT) - Alternative

Choose your favorite! Both work exactly the same way.

---

## Getting Started with OpenAI

### Step 1: Get OpenAI API Key

1. **Visit:** https://platform.openai.com/api-keys
2. **Sign in** with your OpenAI account (create if needed)
3. **Click:** "Create new secret key"
4. **Copy** the key
5. **Save** it safely

### Step 2: Update `.env` File

Edit `.env` in your WEDNESDAY folder:

```env
# Change brain type to OpenAI
BRAIN_TYPE=openai

# Add your OpenAI API key
OPENAI_API_KEY=sk-proj-your-actual-key-here

# Choose your model
OPENAI_MODEL=gpt-4o-mini
```

### Step 3: Install OpenAI Package

```bash
pip install openai
```

### Step 4: Run Wednesday

```bash
python main.py
```

That's it! Wednesday will now use ChatGPT as her brain. 🧠

---

## OpenAI Models Available

### Recommended Models

| Model | Speed | Quality | Cost | Best For |
|-------|-------|---------|------|----------|
| **gpt-4o-mini** | Fast | High | Low | ⭐ Recommended |
| **gpt-4o** | Medium | Very High | Medium | Powerful tasks |
| **gpt-4-turbo** | Medium | Very High | High | Complex reasoning |
| **gpt-3.5-turbo** | Very Fast | Good | Very Low | Budget option |

### Configuration Examples

**Fast & Cheap (Default)**
```env
OPENAI_MODEL=gpt-4o-mini
```

**Most Powerful**
```env
OPENAI_MODEL=gpt-4o
```

**Budget Option**
```env
OPENAI_MODEL=gpt-3.5-turbo
```

---

## Switching Between Brains

### Use Gemini
```env
BRAIN_TYPE=gemini
GEMINI_API_KEY=your_gemini_key_here
```

### Use OpenAI
```env
BRAIN_TYPE=openai
OPENAI_API_KEY=your_openai_key_here
```

**Then restart Wednesday:**
```bash
python main.py
```

---

## Cost Comparison

### OpenAI Pricing (approx.)
- **gpt-4o-mini:** $0.15 per 1M input tokens
- **gpt-4o:** $5 per 1M input tokens
- **gpt-3.5-turbo:** $0.50 per 1M input tokens

### Gemini Pricing
- **Free tier:** 60 requests/minute
- **Paid:** $0.075 per 1M input tokens

### Budget Tips
- Use **gpt-4o-mini** for best value
- Set smaller context windows in code if needed
- Monitor usage at: https://platform.openai.com/account/usage

---

## Troubleshooting

### Error: "openai package not installed"
```bash
pip install openai
```

### Error: "Invalid API key"
1. Check .env has correct key (starts with `sk-proj-`)
2. Verify key hasn't expired at https://platform.openai.com/api-keys
3. Make sure file is saved

### Error: "Rate limit exceeded"
- Free trial has limits
- Wait a minute and try again
- Or upgrade your OpenAI account

### Error: "API key not found"
```env
# Make sure this is set:
OPENAI_API_KEY=sk-proj-xxxxx
BRAIN_TYPE=openai
```

### Slow Responses
- Try **gpt-3.5-turbo** for faster responses
- Or reduce context size in the brain code

---

## Performance Comparison

### Response Quality

**Gemini 2.0 Flash:**
- Fast and conversational
- Great for casual chat
- Good balance

**OpenAI GPT-4o-mini:**
- Very smart
- Better understanding
- Slight edge in reasoning

**OpenAI GPT-4o:**
- Most intelligent
- Best reasoning
- Slower and more expensive

### Speed

**Fastest → Slowest:**
1. gpt-3.5-turbo (OpenAI)
2. gpt-4o-mini (OpenAI)
3. Gemini 2.0 Flash (Google)
4. gpt-4o (OpenAI)
5. gpt-4-turbo (OpenAI)

---

## Using Both Brains

You can have both keys configured! Just switch which brain to use:

```env
# Both keys configured
GEMINI_API_KEY=AIzaSy...
OPENAI_API_KEY=sk-proj-...

# Choose which to use:
BRAIN_TYPE=gemini     # Use Gemini
# or
BRAIN_TYPE=openai     # Use OpenAI
```

---

## Features Supported by Both

✅ Casual friendly personality
✅ Multi-step reasoning
✅ Skill execution
✅ Conversation memory
✅ Web search
✅ File operations
✅ App control
✅ Reminders & notes
✅ Weather
✅ Screenshots
✅ Workflows

**Both brains are feature-complete!**

---

## Pro Tips

### 1. Start with gpt-4o-mini
```env
OPENAI_MODEL=gpt-4o-mini  # Best value for money
```

### 2. Use Gemini for Free
```env
BRAIN_TYPE=gemini  # Free tier available
```

### 3. Monitor Your Costs
Visit: https://platform.openai.com/account/usage

### 4. Switch Between Brains
A/B test to see which you prefer!

### 5. Combine with Advanced Memory
Wednesday's memory works with both brains!

---

## Example .env Configurations

### OpenAI (Budget)
```env
BRAIN_TYPE=openai
OPENAI_API_KEY=sk-proj-xxxxx
OPENAI_MODEL=gpt-3.5-turbo
```

### OpenAI (Recommended)
```env
BRAIN_TYPE=openai
OPENAI_API_KEY=sk-proj-xxxxx
OPENAI_MODEL=gpt-4o-mini
```

### OpenAI (Premium)
```env
BRAIN_TYPE=openai
OPENAI_API_KEY=sk-proj-xxxxx
OPENAI_MODEL=gpt-4o
```

### Gemini (Free)
```env
BRAIN_TYPE=gemini
GEMINI_API_KEY=AIzaSy...
```

---

## Comparing Responses

Same question, different brains:

**You:** "Tell me a joke"

**Gemini:** "Why don't scientists trust atoms? Because they make up everything! 😂"

**GPT-4o-mini:** "Why did the scarecrow win an award? He was outstanding in his field! 🌾"

**Both funny, different styles!**

---

## Advanced: Customize Brain Behavior

Edit `assistant/openai_brain.py` to change:
- Temperature (creativity): 0.8 (default) → 0.5 (less creative) or 1.0 (more creative)
- Max tokens: 500 (default) → adjust response length
- System prompt: Make Wednesday behave differently

```python
# In openai_brain.py around line 100:
response = self.client.chat.completions.create(
    model=self.config.openai_model,
    messages=messages,
    temperature=0.8,      # ← Adjust this (0-1)
    max_tokens=500        # ← Or this
)
```

---

## FAQ

**Q: Which brain is better?**
A: Both are great! Try both and see which you prefer.

**Q: Is OpenAI faster?**
A: gpt-3.5-turbo is fast, but GPT-4 models are slower but smarter.

**Q: Can I use both at the same time?**
A: You can switch between them by changing BRAIN_TYPE.

**Q: Do I need both API keys?**
A: Only one at a time. Get both if you want to switch later.

**Q: What if I run out of OpenAI credits?**
A: Switch to Gemini free tier or add billing to your OpenAI account.

**Q: Is the personality different?**
A: Personality is the same! Both follow the same friendly prompt.

---

## Next Steps

1. **Get OpenAI API key** from https://platform.openai.com/api-keys
2. **Update .env:**
   ```env
   BRAIN_TYPE=openai
   OPENAI_API_KEY=your_key_here
   OPENAI_MODEL=gpt-4o-mini
   ```
3. **Install package:**
   ```bash
   pip install openai
   ```
4. **Run Wednesday:**
   ```bash
   python main.py
   ```

**Enjoy your upgraded AI assistant!** 🚀

---

## Summary

| Aspect | Gemini | OpenAI |
|--------|--------|--------|
| API Key | Free tier | $5+ (paid) |
| Setup | Easy | Easy |
| Intelligence | Great | Excellent |
| Speed | Fast | Varies |
| Cost | Cheap | Moderate |
| Personality | Friendly | Friendly |

**Wednesday now supports both!** Choose based on your preferences. 🤖✨
