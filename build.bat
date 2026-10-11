@echo off
rem ---------------------------------------------------------------
rem Lion Code - one-shot build: clear caches -> Nuitka x3 -> Inno6
rem Run me by double-clicking or from cmd:   build.bat
rem
rem Rules for this file (learned the hard way):
rem   - ASCII only: cmd.exe parses .cmd/.bat in the console codepage (GBK on
rem     Chinese Windows), so non-ASCII literals break.
rem   - CRLF line endings: cmd mis-parses LF-only batch files.
rem   - Never inline complex quoting here - real logic lives in build.ps1.
rem ---------------------------------------------------------------
setlocal
cd /d "%~dp0"
set "PS=powershell"
where "%PS%" >nul 2>&1
if errorlevel 1 set "PS=powershell.exe"

echo ============================================================
echo   Lion Code build : caches -> Nuitka x3 -> Inno Setup 6
echo   Output is NOT filtered - if a stage fails you will see
echo   the real error below.
echo ============================================================
echo.

call "%PS%" -NoProfile -ExecutionPolicy Bypass -File "%~dp0build.ps1"
set "RC=%errorlevel%"

echo.
echo ============================================================
if "%RC%"=="0" (
  echo   RESULT: OK   exit code 0
) else (
  echo   RESULT: FAILED   exit code %RC%   - see [FAIL] lines above
)
echo ============================================================
echo.
echo Press any key to close this window...
pause >nul
rem %RC% does not survive endlocal - carry it on the SAME line, otherwise this
rem script always exits 0 even when the build failed (it just did: printed
rem "RESULT: FAILED exit code 1" but returned 0).
endlocal & exit /b %RC%