@echo off
chcp 65001 > nul
setlocal

cls
echo ===========================================
echo          欢迎使用代码同步工具
echo ===========================================

REM 切换到脚本所在目录
cd /d "%~dp0"

REM 检查Git是否可用
git --version > nul 2>&1
if errorlevel 1 (
    echo [错误] 无法找到Git, 请确保Git已正确安装。
    pause
    exit /b 1
)

REM --- Git 配置 ---
echo [配置] 正在设置Git用户信息...
git config user.email "1263247980@qq.com"
git config user.name "ZENG-03"

echo.
echo [检查] 正在检查远程仓库配置...
git remote -v | findstr "origin" > nul
if errorlevel 1 (
    echo [配置] 未找到远程仓库 'origin'，正在添加...
    git remote add origin https://github.com/ZENG-03/vip-video-parser.git
)

echo.
echo [更新] 正在添加所有更改...
git add .

echo.
set /p commit_msg="请输入本次提交的说明 (直接回车将使用默认说明): "
if "%commit_msg%"=="" set "commit_msg=更新代码"

echo.
echo [提交] 正在提交更改...
git commit -m "%commit_msg%"
if errorlevel 1 (
    if not "%errorlevel%"=="0" (
        echo [提示] 可能没有需要提交的更改。将继续尝试推送。
    )
)

echo.
echo [推送] 正在推送到GitHub...
git push origin main
if errorlevel 1 (
    echo [错误] 推送失败。请检查网络连接和GitHub权限。
    pause
) else (
    echo [完成] 同步成功！
)

echo.
echo ===========================================
endlocal
pause