"""UI Agent - A polished CLI tool for UI automation using Google Gemini Vision API."""

__version__ = "0.1.0"
__author__ = "Your Name"
__license__ = "MIT"

from .config import Config
from .vision import VisionAnalyzer
from .automator import UIAutomator

__all__ = ["Config", "VisionAnalyzer", "UIAutomator"]
