@echo off
REM -------------------------------
REM Projex Generator Windows Wrapper
REM Run main.py in current directory of terminal
REM -------------------------------

REM Check python
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [!] Python niet gevonden. Voeg Python toe aan je PATH.
    exit /b 1
)

REM Check GitPython
python -c "import git" 2>nul
IF ERRORLEVEL 1 (
    echo [!] GitPython niet gevonden. Installeer met:
    echo python -m pip install --user GitPython
    exit /b 1
)

REM Run main.py vanuit CWD (waar terminal is geopend)
python "%~dp0main.py" %*
