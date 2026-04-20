"""Utility functions for UI Agent."""

import base64
import subprocess
from pathlib import Path
from typing import Tuple
import mss


def get_screenshot_as_bytes() -> tuple:
    """Capture full screen and return as bytes."""
    result = subprocess.run(["grim", "-"], capture_output=True, check=True)
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(result.stdout)).convert("RGB")
    return img.tobytes(), (img.width, img.height, img.width * 3)


def get_screenshot_bytes_and_dims() -> Tuple[bytes, int, int]:
    """Capture full screen and return bytes with dimensions."""
    result = subprocess.run(["grim", "-"], capture_output=True, check=True)
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(result.stdout))
    return result.stdout, img.width, img.height


def get_screen_dimensions() -> Tuple[int, int]:
    """Get current screen dimensions."""
    result = subprocess.run(["grim", "-"], capture_output=True, check=True)
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(result.stdout))
    return img.width, img.height


def denormalize_coordinates(
    x_norm: float, y_norm: float, screen_width: int, screen_height: int
) -> Tuple[int, int]:
    """Convert normalized coordinates (0-1000) to actual screen pixels.
    
    Args:
        x_norm: Normalized X coordinate (0-1000)
        y_norm: Normalized Y coordinate (0-1000)
        screen_width: Screen width in pixels
        screen_height: Screen height in pixels
        
    Returns:
        Tuple of (pixel_x, pixel_y)
    """
    pixel_x = int((x_norm / 1000.0) * screen_width)
    pixel_y = int((y_norm / 1000.0) * screen_height)
    return pixel_x, pixel_y


def denormalize_box(
    box: Tuple[int, int, int, int], screen_width: int, screen_height: int
) -> Tuple[int, int, int, int]:
    """Convert normalized bounding box to pixel coordinates.
    
    Args:
        box: Tuple of (ymin, xmin, ymax, xmax) normalized 0-1000
        screen_width: Screen width in pixels
        screen_height: Screen height in pixels
        
    Returns:
        Tuple of (xmin_px, ymin_px, xmax_px, ymax_px)
    """
    ymin, xmin, ymax, xmax = box
    xmin_px, ymin_px = denormalize_coordinates(xmin, ymin, screen_width, screen_height)
    xmax_px, ymax_px = denormalize_coordinates(xmax, ymax, screen_width, screen_height)
    return xmin_px, ymin_px, xmax_px, ymax_px


def calculate_center(box: Tuple[int, int, int, int]) -> Tuple[int, int]:
    """Calculate center point of a bounding box.
    
    Args:
        box: Tuple of (xmin, ymin, xmax, ymax)
        
    Returns:
        Tuple of (center_x, center_y)
    """
    xmin, ymin, xmax, ymax = box
    center_x = (xmin + xmax) // 2
    center_y = (ymin + ymax) // 2
    return center_x, center_y


def toggle_screen_privacy(blank: bool) -> Tuple[bool, str]:
    """Attempt to blank or restore screen on Linux/X11 using xset.

    Returns:
        Tuple of (success, message)
    """
    command = ["xset", "dpms", "force", "off" if blank else "on"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return True, "screen blanked" if blank else "screen restored"
        stderr = (result.stderr or "").strip()
        return False, stderr or "xset command failed"
    except FileNotFoundError:
        return False, "xset not installed"
    except Exception as exc:
        return False, str(exc)
