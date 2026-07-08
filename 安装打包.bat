@echo off
echo ========================================
echo   PUBG距离测量工具 - 安装与打包
echo ========================================
echo.

echo [1/2] 安装依赖...
pip install -r requirements.txt pyinstaller
if errorlevel 1 (
    echo 依赖安装失败!
    pause
    exit /b 1
)

echo.
echo [2/2] 打包为EXE...
python build.py

echo.
if exist "dist\PUBG距离测量工具.exe" (
    echo ========================================
    echo   打包成功!
    echo   EXE文件在: dist\PUBG距离测量工具.exe
    echo ========================================
) else (
    echo 打包失败，请检查错误信息
)

pause
