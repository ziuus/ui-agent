"""Tests for ui-agent CLI tool."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from ui_agent.config import Config
from ui_agent.vision import VisionAnalyzer
from ui_agent.automator import UIAutomator
from ui_agent.utils import (
    denormalize_coordinates,
    denormalize_box,
    calculate_center,
)


class TestConfig:
    """Test configuration management."""

    def test_config_loads_env_vars(self):
        """Test that config loads environment variables."""
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test_key_123"}):
            config = Config()
            assert config.gemini_api_key == "test_key_123"

    def test_validate_api_key_success(self):
        """Test API key validation."""
        with patch.dict("os.environ", {"GEMINI_API_KEY": "valid_key"}):
            config = Config()
            assert config.validate_api_key() is True

    def test_validate_api_key_missing(self):
        """Test API key validation when missing."""
        with patch.dict("os.environ", {"GEMINI_API_KEY": ""}):
            config = Config()
            assert config.validate_api_key() is False


class TestUtils:
    """Test utility functions."""

    def test_denormalize_coordinates(self):
        """Test coordinate denormalization."""
        # Half screen position
        x, y = denormalize_coordinates(500, 500, 1920, 1080)
        assert x == 960
        assert y == 540

    def test_denormalize_box(self):
        """Test bounding box denormalization."""
        box = denormalize_box((0, 0, 500, 500), 1000, 1000)
        assert box == (0, 0, 500, 500)

    def test_calculate_center(self):
        """Test center calculation."""
        center = calculate_center((0, 0, 100, 100))
        assert center == (50, 50)

    def test_calculate_center_offset(self):
        """Test center calculation with offset."""
        center = calculate_center((100, 200, 300, 400))
        assert center == (200, 300)


class TestAutomator:
    """Test UI automation."""

    def test_automator_initialization(self):
        """Test automator initializes with failsafe."""
        automator = UIAutomator(failsafe=True)
        assert automator is not None

    @patch("pyautogui.position")
    def test_get_mouse_position(self, mock_pos):
        """Test getting mouse position."""
        mock_pos.return_value = (100, 200)
        automator = UIAutomator()
        pos = automator.get_mouse_position()
        assert pos == (100, 200)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
