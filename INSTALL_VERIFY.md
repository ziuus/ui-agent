# Installation & Verification Checklist ✓

Use this checklist to verify the UI Agent installation is complete and working.

## ✅ Pre-Installation

- [ ] Python 3.8+ installed (`python --version` shows 3.8 or higher)
- [ ] pip is available (`pip --version` works)
- [ ] You're in the project directory: `/home/zius/Projects/slovioV2/ui-agent`
- [ ] All files are present (run: `ls -la ui_agent/`)

### Files & Directories to Check
```bash
# Should show these files:
ls -la ui_agent/
# Should output:
# __init__.py
# __main__.py
# cli.py
# config.py
# vision.py
# automator.py
# utils.py
```

## ✅ Installation Steps

### Step 1: Install Package
```bash
# Navigate to project
cd /home/zius/Projects/slovioV2/ui-agent

# Install (editable mode for development)
pip install -e .

# Note: This reads pyproject.toml and installs all dependencies
```

**Expected Output:**
```
Successfully installed ui-agent-0.1.0 typer rich google-generativeai ...
```

### Step 2: Verify Installation
```bash
# Check if command is available
which ui-agent
# Or on Windows:
where ui-agent

# Should show path like: /usr/local/bin/ui-agent
```

### Step 3: Check Version
```bash
ui-agent --version
# Should output: ui-agent v0.1.0
```

### Step 4: Get Help
```bash
ui-agent --help
# Should show CLI options and commands
```

## ✅ Configuration

### Step 1: Get API Key
```
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key" (or "Gemini API Key")
3. Copy the key (looks like: AIzaSyD...)
4. Keep it safe!
```

### Step 2: Set API Key
**Option A (Environment Variable - Recommended):**
```bash
export GEMINI_API_KEY="your_api_key_here"

# Verify it's set:
echo $GEMINI_API_KEY
# Should output your key
```

**Option B (Using Config Command):**
```bash
ui-agent config --api-key "your_key_here"
```

**Option C (Create .env File):**
```bash
# Create in home directory or project directory:
echo "GEMINI_API_KEY=your_key_here" > ~/.env

# Verify:
cat ~/.env
```

### Step 3: Verify Configuration
```bash
ui-agent config --show

# Should output a table like:
# ┌────────────────┬─────────────────────┐
# │ Setting        │ Value               │
# ├────────────────┼─────────────────────┤
# │ API Key        │ AIzaSyD...          │
# │ Default Delay  │ 2.0s                │
# │ Log Level      │ INFO                │
# └────────────────┴─────────────────────┘
```

## ✅ Dependency Verification

### Check Installed Packages
```bash
pip list | grep -E "typer|rich|google|pyautogui|mss|Pillow|python-dotenv"

# Should show all 7 packages installed with versions
```

### Full Dependency List
- [ ] `typer` ≥ 0.9.0 (CLI framework)
- [ ] `rich` ≥ 13.0.0 (terminal output)
- [ ] `google-generativeai` ≥ 0.3.0 (Gemini API)
- [ ] `pyautogui` ≥ 0.9.53 (mouse/keyboard)
- [ ] `mss` ≥ 9.0.1 (screenshots)
- [ ] `Pillow` ≥ 10.0.0 (image processing)
- [ ] `python-dotenv` ≥ 1.0.0 (.env support)

```bash
# Verify all dependencies:
pip install --requirement requirements.txt

# Should output: Requirement already satisfied for all packages
```

## ✅ Functional Tests

### Test 1: Screenshot Command
```bash
ui-agent screenshot

# Expected output:
# ╭─────────────────────────────╮
# │ 📸 Screenshot               │
# ├─────────────────────────────┤
# │ Resolution     1920×1080    │
# │ Size           ~500 KB      │
# ╰─────────────────────────────╯
```

### Test 2: Save Screenshot
```bash
ui-agent screenshot --output test.png

# Verify file was created:
ls -lh test.png

# Clean up:
rm test.png
```

### Test 3: Config Display
```bash
ui-agent config --show

# Should show all settings with values
```

### Test 4: Help Commands
```bash
ui-agent --help              # Main help
ui-agent click --help        # Click command help
ui-agent type --help         # Type command help
ui-agent screenshot --help   # Screenshot help
ui-agent config --help       # Config help
```

### Test 5: Click Command (Dry Run)
```bash
# Open a browser or application with buttons visible
# Run this (you'll see it wait, then ABORT by moving mouse to corner):
ui-agent click "any visible button name" --delay 3

# Expected behavior:
# 1. Screenshot captured
# 2. "Analyzing..." message
# 3. Table with target coordinates
# 4. 3-second countdown
# 5. If you move mouse to top-left: "Cancelled by user"
```

## ✅ Platform-Specific Checks

### Linux
```bash
# Check X11 is available (for mouse control)
echo $DISPLAY
# Should output something like ":0" or ":1"

# If using Wayland, pyautogui may not work
# Check with: echo $WAYLAND_DISPLAY
```

### macOS
```bash
# Check accessibility permissions (may be required)
# System Preferences → Security & Privacy → Accessibility
# Add your terminal app to the list
```

### Windows
```bash
# Should work out of the box
# Window Terminal or PowerShell recommended
```

## ✅ Troubleshooting Verification

### If Package Won't Install
```bash
# Check pip is up to date:
pip install --upgrade pip

# Try installing with verbose output:
pip install -e . -v

# Check for errors with specific package:
pip install google-generativeai
```

### If Command Not Found
```bash
# Check installation location:
which ui-agent
# Or: where ui-agent (Windows)

# If not found, try adding to PATH:
export PATH=$PATH:~/.local/bin

# Reinstall:
pip install -e .
```

### If API Key Not Working
```bash
# Verify key is set correctly:
echo $GEMINI_API_KEY
# Should show full key, not empty

# Verify key format (should start with "AIza"):
echo $GEMINI_API_KEY | head -c 5

# Try config command:
ui-agent config --show

# If still not working, get a new key from:
# https://makersuite.google.com/app/apikey
```

### If Screenshot/Mouse Fails
```bash
# Test mss (screenshot library):
python3 -c "import mss; print(mss.mss().monitors[1])"

# Test pyautogui (mouse control):
python3 -c "import pyautogui; print(pyautogui.position())"

# For Linux, verify X11:
echo $DISPLAY
```

## ✅ Complete Verification Script

Run this to verify everything:

```bash
#!/bin/bash
echo "🤖 UI Agent Verification"
echo "========================"
echo ""

# Check Python
echo -n "Python: "
python3 --version

# Check installation
echo -n "CLI: "
which ui-agent || echo "NOT INSTALLED"

# Check version
echo -n "Version: "
ui-agent --version 2>/dev/null || echo "FAILED"

# Check dependencies
echo -n "Dependencies: "
pip list | grep -c "typer\|rich\|google" 2>/dev/null || echo "FAILED"

# Check API key
echo -n "API Key: "
[ -n "$GEMINI_API_KEY" ] && echo "SET" || echo "NOT SET"

# Try screenshot
echo -n "Screenshot: "
ui-agent screenshot >/dev/null 2>&1 && echo "OK" || echo "FAILED"

# Config
echo -n "Config: "
ui-agent config --show >/dev/null 2>&1 && echo "OK" || echo "FAILED"

echo ""
echo "✓ Verification complete!"
```

Save as `verify.sh` and run:
```bash
bash verify.sh
```

## ✅ Performance Baseline

Run these to establish baseline performance:

```bash
# Time a screenshot
time ui-agent screenshot > /dev/null

# Time a click command (will wait 1 second then abort)
time ui-agent click "test" --delay 0.5 --no-failsafe 2>/dev/null || true

# Should take 1-3 seconds total including delay
```

## ✅ First Real Command

When everything is verified:

```bash
# 1. Open any application with a button visible
# 2. Run:
ui-agent click "name of button"

# 3. Watch what happens:
#    - Screenshot captured
#    - Element analyzed by Gemini
#    - Coordinates displayed
#    - Mouse moves to button (after delay)
#    - Click executed

# 4. Success! ✓
```

## 📋 Pre-Flight Checklist

Before using in production, verify:

- [ ] Python 3.8+ installed
- [ ] Package installed with `pip install -e .`
- [ ] `ui-agent --version` works
- [ ] API key is set and verified
- [ ] `ui-agent config --show` displays correctly
- [ ] `ui-agent screenshot` works
- [ ] Tested click command with `--delay 3` to verify abort
- [ ] Read README.md for all features
- [ ] Understand safety features (failsafe, delay)

## ✅ You're Ready When

- ✓ All checklist items are checked
- ✓ `ui-agent --help` shows without error
- ✓ `ui-agent config --show` displays API key
- ✓ `ui-agent screenshot` captures screen size
- ✓ API key is available and validated

## 📞 Support

If any verification fails:

1. Read the error message carefully
2. Check the Troubleshooting section above
3. Review [README.md](README.md) for detailed info
4. Run with `-v` (verbose) flag: `ui-agent click "button" -v`
5. Check Python/pip versions

---

**Next: Try your first command!**

```bash
ui-agent click "any visible button"
```

Good luck! 🚀
