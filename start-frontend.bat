@echo off
chcp 65001 >nul
echo ========================================
echo   上理工校园失物招领平台 前端启动
echo ========================================
echo.

echo [1/2] 检查 Node.js 环境...
where node >nul 2>nul
if errorlevel 1 (
    echo 错误: 未找到 Node.js，请先安装 Node.js 16+
    pause
    exit /b 1
)

echo [2/2] 安装前端依赖并启动...
cd /d "%~dp0frontend"
if not exist "node_modules" (
    echo 首次运行，正在安装依赖...
    call npm install
    if errorlevel 1 (
        echo 错误: 前端依赖安装失败
        pause
        exit /b 1
    )
)

echo.
echo 前端地址: http://localhost:5173
echo.
call npm run dev
pause