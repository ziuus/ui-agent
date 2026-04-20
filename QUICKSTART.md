# UI Agent - Quick Start Guide ⚡

## 🎯 What You Built

A production-ready **Vision-Powered UI Automation CLI** that:
- Takes screenshots and analyzes them with Gemini 1.5 Flash
- Finds UI elements using plain English descriptions  
- Clicks buttons, types text, and automates workflows
- Works cross-platform (Windows, macOS, Linux)
- Is completely free to use (free Gemini API tier)

## 📦 Project Contents

```
ui-agent/
├── ui_agent/                  # Main package
│   ├── cli.py                 # Command-line interface (Typer)
│   ├── vision.py              # Gemini integration
│   ├── automator.py           # Mouse/keyboard control
│   ├── config.py              # Configuration management
│   ├── utils.py               # Utilities
│   ├── __init__.py
│   └── __main__.py
├── pyproject.toml             # Modern Python packaging (PEP 517/518)
├── setup.py                   # Backward-compatible setup
├── requirements.txt           # Dependencies for pip
├── README.md                  # Full documentation (50+ sections)
├── EXAMPLES.md                # Usage examples
├── QUICKSTART.md              # This file
├── LICENSE                    # MIT License
├── example_usage.py           # Programmatic usage example
├── install.sh                 # Linux/macOS installer
├── install.bat                # Windows installer
├── .env.example               # Configuration template
└── .gitignore                 # Git ignore rules
```

## 🚀 Installation (5 Minutes)

### Step 1: Get the Code
Already done! You're in `/home/zius/Projects/slovioV2/ui-agent`

### Step 2: Get a Free API Key
Visit: [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
- Click "Create API Key"
- Copy your key (looks like: `AIzaSyD...`)

### Step 3: Install Globally

**On Linux/macOS:**
```bash
cd /home/zius/Projects/slovioV2/ui-agent
bash install.sh
```

**On Windows:**
```cmd
cd C:\Path\To\ui-agent
install.bat
```

**Or manually:**
```bash
pip install -e .
```

### Step 4: Configure API Key

**Option A (Recommended):**
```bash
export GEMINI_API_KEY="your_key_here"
# Add to ~/.bashrc or ~/.zshrc to make permanent
```

**Option B (Simpler):**
```bash
# Windows
set GEMINI_API_KEY=your_key_here

# Linux/macOS
export GEMINI_API_KEY=your_key_here
```

**Option C (Persistent):**
```bash
ui-agent config --api-key "your_key_here"
```

### Step 5: Verify Setup
```bash
ui-agent config --show
```

Should show your API key (first 20 chars) and settings.

## 💡 Your First Command

### Simple Click
```bash
# Open any application with a button visible
ui-agent click "Settings button"
```

You'll see:
1. ✓ Screenshot captured
2. ✓ Sending to Gemini...
3. A table showing the target coordinates
4. 2-second delay (move mouse to top-left to abort)
5. ✓ Click executed!

### Type Some Text
```bash
# First click an input field
ui-agent click "Email input"

# Then type
ui-agent type "hello@example.com"
```

## 📚 Core Commands

### `click` - Find and click UI elements
```bash
ui-agent click "Login button"                    # Basic
ui-agent click "Submit button" --delay 3        # Custom delay
ui-agent click "Element" -v                      # Verbose
ui-agent click "Element" --no-failsafe           # Advanced
```

**Options:**
- `--delay` / `-d`: Wait before clicking (0.5-10s, default: 2s)
- `--verbose` / `-v`: Show detailed output
- `--no-failsafe`: Disable safety checks (not recommended)

### `type` - Enter text  
```bash
ui-agent type "Hello, World!"                    # Basic
ui-agent type "password" --interval 0.1          # Slower typing
ui-agent type "text" --delay 0.5                 # Custom delay
ui-agent type "text" --interval 0.05 -v          # Verbose
```

**Options:**
- `--delay` / `-d`: Wait before typing (0-10s, default: 1s)
- `--interval` / `-i`: Pause between chars (0-1s, default: 0.05s)
- `--verbose` / `-v`: Show details

### `screenshot` - Capture screen
```bash
ui-agent screenshot                              # Display info
ui-agent screenshot --output screen.png          # Save to file
```

### `config` - Manage settings
```bash
ui-agent config --show                           # View current config
ui-agent config --api-key "new_key"              # Set API key
```

## 🎬 Practical Examples

### Login to Gmail
```bash
ui-agent click "Email or phone field"
ui-agent type "your.email@gmail.com" --interval 0.05

ui-agent click "Next button"

ui-agent click "Password field"  
ui-agent type "YourPassword123" --interval 0.1

ui-agent click "Next button"
```

### Fill a Web Form
```bash
# First name
ui-agent click "First Name input"
ui-agent type "John" --interval 0.03

# Last name
ui-agent click "Last Name input"
ui-agent type "Doe" --interval 0.03

# Email
ui-agent click "Email input"
ui-agent type "john@example.com" --interval 0.02

# Submit
ui-agent click "Submit button"
```

### Google Search
```bash
ui-agent click "Google search box"
ui-agent type "how to build an ai agent" --interval 0.02

ui-agent click "Search button"
```

## 🛡️ Safety Features

### Failsafe (Default Enabled)
- **Move your mouse to the top-left corner** anytime to abort
- Works even while waiting

### Delay Before Action
- Default: 2 seconds
- Gives you time to review coordinates before clicking
- Increase with `--delay` for safety, decrease for speed

### Clear Feedback
```
╭───────────────────────────────────╮
│ Click Target                      │
├──────────────────────────────────┤
│ Description      Login button    │
│ Bounding Box     (150, 100) → (2  │
│ Center Point     (240, 150)      │
│ Size             180 × 100 px    │
│ Delay            2s              │
╰───────────────────────────────────╯
```

## 🔧 Advanced Tips

### Slow Typing (Better Detection)
```bash
ui-agent type "password" --interval 0.15  # 150ms between chars
```

### Fast Typing (Risky)
```bash
ui-agent type "fast text" --interval 0.01  # 10ms between chars
```

### Immediate Clicks (Risky)
```bash
ui-agent click "Element" --delay 0.5  # Only 0.5s to abort
```

### Better Descriptions
```bash
# ❌ Bad
ui-agent click "button"

# ✅ Good
ui-agent click "blue login button in top right"

# ✓ Best
ui-agent click "red submit button with checkmark icon"
```

### Using as Python Library
```python
from ui_agent.config import Config
from ui_agent.vision import VisionAnalyzer
from ui_agent.automator import UIAutomator
from ui_agent.utils import get_screenshot_bytes_and_dims

# Get screenshot
screenshot_bytes, width, height = get_screenshot_bytes_and_dims()

# Find element
config = Config()
analyzer = VisionAnalyzer(config.get_api_key())
ymin, xmin, ymax, xmax = analyzer.locate_element(screenshot_bytes, "button")

# Click it
automator = UIAutomator()
automator.click_at_normalized_coords((ymin, xmin, ymax, xmax), width, height)
```

See `example_usage.py` for complete examples.

## ⚙️ Configuration

### Environment Variables
```bash
# Required
GEMINI_API_KEY=your_key

# Optional
DEFAULT_DELAY=2.0           # Default delay before actions
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR
```

### .env File
Create in your home directory or project root:
```env
GEMINI_API_KEY=AIzaSyD...
DEFAULT_DELAY=2.0
LOG_LEVEL=INFO
```

## 📊 Technical Details

### Coordinate System
- Gemini returns normalized coordinates on 0-1000 scale
- `(0, 0)` = top-left corner
- `(1000, 1000)` = bottom-right corner
- UI Agent automatically maps to your screen resolution

### Bounding Box Format
- Gemini returns: `[ymin, xmin, ymax, xmax]`
- Y axis: top-to-bottom (0 at top)
- X axis: left-to-right (0 at left)
- UI Agent converts to pixel coordinates internally

### Performance
- Screenshot: ~50-200ms
- API call: ~1-2s (Gemini 1.5 Flash)
- Mouse movement: ~300ms
- **Total with 2s delay: ~3-5 seconds**

### Costs
- **Free tier:** 1,500 requests/minutes
- **Average cost:** < $0.001 per action
- Essentially free for testing and light automation

## 🐛 Troubleshooting

### "Element not found"
```bash
# Make description more specific
ui-agent click "blue 'Save' button with star icon"

# Use verbose mode to see the API response
ui-agent click "element" --verbose

# Try a screenshot to verify element is visible
ui-agent screenshot --output current.png
```

### "GEMINI_API_KEY not configured"
```bash
# Check your key is set
echo $GEMINI_API_KEY

# If empty, set it
export GEMINI_API_KEY="your_key"

# Or use config command
ui-agent config --api-key "your_key"
```

### "API rate limited"
```bash
# Wait a moment and retry (or get premium API key)
sleep 60
ui-agent click "element"
```

### Mouse not clicking
```bash
# On some systems, need longer delay
ui-agent click "element" --delay 3.0

# Or try with failsafe disabled (not recommended)
ui-agent click "element" --no-failsafe
```

### Typing not working
```bash
# Make sure field is focused first
ui-agent click "input field"
ui-agent type "text" --delay 0.5

# Try slower typing
ui-agent type "text" --interval 0.2  # 200ms between chars
```

## 📚 Further Reading

- **Full Docs:** See [README.md](README.md)
- **Examples:** See [EXAMPLES.md](EXAMPLES.md)  
- **API Reference:** Run `ui-agent --help`
- **Gemini API:** [makersuite.google.com](https://makersuite.google.com)

## 🎓 What You Learned

This project demonstrates:
- ✅ Modern Python packaging (PEP 517/518)
- ✅ Professional CLI with Typer
- ✅ Vision API integration (Gemini)
- ✅ Cross-platform automation (pyautogui, mss)
- ✅ Rich terminal output
- ✅ Configuration management
- ✅ Error handling & validation
- ✅ Human-in-the-loop safety

## 🚀 Next Steps

1. **Try it out** - Run `ui-agent click "button"` on your screen
2. **Explore examples** - Check [EXAMPLES.md](EXAMPLES.md)
3. **Automate a workflow** - Chain multiple commands together
4. **Use as library** - Import `ui_agent` in your own code
5. **Contribute** - Add features, improve docs, report issues

---

**Ready to automate? Run your first command:**
```bash
ui-agent click "any button on screen"
```

Happy automating! 🎯🤖
