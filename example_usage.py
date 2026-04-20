#!/usr/bin/env python3
"""
Example: Using UI Agent programmatically (Advanced)

This shows how to use UI Agent as a library rather than just a CLI tool.
"""

import os
from ui_agent.config import Config
from ui_agent.vision import VisionAnalyzer
from ui_agent.automator import UIAutomator
from ui_agent.utils import get_screenshot_bytes_and_dims


def click_on_element(element_description: str, delay: float = 2.0) -> None:
    """Click on a UI element programmatically."""
    # Load configuration
    config = Config()
    
    # Get screenshot
    print("📸 Taking screenshot...")
    screenshot_bytes, screen_width, screen_height = get_screenshot_bytes_and_dims()
    print(f"✓ Captured {screen_width}×{screen_height}")
    
    # Find element using vision API
    print("🔍 Analyzing with Gemini Vision...")
    analyzer = VisionAnalyzer(config.get_api_key())
    ymin, xmin, ymax, xmax = analyzer.locate_element(screenshot_bytes, element_description)
    print(f"✓ Found at: ({ymin}, {xmin}) → ({ymax}, {xmax})")
    
    # Click on it
    print(f"🖱️  Clicking (delay: {delay}s)...")
    automator = UIAutomator()
    automator.click_at_normalized_coords(
        (ymin, xmin, ymax, xmax),
        screen_width,
        screen_height,
        delay=delay,
        description=element_description,
    )
    print("✓ Clicked!")


def type_text(text: str, delay: float = 1.0) -> None:
    """Type text programmatically."""
    print(f"⌨️  Typing text (delay: {delay}s)...")
    automator = UIAutomator()
    automator.type_text(text, delay=delay)
    print("✓ Text entered!")


if __name__ == "__main__":
    # Example: Click and type
    click_on_element("Email input field", delay=2.0)
    type_text("user@example.com", delay=1.0)
    
    click_on_element("Password input field", delay=1.5)
    type_text("MyPassword123", delay=1.0)
    
    click_on_element("Login button", delay=2.0)
