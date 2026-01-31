@echo off
cd /d "%~dp0"
echo Starting R# Web Visualizer...
echo.

REM Try using npm/http-server first (better, supports ranges/mime types well)
call npm start
if %errorlevel% equ 0 goto end

REM Fallback to Python if Node.js is not installed
echo Node.js not found. Falling back to Python HTTP server...
start http://localhost:8000
python -m http.server 8000

:end
pause