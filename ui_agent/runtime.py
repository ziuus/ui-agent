"""Shared runtime state for TUI, web dashboard, and autonomous loop."""

from __future__ import annotations

import base64
import threading
import time
from dataclasses import dataclass, field
from queue import Queue
from typing import Any, Dict, List, Optional


@dataclass
class RuntimeState:
    """Thread-safe mutable state exposed to both TUI and web clients."""

    status: str = "idle"
    current_goal: str = ""
    latest_screenshot_b64: str = ""
    logs: List[Dict[str, Any]] = field(default_factory=list)
    chat: List[Dict[str, Any]] = field(default_factory=list)
    step_count: int = 0
    version: int = 0


class AgentRuntime:
    """Coordinator for state, command queue, and pub/sub snapshots."""

    def __init__(self) -> None:
        self._state = RuntimeState()
        self._lock = threading.Lock()
        self.command_queue: Queue[str] = Queue()

    def submit_command(self, text: str) -> None:
        self.command_queue.put(text.strip())

    def set_status(self, status: str, goal: Optional[str] = None) -> None:
        with self._lock:
            self._state.status = status
            if goal is not None:
                self._state.current_goal = goal
            self._state.version += 1

    def set_screenshot(self, screenshot_bytes: bytes) -> None:
        encoded = base64.b64encode(screenshot_bytes).decode("ascii")
        with self._lock:
            self._state.latest_screenshot_b64 = encoded
            self._state.version += 1

    def add_log(self, level: str, message: str, action: Optional[Dict[str, Any]] = None) -> None:
        with self._lock:
            self._state.logs.append(
                {
                    "ts": time.time(),
                    "level": level,
                    "message": message,
                    "action": action or {},
                }
            )
            self._state.logs = self._state.logs[-200:]
            self._state.version += 1

    def add_chat(
        self,
        role: str,
        content: str,
        *,
        kind: str = "text",
        structured: Optional[Dict[str, Any]] = None,
    ) -> None:
        with self._lock:
            self._state.chat.append(
                {
                    "ts": time.time(),
                    "role": role,
                    "content": content,
                    "kind": kind,
                    "structured": structured or {},
                }
            )
            self._state.chat = self._state.chat[-100:]
            self._state.version += 1

    def increment_step(self) -> None:
        with self._lock:
            self._state.step_count += 1
            self._state.version += 1

    def reset_steps(self) -> None:
        with self._lock:
            self._state.step_count = 0
            self._state.version += 1

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "status": self._state.status,
                "current_goal": self._state.current_goal,
                "latest_screenshot_b64": self._state.latest_screenshot_b64,
                "logs": list(self._state.logs),
                "chat": list(self._state.chat),
                "step_count": self._state.step_count,
                "version": self._state.version,
            }
