@echo off
rem lion-code command: start Lion Code in THIS console.
rem
rem The MiMo TUI pokes the console mode through FFI, so it needs a real
rem terminal: do NOT use "start" (new window) and do NOT run it hidden.
rem
rem Keep this file ASCII-only with CRLF endings: cmd.exe parses .cmd in the
rem console codepage (GBK on Chinese Windows), so UTF-8 non-ASCII literals
rem break paths, and cmd mis-parses LF-only batch files.
setlocal
set "ROOT=%~dp0"
cd /d "%ROOT%"
"%ROOT%start.exe" %*
set "RC=%errorlevel%"
if not "%RC%"=="0" echo [lion-code] start.exe exited with code %RC%
endlocal & exit /b %RC%
