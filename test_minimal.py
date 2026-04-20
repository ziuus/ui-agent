import sys
from unittest.mock import MagicMock

# Mock display-dependent modules before they are imported by ui_agent
sys.modules['pyautogui'] = MagicMock()
sys.modules['Xlib'] = MagicMock()
sys.modules['Xlib.display'] = MagicMock()
sys.modules['Xlib.protocol'] = MagicMock()
sys.modules['Xlib.error'] = MagicMock()
sys.modules['mouseinfo'] = MagicMock()

import pytest
from ui_agent.config import Config
from ui_agent.utils import denormalize_coordinates, calculate_center

def test_config_loading():
    import os
    os.environ["GEMINI_API_KEY"] = "test_key_123"
    config = Config()
    assert config.gemini_api_key == "test_key_123"

def test_coordinates():
    # 500, 500 on 1000x1000 normalized scale should be middle of screen
    x, y = denormalize_coordinates(500, 500, 1920, 1080)
    assert x == 960
    assert y == 540

def test_center():
    # Center of (0,0) to (100,100) is (50,50)
    cx, cy = calculate_center((0, 0, 100, 100))
    assert cx == 50
    assert cy == 50

if __name__ == "__main__":
    pytest.main([__file__])
