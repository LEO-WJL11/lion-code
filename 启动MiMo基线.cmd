@echo off
rem ── 启动 MiMo Code 原版前端（改造基线）─────────────────────────
rem
rem 【为什么用 Windows Terminal + cmd /k】
rem MiMo 的 app.tsx 会调 win32InstallCtrlCGuard() / win32DisableProcessedInput()，
rem 用 FFI 直接 SetConsoleMode 改控制台模式。老式 cmd 窗口在这之后会异常
rem （实测：窗口一闪就关，连 pause 都拦不住）。
rem   · wt.exe  —— 现代终端，对控制台模式改动兼容
rem   · cmd /k  —— 程序退出后窗口也不关，能看到报错
rem
rem 【依赖布局】必须是 hoisted（bun install --linker=hoisted --ignore-scripts），
rem 否则 packages/*/node_modules 的旧副本挡住根目录完整依赖，
rem 报 Cannot find module 'drizzle-orm/sqlite-core'。
chcp 65001 >nul
set "BUN=%APPDATA%\npm\bun.cmd"
if not exist "%BUN%" set "BUN=bun"
set "DIR=%~dp0MiMo-Code-main\packages\cli"
set "WT=%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe"

if exist "%WT%" (
    start "" "%WT%" -d "%DIR%" cmd /k ""%BUN%" run --conditions=browser ./src/index.ts"
) else (
    start "" cmd /k "cd /d "%DIR%" && "%BUN%" run --conditions=browser ./src/index.ts"
)