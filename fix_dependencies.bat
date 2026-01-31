@echo off
echo Cleaning up old pygame installations...
pip uninstall -y pygame pygame-ce

echo.
echo Installing updated dependencies (using pygame-ce)...
pip install -r requirements.txt

echo.
echo Done! Try running play.bat or build_exe.bat now.
pause