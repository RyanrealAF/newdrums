@echo off
cd /d "%~dp0"
if "%~1"=="" (
    echo ---------------------------------------------------
    echo  R# Visualizer - Drag & Drop Launcher
    echo ---------------------------------------------------
    echo.
    echo  Please drag and drop an audio file (WAV, MP3)
    echo  onto this batch file to start the visualizer.
    echo.
    pause
) else (
    python launcher.py "%~1"
    if errorlevel 1 pause
)