@echo off
setlocal

if not exist "venv" (
    python -m venv venv
)

REM 
call venv\Scripts\activate.bat

REM
python -m pip install --upgrade pip

REM 
pip install -r requirements.txt

REM
python main.py

endlocal
pause
