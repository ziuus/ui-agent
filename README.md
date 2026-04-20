# UI Agent 🤖

A polished, production-ready CLI tool for **vision-powered UI automation**. Point and click any UI element using natural language descriptions—powered by Google Gemini 1.5 Flash's free Vision API.

```
$ ui-agent click "Login button"
$ ui-agent click "Search input" --delay 1.5
$ ui-agent type "hello@example.com"
$ ui-agent type "MyPassword123" --interval 0.1
```

## Features

✨ **Vision-Powered Element Location** — Describe any UI element naturally ("red save button", "email input field") and Gemini finds it  
⚡ **Lightning Fast** — Uses free Gemini 1.5 Flash API (0.075¢ per 1M input tokens)  
🛡️ **Safety-First Design** — Built-in failsafe, configurable delays, human confirmation  
🎨 **Beautiful CLI** — Rich formatting, spinners, progress indicators  
🌐 **Cross-Platform** — Works on Windows, macOS, Linux  
📦 **Zero Config** — Just set `GEMINI_API_KEY` and go  
⌨️ **Keyboard + Mouse** — Click elements or type text with precision  

## Installation

### Prerequisites

- **Python 3.8+** (check with `python --version`)
- **Free Google Gemini API Key** (from [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey))

### Option 1: Fast Install (Recommended)

```bash
# Clone/download the repository
cd ui-agent

# Install globally with pip
pip install -e .

# Verify installation
ui-agent --version
```

### Option 2: Install from PyPI (Future)

```bash
pip install ui-agent
```

### Option 3: Virtual Environment (Development)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with dependencies
pip install -r requirements.txt

# Run from within repo
python -m ui_agent --version
```

## Setup

### 1. Get a Free API Key

Visit [Google AI Studio](https://makersuite.google.com/app/apikey) and create a new API key. It's completely free for testing.

### 2. Configure the API Key

**Option A: Environment Variable (Recommended)**
```bash
export GEMINI_API_KEY="your_api_key_here"
# Add to ~/.bashrc or ~/.zshrc to make permanent
```

**Option B: .env File**
```bash
# Create .env in your working directory
cd ~
cat > .env << EOF
GEMINI_API_KEY=your_api_key_here
EOF
```

**Option C: Use the Config Command**
```bash
ui-agent config --api-key "your_api_key_here"
```

### 3. Verify Setup

```bash
ui-agent config --show
# Should display your API key (first 20 chars) and settings
```

## Usage

### Click Command

Find and click any UI element using a natural language description.

```bash
# Basic usage
ui-agent click "Submit button"

# With custom delay (default: 2.0s)
ui-agent click "Login button" --delay 1.5

# With verbose output
ui-agent click "Search field" -v

# Disable failsafe
ui-agent click "Element" --no-failsafe
```

**How it works:**
1. Takes a screenshot of your current screen
2. Sends it to Gemini 1.5 Flash with your description
3. API returns exact coordinates of the element
4. Waits for your confirmation (delay period)
5. Moves mouse to center and clicks

**Safety:**
- Move your mouse to the **top-left corner** anytime to abort
- You have `--delay` seconds (default 2s) to inspect before clicking
- Always shows you what it's about to click

### Type Command

Type text directly (useful after clicking an input field).

```bash
# Simple text
ui-agent type "Hello, World!"

# With password (slower typing to be detected)
ui-agent type "MyPassword123" --interval 0.2

# With delay before typing
ui-agent type "user@example.com" --delay 0.5 --interval 0.05
```

**Options:**
- `--delay` / `-d`: Wait N seconds before typing starts (default: 1.0)
- `--interval` / `-i`: Delay between typed characters (default: 0.05)

### Screenshot Command

Capture current screen and optionally save to file.

```bash
# Just capture and display info
ui-agent screenshot

# Save to file
ui-agent screenshot --output screen.png
```

### Config Command

Manage settings and verify setup.

```bash
# Show current configuration
ui-agent config --show

# Set API key interactively
ui-agent config --api-key "your_key"
```

## Examples

### Example 1: Login Flow

```bash
# Click email field
ui-agent click "Email input field" --delay 1.5

# Type email
ui-agent type "user@example.com" --interval 0.05

# Tab to password field (via keyboard would be added in future)
ui-agent click "Password input field"

# Type password
ui-agent type "SecurePassword123" --interval 0.1

# Click login button
ui-agent click "Login button" --delay 2.0
```

### Example 2: Form Filling

```bash
ui-agent click "First Name field"
ui-agent type "John" --interval 0.05

ui-agent click "Last Name field"
ui-agent type "Doe" --interval 0.05

ui-agent click "Submit button"
```

### Example 3: Web Search

```bash
ui-agent click "Google search box"
ui-agent type "how to build ai agents" --interval 0.03
ui-agent click "Google Search button"
```

## Advanced Options

### Custom Delays

```bash
# Slow delay for safety
ui-agent click "Dangerous button" --delay 5.0

# Fast confirmation for known elements
ui-agent click "Simple link" --delay 0.5
```

### Character Typing Intervals

```bash
# Fast typing (detected by some systems)
ui-agent type "text" --interval 0.01

# Human-like typing
ui-agent type "text" --interval 0.05

# Very slow (for analysis)
ui-agent type "text" --interval 0.5
```

### Verbose Output

```bash
# See detailed information during execution
ui-agent click "Element" --verbose

ui-agent type "text" -v
```

## How It Works

### Vision Flow (Click Command)

```
[Screenshot] → [Gemini 1.5 Flash] → [Bounding Box]
    ↓
[Normalize 0-1000] → [Map to Screen Coords] → [Move Mouse] → [Click]
    ↓
[Wait for Delay] → [User Aborts or Confirm?]
```

### Coordinate System

Gemini returns normalized coordinates `[ymin, xmin, ymax, xmax]` on a 0-1000 scale:
- `(0, 0)` = top-left corner
- `(1000, 1000)` = bottom-right corner
- UI Agent automatically maps these to your actual screen resolution

### Safety Mechanisms

1. **Failsafe Enabled** — Move mouse to top-left to abort anytime
2. **Delay Before Action** — Default 2 seconds to review
3. **Clear Feedback** — Shows target coordinates and element info
4. **Error Handling** — Gracefully handles API failures and invalid responses

## Troubleshooting

### "GEMINI_API_KEY not configured"

```bash
# Make sure your key is set
echo $GEMINI_API_KEY  # Should print your key

# Or set it
export GEMINI_API_KEY="your_key"
ui-agent click "element"
```

### "Element not found"

- The element description might be too vague: try "blue button with checkmark" instead of just "button"
- The element might be off-screen or hidden
- Try taking a screenshot first: `ui-agent screenshot`

### "Invalid API response"

- Your API key might be wrong or expired
- You might be rate-limited (wait a moment and retry)
- Check your Gemini API quota

### Mouse not moving

- On Linux: requires X11 (not Wayland). Configure Wayland if needed
- Ensure no other application is controlling the mouse
- Use `--no-failsafe` carefully (limits safety checks)

### Typing not working

- Make sure the target input field is focused first: `ui-agent click "input field"`
- Try slower intervals: `--interval 0.1`
- Some systems may require special handling for special characters

## Global Installation

### Linux / macOS

```bash
# Install globally for current user
pip install -e .

# Verify it's in your PATH
which ui-agent

# Use anywhere
cd ~/Desktop
ui-agent click "Element"
```

### Windows

```bash
# Install globally
pip install -e .

# Verify it works
ui-agent --version

# Use in any Command Prompt/PowerShell
ui-agent click "Element"
```

## Project Structure

```
ui-agent/
├── ui_agent/
│   ├── __init__.py           # Package exports
│   ├── __main__.py           # Entry point
│   ├── cli.py                # Typer CLI commands
│   ├── config.py             # Configuration management
│   ├── vision.py             # Gemini Vision integration
│   ├── automator.py          # Mouse/keyboard control
│   └── utils.py              # Utility functions
├── pyproject.toml            # Modern Python packaging
├── setup.py                  # Legacy setup
├── requirements.txt          # Pip dependencies
├── .env.example              # Example configuration
└── README.md                 # This file
```

## Dependencies

| Package | Purpose | License |
|---------|---------|---------|
| `google-generativeai` | Gemini Vision API | Apache 2.0 |
| `typer` | CLI framework | MIT |
| `rich` | Terminal output | MIT |
| `pyautogui` | Mouse/keyboard control | BSD |
| `mss` | Screenshot capture | MIT |
| `pillow` | Image processing | HPND |
| `python-dotenv` | .env file support | BSD |

## Limitations & Future Features

### Current Limitations
- Only supports primary monitor (multi-monitor support planned)
- No keyboard-only navigation yet (mouse-based only)
- Regex-based coordinates (not pixel-perfect for rotated/scaled displays)

### Planned Features
- 🎯 Multiple monitor support
- ⌨️ Keyboard navigation (Tab, Enter, etc.)
- 🔄 Command chaining / scripting
- 📊 Action replay/macros
- 🎬 Screen recording integration
- 🔐 Secure credential handling
- 🌍 Multi-language support

## Performance

**Typical Execution Time:**
- Screenshot capture: ~50-200ms
- API request: ~1-2 seconds (Gemini 1.5 Flash is fast)
- Mouse movement: ~200-500ms
- **Total with 2s delay: ~3-5 seconds**

## Cost

Using free tier of Gemini API:
- **1M input tokens**: ~$0.075
- Average request: ~500-1000 tokens (depends on image size)
- **Cost per click**: < $0.001 (essentially free for testing)

## Security Considerations

- API key is stored in environment or .env file
- Screenshots are sent to Google's servers (review privacy policy)
- Consider using environment variables in production rather than .env files
- Never commit API keys to version control
- Use `.env` in `.gitignore`

## Contributing

Contributions welcome! Areas for help:
- Multi-monitor support
- Additional vision models
- Performance optimizations
- Documentation improvements

## License

MIT License — See LICENSE file for details

## Support & Issues

- 📚 Read the README sections above
- 🐛 Check existing GitHub issues
- 💬 Create a new issue with details about what you're trying to do
- 💭 Include: Python version, OS, error message, and command used

---

**Built with ❤️ using Gemini 1.5 Flash**
