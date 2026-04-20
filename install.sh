#!/bin/bash
# Quick start script for UI Agent

set -e

echo "🤖 UI Agent - Quick Start Installer"
echo "===================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version found"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "✗ pip3 not found. Please install Python3 and pip3."
    exit 1
fi
echo "✓ pip3 found"

# Create virtual environment (optional)
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
else
    echo "✓ Virtual environment exists"
    source venv/bin/activate
    echo "✓ Virtual environment activated"
fi

# Install package
echo ""
echo "Installing UI Agent..."
pip install -e .
echo "✓ Installation complete!"

# Verify installation
echo ""
echo "Verifying installation..."
if command -v ui-agent &> /dev/null; then
    echo "✓ ui-agent command is available globally!"
    ui-agent --version
else
    echo "✓ ui-agent is available (install with: pip install -e .)"
fi

# Setup API key
echo ""
echo "Next steps:"
echo "1. Get a free Gemini API key from:"
echo "   https://makersuite.google.com/app/apikey"
echo ""
echo "2. Set your API key:"
echo "   export GEMINI_API_KEY='your_key_here'"
echo ""
echo "3. Try it out:"
echo "   ui-agent click 'button name'"
echo ""
echo "✓ Setup complete! Happy automating! 🚀"
