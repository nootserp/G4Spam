@echo off
setlocal

echo [*] Checking virtual environment...
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv >nul 2>&1 || exit /b
)

echo [*] Activating virtual environment...
call venv\Scripts\activate.bat || exit /b

echo [*] Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1 || (
    echo [!] pip upgrade failed
    exit /b
)

echo [*] Installing dependencies...
pip install -r requirements.txt >nul 2>&1 || (
    echo [!] requirements install failed
    exit /b
)

echo [*] Running main.py...
python main.py

endlocal
pause
