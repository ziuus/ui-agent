"""FastAPI server for live dashboard and command API."""

from __future__ import annotations

import asyncio
import threading
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .runtime import AgentRuntime


STATIC_DIR = Path(__file__).resolve().parent / "static"


def create_app(runtime: AgentRuntime, stop_event: threading.Event) -> FastAPI:
    app = FastAPI(title="Slovio Agent Dashboard", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.get("/")
    async def index() -> FileResponse:
        return FileResponse(str(STATIC_DIR / "index.html"))

    @app.get("/api/state")
    async def get_state():
        return runtime.snapshot()

    @app.post("/api/command")
    async def post_command(payload: dict):
        text = str(payload.get("command", "")).strip()
        if text:
            runtime.submit_command(text)
            runtime.add_log("info", f"Command queued from dashboard: {text}")
            return {
                "queued": True,
                "output": {
                    "type": "ack",
                    "status": "accepted",
                    "message": "Command queued",
                    "data": {"command": text},
                },
            }
        return {
            "queued": False,
            "output": {
                "type": "ack",
                "status": "error",
                "message": "Missing command",
                "data": {},
            },
        }

    @app.post("/api/shutdown")
    async def shutdown():
        runtime.submit_command("/quit")
        stop_event.set()
        return {"ok": True}

    @app.websocket("/ws")
    async def websocket_state(ws: WebSocket):
        await ws.accept()
        last_version: Optional[int] = None
        try:
            while not stop_event.is_set():
                snapshot = runtime.snapshot()
                if snapshot["version"] != last_version:
                    await ws.send_json(snapshot)
                    last_version = snapshot["version"]
                await asyncio.sleep(0.25)
        except WebSocketDisconnect:
            return
        except Exception as exc:
            runtime.add_log("error", f"WebSocket error: {exc}")

    return app
