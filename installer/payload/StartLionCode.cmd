@echo off
rem Lion Code launcher (double-click me). Installed copy.
rem
rem Keep this file ASCII-only: cmd.exe parses .cmd in the console codepage
rem (GBK on Chinese Windows), so UTF-8 non-ASCII literals break paths.
rem Keep CRLF line endings too: cmd.exe mis-parses LF-only batch files.
rem
rem Real work lives in _run_mimo.cmd (no nested quoting). This file only
rem opens a window for it. Windows Terminal is used because MiMo pokes the
rem console mode through FFI and a plain conhost window dies right after.
rem (Logic reused from the repo root launcher on purpose - it already solved
rem  the "TUI needs a real console" problem.)
setlocal
set "ROOT=%~dp0."
set "RUNNER=%~dp0_run_mimo.cmd"
set "WT=%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe"
if not exist "%RUNNER%" (
    echo missing _run_mimo.cmd
    pause
    exit /b 1
)
if exist "%WT%" (
    "%WT%" -d "%ROOT%" cmd /k "%RUNNER%"
    if not errorlevel 1 exit /b 0
)
start "" cmd /k "%RUNNER%"
exit /b 0
