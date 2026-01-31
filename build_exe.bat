@echo off
echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building R# Visualizer EXE...
echo This may take a few minutes...
echo.

REM --collect-all librosa is crucial because librosa uses dynamic loading
pyinstaller --noconfirm --onefile --name "RSharpViz" --collect-all librosa launcher.py

echo.
if exist "dist\RSharpViz.exe" (
    echo Build Successful!
    echo Your standalone EXE is located in the 'dist' folder.
    echo You can drag and drop audio files onto dist\RSharpViz.exe
) else (
    echo Build Failed. Check the error messages above.
)
pause