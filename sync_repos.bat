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
git config user.email "zeng03@users.noreply.github.com"
git config user.name "ZENG-03"

REM --- 尝试修复网络连接问题 ---
echo [网络] 正在设置Git超时参数...
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999

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
echo [修正] 正在更新提交者信息以符合隐私设置...
git commit --amend --no-edit --reset-author > nul

echo.
echo [推送] 正在推送到GitHub (可能需要等待较长时间)...
git push -u origin main
if errorlevel 1 (
    echo [错误] 推送失败，尝试使用替代方法...
    echo.
    echo [备用方法] 您可以尝试以下方法之一：
    echo.
    echo 1. 使用浏览器访问 GitHub，手动上传修改后的文件
    echo    https://github.com/ZENG-03/vip-video-parser
    echo.
    echo 2. 稍后再试，或者使用其他网络环境
    echo.
    echo 3. 打开浏览器直接访问 Vercel 管理页面，重新部署项目
    echo    https://vercel.com/dashboard
    echo.
    echo [提示] 您的代码已成功保存在本地Git仓库中，不会丢失。
    pause
) else (
    echo [完成] 同步成功！
)

echo.
echo ===========================================
endlocal
pause