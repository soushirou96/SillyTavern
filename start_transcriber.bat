@echo off
echo Starting Gemini Video Transcriber...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import google.generativeai" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements-transcriber.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Start the application
python video_transcriber.py

if errorlevel 1 (
    echo.
    echo Application exited with an error
    pause
)
