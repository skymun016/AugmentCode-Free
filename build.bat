@echo off
chcp 65001 >nul
echo ====================================
echo    AugmentCode-Free Windows 打包工具
echo ====================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安装或未添加到PATH
    echo 请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

echo ✅ Python 已安装
echo.

REM 运行打包脚本
echo 开始打包...
python build.py

echo.
echo 打包完成！按任意键退出...
pause >nul
