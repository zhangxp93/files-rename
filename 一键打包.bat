@echo off
chcp 65001 >nul
title 文件重命名工具 - 一键打包

echo.
echo ╔══════════════════════════════════════╗
echo ║        文件重命名工具 v2.0           ║
echo ║           一键打包脚本               ║
echo ╚══════════════════════════════════════╝
echo.

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python环境
    echo 请先安装Python并添加到PATH环境变量
    echo.
    pause
    exit /b 1
)

echo ✅ Python环境检查通过
echo.

REM 安装PyInstaller
echo 📦 正在安装PyInstaller...
pip install pyinstaller >nul 2>&1
echo ✅ PyInstaller安装完成
echo.

REM 清理旧文件
echo 🧹 清理旧的打包文件...
if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "dist" rmdir /s /q "dist" >nul 2>&1
echo ✅ 清理完成
echo.

REM 开始打包
echo 🚀 开始打包程序...
echo    源文件: files_renames.py
echo    目标: 文件重命名工具_v2.0.exe
echo.

pyinstaller "文件重命名工具.spec" --clean >nul 2>&1

if errorlevel 1 (
    echo ❌ 打包失败！
    echo 正在尝试简单打包模式...
    pyinstaller --onefile --windowed --name="文件重命名工具_v2.0" "files_renames.py"
)

REM 检查结果
if exist "dist\文件重命名工具_v2.0.exe" (
    echo.
    echo ╔══════════════════════════════════════╗
    echo ║            打包成功！                ║
    echo ╚══════════════════════════════════════╝
    echo.
    echo 📁 文件位置: dist\文件重命名工具_v2.0.exe
    
    for %%i in ("dist\文件重命名工具_v2.0.exe") do (
        set /a size_mb=%%~zi/1024/1024
    )
    echo 📊 文件大小: %size_mb% MB
    echo.
    echo 🎯 使用说明:
    echo    • 可以在任何Windows电脑上运行
    echo    • 无需安装Python环境
    echo    • 支持Windows 7/8/10/11
    echo.
    
    echo 是否立即测试运行? (Y/N)
    set /p test=
    if /i "%test%"=="Y" (
        echo 🚀 启动程序...
        start "" "dist\文件重命名工具_v2.0.exe"
    )
    
    echo.
    echo 是否打开文件夹? (Y/N)
    set /p open=
    if /i "%open%"=="Y" (
        explorer dist
    )
    
) else (
    echo.
    echo ❌ 打包失败！
    echo 请检查错误信息或手动运行打包命令
)

echo.
echo 🧹 清理临时文件...
if exist "build" rmdir /s /q "build" >nul 2>&1
echo.
echo 打包完成！按任意键退出...
pause >nul
