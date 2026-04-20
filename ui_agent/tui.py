"""Rich-powered terminal loop for persistent interaction."""

from __future__ import annotations

import threading
import time
from typing import Optional

from rich.console import Console
from rich.panel import Panel

from .runtime import AgentRuntime


def term_loop(runtime: AgentRuntime, stop_event: threading.Event, poll_interval: float = 0.2) -> None:
    """Persistent command prompt that feeds the autonomous agent."""
    console = Console()
    console.print(
        Panel(
            "Persistent autonomous mode is active.\n"
            "Type commands like: Open the browser and click login\n"
            "Vision chat: What do you see on my screen?\n"
            "Privacy mode: /privacy on or /privacy off\n"
            "Exit with /quit",
            title="Slovio Agent",
            border_style="cyan",
        )
    )

    last_log_index = 0
    last_chat_index = 0

    while not stop_event.is_set():
        _flush_new_logs(
            console,
            runtime,
            log_start_index=last_log_index,
            chat_start_index=last_chat_index,
        )
        snapshot = runtime.snapshot()
        last_log_index = len(snapshot["logs"])
        last_chat_index = len(snapshot["chat"])

        try:
            user_input = console.input("[bold cyan]Slovio Agent > [/bold cyan]").strip()
        except (KeyboardInterrupt, EOFError):
            stop_event.set()
            break

        if not user_input:
            time.sleep(poll_interval)
            continue

        runtime.submit_command(user_input)

        if user_input.lower() in {"/quit", "quit", "exit", "/exit"}:
            stop_event.set()
            break


def _flush_new_logs(
    console: Console,
    runtime: AgentRuntime,
    log_start_index: int,
    chat_start_index: int,
) -> None:
    snapshot = runtime.snapshot()
    logs = snapshot["logs"][log_start_index:]
    for item in logs:
        level = item.get("level", "info")
        message = item.get("message", "")
        color = {
            "error": "red",
            "warning": "yellow",
            "success": "green",
        }.get(level, "white")
        console.print(f"[{color}]{level.upper()}[/{color}] {message}")

    chats = snapshot["chat"][chat_start_index:]
    for entry in chats:
        if entry.get("role") == "assistant":
            console.print(Panel(str(entry.get("content", "")), title="Assistant", border_style="green"))
