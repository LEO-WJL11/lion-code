@echo off
rem Install the MiMo TUI dependencies (Plan B: pre-packed 7z, no network).
rem ASCII only, CRLF. Everything is logged to install-deps.log in the app dir.
rem
rem WHY NOT "bun install" here: measured on this machine - bun's link phase
rem failed with 380-470 "ENOENT ... failed to symlink" errors under every
rem combination (cold/warm cache, frozen or not, 3 different TEMP targets,
rem clean tree, same shell that once succeeded). The one variable left was
rem wall-clock time: the identical command succeeded at 01:03 and failed from
rem 01:51 on. So the installer ships the PROVEN dev tree instead: node_modules
rem packed with 7za (-snh hardlink dedup, -snl junctions kept as links), plus
rem relink-nm.cmd which re-creates the junctions 7z leaves as empty folders.
rem
rem PHASE ARGUMENT - the Inno script runs this twice so the wizard can show an
rem honest status line per phase (times measured on this machine):
rem   install_deps.cmd extract  extraction only -> writes install-deps.extracted
rem   install_deps.cmd relink   relink + gates + install-deps.ok, needs the
rem                             extract phase first (checks the marker above)
rem   install_deps.cmd          the classic all-in-one run (this is what the
rem                             retry dialog in the installer tells you to run)
rem
rem Exit codes: 3=no 7za.exe  4=no archive or no MiMo dir  5=extract failed
rem             6=relink marker missing or sanity gate failed
setlocal
set "APP=%~dp0"
set "LOG=%APP%install-deps.log"
set "OK=%APP%install-deps.ok"
set "EXT=%APP%install-deps.extracted"
set "MIMO=%APP%MiMo-Code-main"
rem relink phase APPENDS to the log - it must not wipe the extract evidence
if /i "%~1"=="relink" goto relink
del "%OK%" >nul 2>&1
del "%EXT%" >nul 2>&1
del "%APP%relink-nm.done" >nul 2>&1
echo === install deps start %DATE% %TIME% === > "%LOG%"
if not exist "%APP%7za.exe" (
    echo 7za.exe missing: "%APP%7za.exe" >> "%LOG%"
    echo === rc=3 === >> "%LOG%"
    exit /b 3
)
if not exist "%APP%node_modules.7z" (
    echo node_modules.7z missing >> "%LOG%"
    echo === rc=4 === >> "%LOG%"
    exit /b 4
)
if not exist "%MIMO%" (
    echo MiMo-Code-main missing >> "%LOG%"
    echo === rc=4 === >> "%LOG%"
    exit /b 4
)
rem -mmt=on: use EVERY core the TARGET machine has (auto). Was -mmt=16, which
rem oversubscribes on 4/8-core user machines - 16 decoder threads over 4 cores
rem is slower than auto and this runs on hardware we do not control.
echo === extract start %TIME% === >> "%LOG%"
"%APP%7za.exe" x "%APP%node_modules.7z" "-o%MIMO%" -y -mmt=on >> "%LOG%" 2>&1
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" (
    echo extract failed rc=%RC% >> "%LOG%"
    echo === rc=5 === >> "%LOG%"
    exit /b 5
)
echo === extract ok %TIME%, files written === >> "%LOG%"
echo ok > "%EXT%"
if /i "%~1"=="extract" exit /b 0
:relink
echo === relink phase start %DATE% %TIME% === >> "%LOG%"
del "%OK%" >nul 2>&1
del "%APP%relink-nm.done" >nul 2>&1
if not exist "%EXT%" (
    echo extraction marker missing - run install_deps.cmd extract first >> "%LOG%"
    echo === rc=5 === >> "%LOG%"
    exit /b 5
)
call "%APP%relink-nm.cmd" >> "%LOG%" 2>&1
if not exist "%APP%relink-nm.done" (
    echo relink marker missing >> "%LOG%"
    echo === rc=6 === >> "%LOG%"
    exit /b 6
)
rem hard gate: the preload package bun needs first must be there, otherwise
rem the TUI dies later with "preload not found @opentui/solid/preload"
if not exist "%MIMO%\node_modules\@opentui\solid" (
    echo sanity check failed: node_modules\@opentui\solid missing >> "%LOG%"
    echo === rc=6 === >> "%LOG%"
    exit /b 6
)
echo === install deps ok %DATE% %TIME% === >> "%LOG%"
echo ok > "%OK%"
exit /b 0
