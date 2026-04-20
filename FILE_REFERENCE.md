# 📚 UI Agent - Complete File Reference

## Project Structure & File Descriptions

### Package Files (`ui_agent/`)

#### `ui_agent/__init__.py`
- Package initialization
- Exports main classes: `Config`, `VisionAnalyzer`, `UIAutomator`
- Version and metadata

#### `ui_agent/__main__.py`
- Entry point for running as module: `python -m ui_agent`
- Imports and calls CLI app

#### `ui_agent/cli.py` ⭐ **MAIN CLI**
- Typer command-line interface
- **Commands:**
  - `click` - Find and click UI elements
  - `type` - Enter text
  - `screenshot` - Capture screen
  - `config` - Manage settings
- ~350 lines of polished CLI code
- Rich formatting for output
- Complete error handling

#### `ui_agent/vision.py` ⭐ **VISION API**
- `VisionAnalyzer` class
- Gemini 1.5 Flash integration
- Methods:
  - `locate_element()` - Find UI element and return coordinates
  - `verify_element()` - Check if element exists
- JSON response parsing
- Error handling for API failures
- ~150 lines

#### `ui_agent/automator.py` ⭐ **AUTOMATION**
- `UIAutomator` class
- pyautogui mouse/keyboard control
- Methods:
  - `click_at_normalized_coords()` - Click at location
  - `type_text()` - Type ASCII characters
  - `type_text_unicode()` - Type with Unicode
  - `move_mouse()` - Move cursor
  - `wait_and_check_abort()` - Safety abort check
  - `get_mouse_position()` - Get current cursor position
- Rich table display for target info
- ~220 lines

#### `ui_agent/config.py` ⭐ **CONFIGURATION**
- `Config` class
- Loads from .env files and environment variables
- Methods:
  - `validate_api_key()` - Check if API key is set
  - `get_api_key()` - Get API key or raise error
  - `_find_env_file()` - Search for .env in directories
- Searches up to 5 directory levels for .env
- ~60 lines

#### `ui_agent/utils.py` ⭐ **UTILITIES**
- Coordinate conversion functions:
  - `get_screenshot_bytes_and_dims()` - Capture screen and return bytes + dimensions
  - `get_screen_dimensions()` - Get screen size
  - `denormalize_coordinates()` - Convert 0-1000 scale to pixels
  - `denormalize_box()` - Convert normalized box to pixels
  - `calculate_center()` - Find center of bounding box
- Image processing
- ~100 lines

### Configuration Files

#### `pyproject.toml` ⭐ **MODERN PACKAGING**
- PEP 517/518 compliant
- Project metadata (name, version, description)
- Dependencies specification
- Build system requirements
- Entry points (declares `ui-agent` command)
- Tool configuration (black, ruff)
- ~70 lines

#### `setup.py` ⭐ **LEGACY PACKAGING**
- setuptools configuration
- Alternative to pyproject.toml
- For backward compatibility
- Entry points configuration
- ~30 lines

#### `requirements.txt`
- Simple pip requirements format
- All dependencies with version constraints
- Can be installed with: `pip install -r requirements.txt`
- 7 lines

#### `.env.example`
- Template for configuration
- Shows available environment variables:
  - `GEMINI_API_KEY`
  - `DEFAULT_DELAY`
  - `LOG_LEVEL`
- Copy to `.env` and fill in values

#### `.gitignore`
- Ignores Python artifacts (`__pycache__`, `.pyc`)
- Ignores virtual environments (`venv/`, `.env`)
- Ignores IDE files (`.vscode`, `.idea`)
- Ignores OS files (`.DS_Store`, `Thumbs.db`)

### Documentation Files

#### `README.md` ⭐ **COMPREHENSIVE GUIDE**
- Full project documentation (~500 lines)
- Features list
- Installation instructions (3 methods)
- Setup guide (4 options for API key)
- Usage examples for all commands
- Advanced options and tips
- Troubleshooting guide
- Performance metrics
- Cost analysis
- Security considerations

#### `QUICKSTART.md` ⭐ **QUICK START**
- Fast setup guide (~300 lines)
- 5-minute installation
- First command walkthrough
- All core commands with examples
- Safety features explanation
- Configuration options
- Practical workflow examples
- Troubleshooting quick reference

#### `PROJECT_SUMMARY.md` ⭐ **PROJECT OVERVIEW**
- Complete project summary (~400 lines)
- File structure overview
- Architecture explanation
- Installation quick reference
- Core commands summary
- Performance metrics
- What's implemented checklist
- Getting started steps

#### `INSTALL_VERIFY.md` ⭐ **VERIFICATION**
- Installation checklist (~300 lines)
- Step-by-step verification
- Platform-specific checks
- Functional tests
- Troubleshooting verification
- Complete verification script
- Performance baseline tests

#### `EXAMPLES.md`
- Usage examples for all commands
- CLI examples (copy-paste ready)
- Practical workflows (login, forms, search)
- Tips for effective use

#### `LICENSE`
- MIT License text
- Full legal permission details

### Installation & Helper Scripts

#### `install.sh`
- Linux/macOS installer script
- Creates virtual environment
- Installs package
- Verifies installation
- Shows next steps

#### `install.bat`
- Windows installer script
- Batch file version of install.sh
- Creates venv and installs
- Displays setup instructions

### Development & Testing

#### `tests.py`
- Basic test suite
- Tests for:
  - Config loading
  - API key validation
  - Coordinate conversion
  - Automator initialization
- Uses pytest
- ~120 lines

#### `example_usage.py`
- Programmatic usage examples
- Shows how to use UI Agent as a library
- Functions:
  - `click_on_element()`
  - `type_text()`
- ~60 lines
- Can be run directly: `python example_usage.py`

### Index Files (This Project)

#### `FILE_REFERENCE.md` (this file)
- Complete file descriptions
- File purposes and locations
- What each file does
- Key functions and classes

#### `QUICKSTART.md`
- Contains this summary

---

## Quick File Lookup

### Need to... → See this file

| Task | File |
|------|------|
| Add new command | `ui_agent/cli.py` |
| Modify Gemini integration | `ui_agent/vision.py` |
| Change mouse/keyboard behavior | `ui_agent/automator.py` |
| Add config options | `ui_agent/config.py` |
| Add utility functions | `ui_agent/utils.py` |
| Change dependencies | `requirements.txt` or `pyproject.toml` |
| Fix import issues | `ui_agent/__init__.py` |
| Add tests | `tests.py` |
| Update documentation | `README.md` |
| Quick reference | `QUICKSTART.md` |
| Verify installation | `INSTALL_VERIFY.md` |
| Show examples | `EXAMPLES.md` |
| Use as library | `example_usage.py` |

## File Sizes

```
ui_agent/
├── cli.py              ~350 lines
├── vision.py           ~150 lines
├── automator.py        ~220 lines
├── config.py           ~60 lines
├── utils.py            ~100 lines
├── __init__.py         ~10 lines
└── __main__.py         ~10 lines

Documentation
├── README.md           ~500 lines
├── QUICKSTART.md       ~300 lines
├── PROJECT_SUMMARY.md  ~400 lines
├── INSTALL_VERIFY.md   ~300 lines
├── EXAMPLES.md         ~100 lines
└── FILE_REFERENCE.md   ~250 lines
```

**Total:** ~2,500 lines of code + documentation

## Dependencies Graph

```
ui_agent/
├── cli.py
│   ├── typer (CLI framework)
│   ├── rich (output formatting)
│   ├── config.py
│   ├── vision.py
│   ├── automator.py
│   └── utils.py
│
├── vision.py
│   ├── google.generativeai (Gemini API)
│   ├── rich (spinner/output)
│   ├── Pillow (image processing)
│   └── json (built-in)
│
├── automator.py
│   ├── pyautogui (mouse/keyboard)
│   ├── rich (output)
│   └── utils.py
│
├── config.py
│   ├── python-dotenv (.env loading)
│   ├── os (env vars)
│   └── pathlib (file paths)
│
└── utils.py
    ├── mss (screenshot)
    ├── Pillow (image)
    ├── io (bytes)
    └── typing (hints)
```

## Key Classes & Methods

### VisionAnalyzer (vision.py)
```python
VisionAnalyzer(api_key: str)
  .locate_element(screenshot_bytes, description) → (ymin, xmin, ymax, xmax)
  .verify_element(screenshot_bytes, description) → bool
```

### UIAutomator (automator.py)
```python
UIAutomator(failsafe: bool = True)
  .click_at_normalized_coords(box, width, height, delay, description)
  .type_text(text, interval, delay)
  .type_text_unicode(text, interval, delay)
  .move_mouse(x, y, duration)
  .get_mouse_position() → (x, y)
  .wait_and_check_abort(duration) → bool
```

### Config (config.py)
```python
Config()
  .validate_api_key() → bool
  .get_api_key() → str
  ._find_env_file() → Optional[Path]
```

## CLI Commands & Options

### click
```
ui-agent click <description> [OPTIONS]
  --delay -d FLOAT
  --no-failsafe
  --verbose -v
```

### type
```
ui-agent type <text> [OPTIONS]
  --delay -d FLOAT
  --interval -i FLOAT
  --verbose -v
```

### screenshot
```
ui-agent screenshot [OPTIONS]
  --output -o TEXT
```

### config
```
ui-agent config [OPTIONS]
  --show
  --api-key TEXT
```

---

**For more details, see QUICKSTART.md or README.md**
