@echo off
chcp 65001 >nul
echo ========================================
echo 文件重命名工具 - 高级打包脚本 v2.0
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python环境
    echo 请确保已安装Python并添加到PATH环境变量
    pause
    exit /b 1
)

echo Python环境检查通过
python --version
echo.

echo 正在检查并安装依赖...
echo 安装PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo 警告: PyInstaller安装可能失败，尝试继续...
)

echo.
echo 清理旧的打包文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"

echo.
echo 开始打包...
echo 目标文件: files_renames.py
echo 输出名称: 文件重命名工具_v2.0.exe
echo.

REM 使用优化参数打包
pyinstaller ^
    --onefile ^
    --windowed ^
    --name="文件重命名工具_v2.0" ^
    --clean ^
    --optimize=2 ^
    --strip ^
    --exclude-module=PIL ^
    --exclude-module=matplotlib ^
    --exclude-module=numpy ^
    --exclude-module=pandas ^
    --exclude-module=scipy ^
    --exclude-module=IPython ^
    --exclude-module=jupyter ^
    --add-data="README.md;." ^
    --add-data="LICENSE;." ^
    "files_renames.py"

if errorlevel 1 (
    echo.
    echo ========================================
    echo 打包失败！
    echo ========================================
    echo 请检查上面的错误信息
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.

if exist "dist\文件重命名工具_v2.0.exe" (
    echo ✅ 可执行文件已生成
    echo 📁 文件位置: dist\文件重命名工具_v2.0.exe
    echo.
    
    echo 📊 文件信息:
    for %%i in ("dist\文件重命名工具_v2.0.exe") do (
        echo    大小: %%~zi 字节 ^(约 %%~zi/1024/1024 MB^)
        echo    创建时间: %%~ti
    )
    echo.
    
    echo 🎯 使用说明:
    echo    1. 将 dist\文件重命名工具_v2.0.exe 复制到目标电脑
    echo    2. 双击运行，无需安装Python环境
    echo    3. 支持 Windows 7/8/10/11 系统
    echo.
    
    echo 📋 功能特性:
    echo    ✓ 批量文件重命名
    echo    ✓ 预览更改功能
    echo    ✓ 自动备份功能
    echo    ✓ 图形化界面
    echo    ✓ 无需Python环境
    echo.
    
    echo 是否要打开dist文件夹查看结果? (Y/N)
    set /p choice=
    if /i "%choice%"=="Y" (
        explorer dist
    )
    
    echo.
    echo 是否要测试运行打包后的程序? (Y/N)
    set /p test_choice=
    if /i "%test_choice%"=="Y" (
        echo 正在启动程序...
        start "" "dist\文件重命名工具_v2.0.exe"
    )
) else (
    echo ❌ 未找到生成的可执行文件
    echo 请检查打包过程中的错误信息
)

echo.
echo 清理临时文件...
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"

echo.
echo ========================================
echo 打包脚本执行完成
echo ========================================
pause
