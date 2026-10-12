@echo off
chcp 65001 >nul
echo ========================================
echo   上理工校园失物招领平台 启动脚本
echo ========================================
echo.

echo [1/4] 检查 Python 环境...
where python >nul 2>nul
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo [2/4] 安装后端依赖...
cd /d "%~dp0backend"
python -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo 错误: 后端依赖安装失败
    pause
    exit /b 1
)

echo [3/4] 初始化数据库（自动建表+创建管理员）...
echo （app.py 启动时已自动初始化，此步可选）
python scripts\seed.py 2>nul

echo [4/4] 启动后端服务...
echo.
echo 后端地址: http://localhost:5000
echo 健康检查: http://localhost:5000/health
echo 管理员账号: admin / admin123（也可用 admin@usst.edu.cn）
echo.
python run.py
pause