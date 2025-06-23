@echo off
title Sistem Manajemen Minat Olahraga Mahasiswa

echo ============================================================
echo    Sistem Manajemen Minat Olahraga Mahasiswa
echo ============================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from https://python.org
    pause
    exit /b 1
)

echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo Starting application...
echo.

python main.py

echo.
echo Application ended.
pause
