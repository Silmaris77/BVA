@echo off
title ZenDegenAcademy Launcher
color 0A

echo.
echo  ███████╗███████╗███╗   ██╗██████╗ ███████╗ ██████╗ ███████╗███╗   ██╗
echo  ╚══███╔╝██╔════╝████╗  ██║██╔══██╗██╔════╝██╔════╝ ██╔════╝████╗  ██║
echo    ███╔╝ █████╗  ██╔██╗ ██║██║  ██║█████╗  ██║  ███╗█████╗  ██╔██╗ ██║
echo   ███╔╝  ██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██║   ██║██╔══╝  ██║╚██╗██║
echo  ███████╗███████╗██║ ╚████║██████╔╝███████╗╚██████╔╝███████╗██║ ╚████║
echo  ╚══════╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝
echo.
echo                        🎓 ACADEMY - Launcher 🚀
echo.
echo ================================================================================
echo.

echo 📁 Current directory: %CD%
echo 📄 Application file: main.py
echo 🐍 Python/Streamlit ready
echo.

echo ⚡ Starting ZenDegenAcademy...
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
    echo.
) else (
    echo ⚠️  No virtual environment found - using system Python
    echo.
)

REM Check if requirements.txt exists and install dependencies
if exist "requirements.txt" (
    echo 📦 Installing/updating dependencies...
    pip install -r requirements.txt --quiet
    echo ✅ Dependencies ready
    echo.
) else (
    echo ⚠️  No requirements.txt found
    echo.
)

echo 🚀 Launching Streamlit application...
echo 🌐 Application will open in your default browser
echo 🛑 Press Ctrl+C to stop the application
echo.
echo ================================================================================

streamlit run main.py

echo.
echo 📊 Application stopped
echo.
pause
