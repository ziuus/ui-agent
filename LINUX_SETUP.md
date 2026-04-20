# Slovio Agent - Linux Desktop Setup Guide

## Quick Start on Linux Desktop

### Option 1: Using the Launcher Script (Recommended)
```bash
cd /home/zius/Projects/slovioV2/ui-agent
./run.sh
```

### Option 2: From VS Code Terminal
```bash
export DISPLAY=:0
export XAUTHORITY=$HOME/.Xauthority
python main.py
```

### Option 3: With X11 Access Control
```bash
# Allow local X11 connections
xhost +local:

# Then run the agent
cd /home/zius/Projects/slovioV2/ui-agent
python main.py
```

## Troubleshooting

### Issue: "XGetImage() failed" when submitting tasks

**Solution 1: Set DISPLAY Variable**
```bash
# Find your display
echo $DISPLAY
# If empty, try:
export DISPLAY=:0
```

**Solution 2: Check X11 Authorization**
```bash
# Verify .Xauthority file exists
ls -la $HOME/.Xauthority

# Allow local connections
xhost +local:
```

**Solution 3: Check Display Server is Running**
```bash
# List X11 sockets
ls -la /tmp/.X11-unix/

# If you're on Wayland instead:
echo $WAYLAND_DISPLAY
```

## Dashboard Access

Once running, open your browser:
```
http://localhost:8001
```

## Usage Examples

### Chat Mode (Normal LLM)
`What is machine learning?`

### Vision Chat
`What do you see on my screen?`

### Autonomous Tasks
`Open calculator and type 50 + 25 then press equals`
`Open Firefox and go to youtube.com`
`Open a text editor and type Hello World`

### Privacy Mode
`/privacy on` - Blanks screen during task execution
`/privacy off` - Restores screen

### Exit
`/quit` or `exit`

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| DISPLAY not found | Run: `export DISPLAY=:0` |
| XGetImage() failed | Run: `xhost +local:` |
| Wayland vs X11 | Try `/usr/bin/gnome-calculator` directly |
| Screenshot but no automation | Check app is installed (calc, gedit, firefox, etc.) |

## Environment Variables

Set these in `.env` or in your terminal:
```bash
# Required
GEMINI_API_KEY=your_key_here

# Optional
DISPLAY=:0                    # X11 display
XAUTHORITY=$HOME/.Xauthority  # X11 auth
SCREEN_PRIVACY=0              # 0=off, 1=on

DEFAULT_DELAY=2.0
LOG_LEVEL=INFO
```

## Notes

- Agent auto-detects display on startup (tries :0, :1, :10)
- On Wayland systems, X11 compatibility may need xwayland
- For headless servers, use screenshots/xvfb as workaround
- Requires: Python 3.8+, FastAPI, uvicorn, websockets, Google Gemini API key
