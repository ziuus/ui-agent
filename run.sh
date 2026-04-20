#!/bin/bash
# Slovio Agent Launcher with X11 Environment Setup

# Auto-detect DISPLAY if not set
if [ -z "$DISPLAY" ]; then
    # Try common X11 displays
    for d in :0 :1 :10; do
        if [ -S /tmp/.X11-unix$(echo $d | sed 's/:/-/') ] 2>/dev/null; then
            export DISPLAY="$d"
            break
        fi
    done
fi

# Set XAUTHORITY if not set
if [ -z "$XAUTHORITY" ]; then
    export XAUTHORITY=$HOME/.Xauthority
fi

# Allow local X11 connections (if xhost available)
if command -v xhost &> /dev/null; then
    xhost +local: >/dev/null 2>&1 || true
fi

echo "Starting Slovio Agent..."
echo "  DISPLAY: $DISPLAY"
echo "  XAUTHORITY: $XAUTHORITY"
echo "  Dashboard: http://localhost:8001"
echo ""

# Run the agent
cd "$(dirname "$0")"
/home/zius/Projects/slovioV2/.venv/bin/python main.py
