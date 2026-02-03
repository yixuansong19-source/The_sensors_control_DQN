@echo off
REM 激活虚拟环境并运行快速仿真脚本

setlocal enabledelayedexpansion

echo.
echo ================================================
echo RADAR TARGET TRACKING - QUICK START
echo ================================================
echo.

REM 检查虚拟环境
if not exist "..\parl-env\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found at ..\parl-env
    pause
    exit /b 1
)

REM 激活虚拟环境
call ..\parl-env\Scripts\activate.bat

REM 显示菜单
echo Choose simulation mode:
echo 1. Quick test (single episode)
echo 2. Full simulation (multiple episodes)
echo 3. Open menu launcher
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Running quick simulation...
    python quick_simulate.py
) else if "%choice%"=="2" (
    echo Running full simulation...
    python simulate_and_visualize.py --episodes 3 --save-dir ./results --show
) else if "%choice%"=="3" (
    echo Opening menu launcher...
    python launcher.py
) else (
    echo Invalid choice
)

pause
