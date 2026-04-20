"""Unified launcher for Slovio Agent TUI + web dashboard."""

from __future__ import annotations

import os
import subprocess
import sys
import threading
import time

import uvicorn
from rich.console import Console

from .brain import AgentBrain
from .config import Config
from .runtime import AgentRuntime
from .server import create_app
from .tui import term_loop


console = Console()


def _setup_x11_environment() -> None:
    """Auto-detect and configure X11 display for GUI automation."""
    if not os.environ.get("DISPLAY"):
        for display in (":0", ":1", ":10"):
            try:
                result = subprocess.run(
                    ["xset", "q"],
                    env={**os.environ, "DISPLAY": display},
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=1,
                )
                if result.returncode == 0:
                    os.environ["DISPLAY"] = display
                    break
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue

    if not os.environ.get("XAUTHORITY"):
        home = os.path.expanduser("~")
        xauth = os.path.join(home, ".Xauthority")
        if os.path.exists(xauth):
            os.environ["XAUTHORITY"] = xauth


def _run_server(runtime: AgentRuntime, stop_event: threading.Event) -> None:
    app = create_app(runtime, stop_event)
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")


def main() -> None:
    _setup_x11_environment()
    config = Config()
    if not config.validate_api_key():
        console.print("[red]GEMINI_API_KEY is missing. Set it in .env or environment.[/red]")
        return

    runtime = AgentRuntime()
    stop_event = threading.Event()
    brain = AgentBrain(runtime=runtime, config=config)

    worker_thread = threading.Thread(
        target=brain.run_command_worker,
        args=(stop_event,),
        name="slovio-brain",
        daemon=True,
    )
    server_thread = threading.Thread(
        target=_run_server,
        args=(runtime, stop_event),
        name="slovio-server",
        daemon=True,
    )

    worker_thread.start()
    server_thread.start()

    runtime.add_log("info", "Web dashboard available at http://localhost:8001")

    try:
        # Only start TUI if stdout is a TTY (interactive terminal)
        if sys.stdout.isatty():
            term_loop(runtime, stop_event)
        else:
            # In non-interactive mode, just keep the server running
            while not stop_event.is_set():
                time.sleep(1)
    finally:
        stop_event.set()
