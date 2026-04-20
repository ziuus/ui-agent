#!/usr/bin/env python
"""Setup script for ui-agent package."""

from setuptools import setup, find_packages

setup(
    name="ui-agent",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ui-agent=ui_agent.cli:app",
            "slovio-agent=ui_agent.launcher:main",
        ],
    },
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "google-generativeai>=0.3.0",
        "fastapi>=0.115.0",
        "uvicorn>=0.30.0",
        "pyautogui>=0.9.53",
        "mss>=9.0.1",
        "python-dotenv>=1.0.0",
        "Pillow>=10.0.0",
    ],
)
