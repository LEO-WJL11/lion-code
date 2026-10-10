@echo off
rem Internal runner (installed copy). ASCII only, CRLF line endings.
rem The installed tree ships the compiled launcher instead of Python sources:
rem   start.exe = stage 1 backend :18080, stage 2 adapter :8791,
rem               stage 3 MiMo TUI attach, plus the watchdog that restarts
rem               stages 1 and 2 if they die.
title Lion Code
cd /d "%~dp0"
set "START=%~dp0start.exe"
if not exist "%START%" (
    echo missing start.exe
    pause
    exit /b 1
)
"%START%"
set "RC=%errorlevel%"
echo.
echo -- exited, code %RC% --
pause >nul
