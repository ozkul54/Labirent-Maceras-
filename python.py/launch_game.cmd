@echo off
setlocal
cd /d "%~dp0"

set "VENV_DIR=%~dp0.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"

where py >nul 2>nul
if errorlevel 1 (
    echo Python bulunamadi. Lutfen Python 3.13 yukleyin.
    pause
    exit /b 1
)

if exist "%VENV_PY%" (
    "%VENV_PY%" -c "import sys; print(sys.executable)" >nul 2>&1
    if errorlevel 1 (
        echo Eski sanal ortam bozuk. Yeniden olusturuluyor...
        rmdir /s /q "%VENV_DIR%"
    )
)

if not exist "%VENV_PY%" (
    echo .venv olusturuluyor. Python 3.13 kullaniliyor...
    py -3.13 -m venv "%VENV_DIR%"
)

if not exist "%VENV_PY%" (
    echo .venv olusturulamadi.
    pause
    exit /b 1
)

"%VENV_PY%" -m pip install --disable-pip-version-check --upgrade pip >nul 2>&1
"%VENV_PY%" -m pip install --disable-pip-version-check pygame-ce >nul 2>&1

"%VENV_PY%" "%~dp0pygame_labirent.py"
exit /b %errorlevel%
