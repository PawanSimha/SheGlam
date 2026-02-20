@echo off
title SheGlam - Instant Makeup Services

echo.
echo =======================================================
echo          SheGlam - One-Click Project Runner
echo =======================================================
echo.

:: Check for Python Installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.10+ from https://python.org/
    pause
    exit /b
)

:: Virtual Environment Setup
if not exist "venv" (
    echo [INFO] First time setup: Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    
    echo [INFO] Installing required libraries...
    pip install -r requirements.txt >nul
    
    echo [INFO] Setting up environment variables...
    if exist ".env.example" copy .env.example .env >nul
) else (
    :: Activate existing environment
    call venv\Scripts\activate
)

:: Create Required Directories (if missing)
if not exist "frontend\static\uploads\certificates" (
    mkdir "frontend\static\uploads\certificates" >nul
)
if not exist "frontend\static\uploads\govt_ids" (
    mkdir "frontend\static\uploads\govt_ids" >nul
)

:: Start Browser in Background
echo [INFO] Launching browser...
start "" "http://localhost:5000"

:: Start Application
echo.
echo [SUCCESS] Starting SheGlam server...
echo.
echo Application running at: http://localhost:5000
echo Press Ctrl+C to stop the server.
echo.

python backend/app.py

pause
