@echo off
rem Internal runner. ASCII only, CRLF line endings (see launcher notes).
title Lion Code
cd /d "%~dp0"
set "PY=%~dp0.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" "%~dp0_start_mimo.py"
set "RC=%errorlevel%"
echo.
echo -- exited, code %RC% --
pause >nul
