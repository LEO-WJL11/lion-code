@echo off
rem ── Lion Code 启动器（双击即可）────────────────────────────────────
rem TUI 需要真终端：双击本文件会开一个控制台窗口，Ink 界面在里面正常渲染。
chcp 65001 >nul
title Lion Code
cd /d "%~dp0"

set "PY=%~dp0.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

"%PY%" "%~dp0main.py" --app-root "%~dp0." %*

rem 出错时留住窗口，方便看信息（正常退出就关掉）
if errorlevel 1 (
    echo.
    echo [Lion Code 已退出，返回码 %errorlevel%]
    pause
)