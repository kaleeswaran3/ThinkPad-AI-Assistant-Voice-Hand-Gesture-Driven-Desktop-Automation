@echo off
REM ThinkPad Voice Assistant Launcher
REM Double-click this file to start the assistant

echo Starting ThinkPad Voice Assistant...

REM Check if virtual environment exists
if exist ".venv\Scripts\python.exe" (
    echo Using virtual environment...
    ".venv\Scripts\python.exe" gui_assistant.py
) else (
    echo Virtual environment not found, using system Python...
    py gui_assistant.py
)

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to exit...
    pause > nul
)
