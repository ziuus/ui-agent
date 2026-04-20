@echo off
REM Quick start script for UI Agent on Windows

echo 🤖 UI Agent - Quick Start Installer
echo ====================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Python not found. Please install Python 3.8+ from python.org
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✓ Python %python_version% found
echo.

REM Check pip
echo Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ pip not found
    exit /b 1
)
echo ✓ pip found
echo.

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment exists
    call venv\Scripts\activate.bat
    echo ✓ Virtual environment activated
)
echo.

REM Install package
echo Installing UI Agent...
pip install -e . >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Installation failed
    exit /b 1
)
echo ✓ Installation complete!
echo.

REM Verify
echo Verifying installation...
ui-agent --version
echo ✓ ui-agent is ready!
echo.

echo Next steps:
echo 1. Get API key from: https://makersuite.google.com/app/apikey
echo 2. Set environment variable:
echo    set GEMINI_API_KEY=your_key_here
echo 3. Try: ui-agent click "button name"
echo.
echo ✓ Setup complete! Happy automating!
