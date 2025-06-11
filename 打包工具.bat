@echo off
chcp 65001 >nul
echo ========================================
echo 文件重命名工具打包脚本
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
echo.

echo 正在安装PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo 警告: PyInstaller安装可能失败，尝试继续...
)

echo.
echo 开始打包...
echo.

pyinstaller --onefile --windowed --name="文件重命名工具_v2.0" --clean "files_renames.py"

if errorlevel 1 (
    echo.
    echo 打包失败！请检查错误信息
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 可执行文件位置: dist\文件重命名工具_v2.0.exe
echo.
echo 你可以将此文件复制到任何Windows电脑上使用
echo 无需安装Python环境
echo.

if exist "dist\文件重命名工具_v2.0.exe" (
    echo 文件大小:
    dir "dist\文件重命名工具_v2.0.exe" | find "文件重命名工具_v2.0.exe"
    echo.
    echo 是否要打开dist文件夹? (Y/N)
    set /p choice=
    if /i "%choice%"=="Y" (
        explorer dist
    )
)

pause
