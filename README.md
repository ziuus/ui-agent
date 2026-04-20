# 🖱️ UI Agent

> **Autonomous Desktop Automation — A vision-powered agentic CLI for intelligent "Computer Use" and UI orchestration.**

UI Agent is a production-ready, high-fidelity automation tool that bridges the gap between natural language intent and native desktop interaction. By leveraging **Gemini-1.5 Flash Vision**, it autonomously navigates, clicks, and types within any local application, providing a zero-friction interface for complex multi-app workflows and system management.

## ⚡ Core Features

- **Vision-Powered Detection**: Describe any UI element in natural language ("the blue submit button in the top right") and let the AI resolve exact coordinates via real-time screen analysis.
- **Agentic Orchestration**: High-fidelity execution of mouse and keyboard events with configurable kinetic delays and safety failsafes.
- **Multi-OS Intelligence**: Native support for Linux, Windows, and macOS with resolution-aware coordinate mapping.
- **Professional CLI**: Polished terminal interface powered by `typer` and `rich`, complete with status indicators, spinners, and formatted tables.
- **Safety First**: Integrated fail-safe protocols—instantly abort any action by moving the mouse to a screen corner.

## 🛠 Tech Stack

- **Engine**: Python 3.10+
- **Intelligence**: Google Gemini-1.5 Flash (Vision API)
- **Automation**: PyAutoGUI + MSS (Screen Capture)
- **CLI**: Typer + Rich
- **Packaging**: Modern PEP 517/518 standards

## 🚀 Getting Started

1. **Global Installation**:
   ```bash
   pip install .
   ```

2. **Configure Environment**:
   ```bash
   export GEMINI_API_KEY="your_key_here"
   ```

3. **Execute Command**:
   ```bash
   ui-agent click "Open the web browser"
   ```

## 📂 Project Structure

- `ui_agent/cli.py`: Primary command interface and logic.
- `ui_agent/vision.py`: Gemini Vision integration and element detection.
- `ui_agent/automator.py`: Kinetic mouse and keyboard control.

---
*UI Agent: Connecting Human Intent to Machine Execution.*
