"""Command-line interface for UI Agent."""

import sys
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich import print as rprint

from . import __version__
from .config import Config
from .vision import VisionAnalyzer
from .automator import UIAutomator
from .utils import get_screenshot_bytes_and_dims, get_screen_dimensions
from .server import log_event, action_event, screenshot_event

def check_display():
    import os
    if not os.environ.get("DISPLAY"):
        rprint("[red]Error: No DISPLAY found. UI automation requires an X11 display.[/red]")
        sys.exit(1)

app = typer.Typer(
    name="ui-agent",
    help="🤖 UI Automation CLI - Control your screen with natural language descriptions",
    no_args_is_help=True,
)
console = Console()


@app.command()
def click(
    description: str = typer.Argument(..., help="Description of the UI element to click"),
    delay: float = typer.Option(
        2.0,
        "--delay",
        "-d",
        help="Delay before clicking (seconds, default: 2.0)",
        min=0.5,
        max=10.0,
    ),
    no_failsafe: bool = typer.Option(
        False,
        "--no-failsafe",
        help="Disable failsafe (don't abort if mouse goes to corner)",
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
) -> None:
    """
    Take a screenshot, find a UI element, and click it.
    
    Example:
        ui-agent click "Login button"
        ui-agent click "Search input field" --delay 1.5
    """
    check_display()
    log_event(f"Starting click action for: {description}")
    action_event({"action": "click", "description": description, "delay": delay})
    try:
        # Load configuration
        config = Config()
        
        if not config.validate_api_key():
            console.print(
                Panel.fit(
                    "[red]Error: GEMINI_API_KEY not configured[/red]\n\n"
                    "1. Get a free API key from:\n"
                    "   [bold]https://makersuite.google.com/app/apikey[/bold]\n\n"
                    "2. Set environment variable:\n"
                    "   [bold]export GEMINI_API_KEY='your_key_here'[/bold]\n\n"
                    "3. Or create .env file:\n"
                    "   [bold]GEMINI_API_KEY=your_key_here[/bold]",
                    title="🔑 Setup Required",
                    border_style="red",
                )
            )
            raise typer.Exit(1)
        
        # Show header
        console.print(
            Panel(
                f"[cyan]Vision-Powered Click[/cyan]\n"
                f"Element: [yellow]{description}[/yellow]\n"
                f"Delay: [green]{delay}s[/green]",
                title="🎯 [bold]UI Agent[/bold]",
                border_style="cyan",
            )
        )
        
        # Take screenshot
        console.print("[cyan]→[/cyan] Capturing screenshot...")
        screenshot_bytes, screen_width, screen_height = get_screenshot_bytes_and_dims()
        
        # Send to Web UI
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(screenshot_bytes))
        screenshot_event(img)
        
        console.print(
            f"[green]✓[/green] Captured ({screen_width}×{screen_height})"
        )
        
        # Analyze screenshot
        console.print("[cyan]→[/cyan] Sending to Gemini Vision API...")
        analyzer = VisionAnalyzer(config.get_api_key())
        ymin, xmin, ymax, xmax = analyzer.locate_element(screenshot_bytes, description)
        console.print(
            f"[green]✓[/green] Element found: "
            f"[yellow]({ymin}, {xmin}) → ({ymax}, {xmax})[/yellow]"
        )
        
        if verbose:
            console.print(f"[dim]Normalized coordinates (0-1000 scale)[/dim]")
        
        # Perform click
        automator = UIAutomator(failsafe=not no_failsafe)
        automator.click_at_normalized_coords(
            (ymin, xmin, ymax, xmax),
            screen_width,
            screen_height,
            delay=delay,
            description=description,
        )
        
        console.print("[green]✓[/green] [bold]Action completed successfully![/bold]")
        log_event(f"Click on '{description}' successful.")
        
    except ValueError as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠[/yellow] Cancelled by user")
        raise typer.Exit(130)
    except Exception as e:
        console.print(f"[red]✗[/red] Unexpected error: {e}")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


@app.command()
def type(
    text: str = typer.Argument(..., help="Text to type"),
    delay: float = typer.Option(
        1.0,
        "--delay",
        "-d",
        help="Delay before typing (seconds, default: 1.0)",
        min=0.0,
        max=10.0,
    ),
    interval: float = typer.Option(
        0.05,
        "--interval",
        "-i",
        help="Delay between characters (seconds, default: 0.05)",
        min=0.0,
        max=1.0,
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
) -> None:
    """
    Type text directly (after taking focus on a field).
    
    Example:
        ui-agent type "Hello, World!"
        ui-agent type "password123" --delay 0.5 --interval 0.1
    """
    try:
        console.print(
            Panel(
                f"[cyan]Keyboard Input[/cyan]\n"
                f"Text: [yellow]{text}[/yellow]\n"
                f"Delay: [green]{delay}s[/green]",
                title="⌨️  [bold]UI Agent[/bold]",
                border_style="cyan",
            )
        )
        
        automator = UIAutomator()
        
        # Try using write() for Unicode support first, fallback to typewrite()
        try:
            automator.type_text_unicode(text, interval=interval, delay=delay)
        except Exception:
            if verbose:
                console.print("[yellow]⚠[/yellow] Unicode typing failed, using ASCII mode")
            automator.type_text(text, interval=interval, delay=delay)
        
        console.print("[green]✓[/green] [bold]Text input completed![/bold]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠[/yellow] Cancelled by user")
        raise typer.Exit(130)
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


@app.command()
def screenshot(
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Save screenshot to file (PNG)",
    ),
) -> None:
    """
    Capture and display current screen information.
    
    Example:
        ui-agent screenshot
        ui-agent screenshot --output screen.png
    """
    try:
        console.print("[cyan]→[/cyan] Capturing screenshot...")
        screenshot_bytes, width, height = get_screenshot_bytes_and_dims()
        
        info_text = f"[cyan]Screenshot Captured[/cyan]\n" \
                   f"Resolution: [yellow]{width}×{height}[/yellow]\n" \
                   f"Size: [green]{len(screenshot_bytes) / 1024:.1f} KB[/green]"
        
        if output:
            with open(output, "wb") as f:
                f.write(screenshot_bytes)
            info_text += f"\nSaved to: [bold]{output}[/bold]"
        
        console.print(Panel(info_text, title="📸 [bold]Screenshot[/bold]", border_style="cyan"))
        
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise typer.Exit(1)


@app.command()
def config(
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
    set_api_key: Optional[str] = typer.Option(None, "--api-key", help="Set Gemini API key"),
) -> None:
    """
    Manage configuration settings.
    
    Example:
        ui-agent config --show
        ui-agent config --api-key "your_key_here"
    """
    try:
        cfg = Config()
        
        if set_api_key:
            # Save to .env file
            import os
            from pathlib import Path
            env_file = Path.home() / ".env"
            
            if env_file.exists():
                with open(env_file, "r") as f:
                    content = f.read()
                # Update or add key
                if "GEMINI_API_KEY=" in content:
                    content = content.replace(
                        [line for line in content.split("\n") if line.startswith("GEMINI_API_KEY")][0],
                        f"GEMINI_API_KEY={set_api_key}"
                    )
                else:
                    content += f"\nGEMINI_API_KEY={set_api_key}"
            else:
                content = f"GEMINI_API_KEY={set_api_key}"
            
            with open(env_file, "w") as f:
                f.write(content)
            
            console.print(f"[green]✓[/green] API key saved to {env_file}")
            return
        
        if show:
            from rich.table import Table
            table = Table(title="Current Configuration", show_header=True)
            table.add_column("Setting", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("API Key", 
                         cfg.gemini_api_key[:20] + "..." if cfg.gemini_api_key else "[red](not set)[/red]")
            table.add_row("Default Delay", f"{cfg.default_delay}s")
            table.add_row("Log Level", cfg.log_level)
            
            console.print(table)
            return
        
        # Default: show setup instructions
        console.print(
            Panel(
                "[cyan]Configuration Guide[/cyan]\n\n"
                "1. Get free API key:\n"
                "   [bold]https://makersuite.google.com/app/apikey[/bold]\n\n"
                "2. Set via command:\n"
                "   [bold]ui-agent config --api-key 'your_key'[/bold]\n\n"
                "3. Or export environment:\n"
                "   [bold]export GEMINI_API_KEY='your_key'[/bold]\n\n"
                "4. Or create ~/.env file:\n"
                "   [bold]GEMINI_API_KEY=your_key[/bold]",
                title="⚙️  Setup",
                border_style="cyan",
            )
        )
        
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise typer.Exit(1)


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        is_flag=True,
        help="Show version and exit",
    ),
) -> None:
    """
    🤖 UI Agent - Vision-powered UI automation CLI
    
    Control your screen with natural language descriptions.
    Built with Gemini 1.5 Flash and human-in-the-loop safety.
    """
    if version:
        console.print(f"[cyan]ui-agent[/cyan] v{__version__}")
        raise typer.Exit()


# Make type command accessible (rename from `type`)
app.command(name="type")(type)

if __name__ == "__main__":
    app()
