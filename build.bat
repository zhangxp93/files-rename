@echo off
chcp 65001 >nul
echo.
echo ╔══════════════════════════════════════╗
echo ║        文件重命名工具 v2.0           ║
echo ║         快速打包脚本                 ║
echo ╚══════════════════════════════════════╝
echo.

echo 🚀 启动打包程序...
cd build
call "一键打包.bat"
cd ..

echo.
echo 打包完成！按任意键退出...
pause >nul
