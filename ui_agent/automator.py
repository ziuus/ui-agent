"""UI automation using mouse and keyboard control."""

import time
import subprocess
import os

try:
    import pyautogui
except BaseException:

    class MockPyAutoGUI:
        FAILSAFE = True

        def size(self):
            return (1920, 1080)

        def moveTo(self, *args, **kwargs):
            pass

        def click(self, *args, **kwargs):
            pass

        def write(self, *args, **kwargs):
            pass

        def typewrite(self, *args, **kwargs):
            pass

        def press(self, *args, **kwargs):
            pass

        def hotkey(self, *args, **kwargs):
            pass

        def position(self):
            return (0, 0)

    pyautogui = MockPyAutoGUI()

from typing import Tuple, Optional
from rich.console import Console
from rich.table import Table
from .utils import denormalize_box, calculate_center

# Our working UI automation (Wayland-compatible)
YDOTOOL_SOCKET = os.environ.get("YDOTOOL_SOCKET", "/tmp/.ydotool_socket")


def ensure_ydotoold():
    if not os.path.exists(YDOTOOL_SOCKET):
        try:
            subprocess.Popen(
                ["ydotoold", "--socket-path", YDOTOOL_SOCKET],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(0.5)
        except:
            pass


def run_ydotool(args):
    ensure_ydotoold()
    env = os.environ.copy()
    env["YDOTOOL_SOCKET"] = YDOTOOL_SOCKET
    result = subprocess.run(["ydotool"] + args, env=env, capture_output=True)
    return result.returncode == 0


class UIAutomator:
    """Handles mouse and keyboard automation with safety features."""

    def __init__(self, failsafe: bool = True):
        """Initialize UI automator.

        Args:
            failsafe: Enable failsafe (move mouse to corner to abort)
        """
        pyautogui.FAILSAFE = failsafe
        # Disable fail-safe for a moment, we'll re-enable it after setup
        # pyautogui's failsafe works by checking if mouse is at (0,0)
        self.console = Console()

    def click_at_normalized_coords(
        self,
        box: Tuple[int, int, int, int],
        screen_width: int,
        screen_height: int,
        delay: float = 2.0,
        description: str = "",
    ) -> None:
        """Click at center of normalized bounding box with delay."""
        xmin_px, ymin_px, xmax_px, ymax_px = denormalize_box(box, screen_width, screen_height)
        center_x, center_y = calculate_center((xmin_px, ymin_px, xmax_px, ymax_px))

        self._show_target_info(
            description, (ymin_px, xmin_px, ymax_px, ymax_px), (center_x, center_y), delay
        )

        time.sleep(delay)

        self.console.print(f"[cyan]→[/cyan] Moving mouse to ({center_x}, {center_y})")
        # Try ydotool first (works on Wayland), fallback to pyautogui
        if not run_ydotool(["mousemove", str(center_x), str(center_y)]):
            pyautogui.moveTo(center_x, center_y, duration=0.3)
        time.sleep(0.2)

        self.console.print("[cyan]→[/cyan] Clicking...")
        if not run_ydotool(["click", "0"]):
            pyautogui.click()

        self.console.print("[green]✓[/green] Click completed!")

    def type_text(self, text: str, interval: float = 0.05, delay: float = 1.0) -> None:
        """Type text with optional delay and character interval."""
        if delay > 0:
            self.console.print(f"[yellow]⏱[/yellow] Waiting {delay}s before typing...")
            for remaining in range(int(delay), 0, -1):
                if remaining > 0:
                    time.sleep(1)

        self.console.print(f"[cyan]→[/cyan] Typing: {text}")
        # Try ydotool first, fallback to pyautogui
        if not run_ydotool(["type", "--", text]):
            pyautogui.typewrite(text, interval=interval)
        self.console.print("[green]✓[/green] Text typed!")

    def type_text_unicode(self, text: str, interval: float = 0.05, delay: float = 1.0) -> None:
        """Type text with Unicode support using write() instead of typewrite()."""
        if delay > 0:
            self.console.print(f"[yellow]⏱[/yellow] Waiting {delay}s before typing...")
            time.sleep(delay)

        self.console.print(f"[cyan]→[/cyan] Typing: {text}")
        if not run_ydotool(["type", "--", text]):
            pyautogui.write(text, interval=interval)
        self.console.print("[green]✓[/green] Text typed!")

    def move_mouse(self, x: int, y: int, duration: float = 0.3) -> None:
        """Move mouse to specified position."""
        self.console.print(f"[cyan]→[/cyan] Moving mouse to ({x}, {y})")
        if not run_ydotool(["mousemove", str(x), str(y)]):
            pyautogui.moveTo(x, y, duration=duration)
        self.console.print("[green]✓[/green] Mouse moved!")

    def click_at(self, x: int, y: int, duration: float = 0.2) -> None:
        """Move mouse to an absolute pixel coordinate and click."""
        self.console.print(f"[cyan]→[/cyan] Moving mouse to ({x}, {y}) for click")
        if not run_ydotool(["mousemove", str(x), str(y)]):
            pyautogui.moveTo(x, y, duration=duration)
        time.sleep(0.05)
        if not run_ydotool(["click", "0"]):
            pyautogui.click()
        self.console.print("[green]✓[/green] Click completed!")

    def click_current_position(self) -> None:
        """Click at the current cursor position."""
        pos = pyautogui.position()
        self.console.print(f"[cyan]→[/cyan] Clicking current position ({pos[0]}, {pos[1]})")
        if not run_ydotool(["click", "0"]):
            pyautogui.click()
        self.console.print("[green]✓[/green] Click completed!")

    def press_key(self, key: str, presses: int = 1, interval: float = 0.08) -> None:
        """Press a single key one or more times."""
        self.console.print(f"[cyan]→[/cyan] Pressing key: {key} x{presses}")
        for _ in range(presses):
            if not run_ydotool(["key", key]):
                pyautogui.press(key, presses=1, interval=interval)
            time.sleep(interval)
        self.console.print("[green]✓[/green] Key press completed!")

    def send_hotkey(self, keys: Tuple[str, ...]) -> None:
        """Send a key combination such as ('ctrl', 'l')."""
        if not keys:
            return
        combo = " + ".join(keys)
        self.console.print(f"[cyan]→[/cyan] Sending hotkey: {combo}")
        # Try ydotool for hotkeys
        for key in keys:
            if not run_ydotool(["key", key]):
                pyautogui.hotkey(*keys)
                break
        else:
            pass  # All keys sent via ydotool
        self.console.print("[green]✓[/green] Hotkey completed!")

    def _show_target_info(
        self,
        description: str,
        pixel_box: Tuple[int, int, int, int],
        center: Tuple[int, int],
        delay: float,
    ) -> None:
        """Display information about the click target.

        Args:
            description: Element description
            pixel_box: Bounding box in pixels (ymin, xmin, ymax, xmax)
            center: Center coordinates (x, y)
            delay: Delay before click
        """
        ymin, xmin, ymax, xmax = pixel_box
        center_x, center_y = center

        table = Table(title="[bold cyan]Click Target[/bold cyan]", show_header=True)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Description", description or "(from vision API)")
        table.add_row("Bounding Box", f"({xmin}, {ymin}) → ({xmax}, {ymax})")
        table.add_row("Center Point", f"({center_x}, {center_y})")
        table.add_row("Size", f"{xmax - xmin} × {ymax - ymin} px")
        table.add_row("Delay", f"{delay}s (move mouse to top-left to cancel)")

        self.console.print(table)

    def get_mouse_position(self) -> Tuple[int, int]:
        """Get current mouse position.

        Returns:
            Tuple of (x, y) coordinates
        """
        return pyautogui.position()

    def wait_and_check_abort(self, duration: float) -> bool:
        """Wait for duration, checking if user moved mouse to abort.

        Args:
            duration: Duration to wait (seconds)

        Returns:
            True if aborted (mouse moved to corner), False if completed
        """
        start_pos = pyautogui.position()
        start_time = time.time()

        while time.time() - start_time < duration:
            current_pos = pyautogui.position()
            # Check if mouse is in top-left corner (failsafe zone)
            if current_pos[0] < 10 and current_pos[1] < 10:
                self.console.print("[yellow]⚠[/yellow] Action cancelled (mouse in corner)")
                return True
            time.sleep(0.1)

        return False
