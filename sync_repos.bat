@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

cls
echo ===========================================
echo          欢迎使用代码同步工具
echo ===========================================

REM 切换到脚本所��目录
cd /d "%~dp0"

REM 检查Git是否可用
git --version > nul 2>&1
if errorlevel 1 (
    echo [错误] 无法找到Git, 请确保Git已正确安装。
    echo 您可以从 https://git-scm.com/downloads 下载安装。
    pause
    exit /b 1
)

REM 检查是否已初始化Git仓库
if not exist ".git" (
    echo [初始化] 首次运行, 正在初始化Git仓库...
    git init
    git checkout -b main

    echo [配置] 设置Git用户信息...
    git config user.name "zeng03"
    git config user.email "1263247980@qq.com"

    echo [配置] 添加远程仓库...
    git remote add origin https://github.com/ZENG-03/vip-video-parser.git

    echo [初始化] 准备首次提交...
    git add .
    git commit -m "初始化项目"

    echo [推送] 正在推送到GitHub...
    git push -u origin main
    if errorlevel 1 (
        echo [错误] 推送失败, 请检查仓库地址和权限。
        pause
        exit /b 1
    )
) else (
    echo [检查] 确保远程仓库配置正确...
    git remote -v | findstr "origin" > nul
    if errorlevel 1 (
        echo [配置] 添加远程仓库...
        git remote add origin https://github.com/ZENG-03/vip-video-parser.git
    )

    echo [检查] 确保在正确的分支上...
    for /f "tokens=*" %%i in ('git branch --show-current') do set "current_branch=%%i"
    if not "!current_branch!"=="main" (
        echo [分支] 切换到main分支...
        git checkout main 2>nul || git checkout -b main
    )

    echo [更新] 正在获取远程更新...
    git fetch origin main

    echo [更新] 正在同步最新改动...
    git add .

    REM 检查是否有改动需要提交
    git diff --cached --quiet
    if not errorlevel 1 (
        echo [提示] 没有检测到需要提交的更改。
        choice /C YN /M "是否仍要执行空提交"
        if errorlevel 2 goto end
    )

    set /p commit_msg="请输入本次提交的说明 (直接回车将使用默认说明): "
    if "!commit_msg!"=="" (
        set "commit_msg=��新代码"
    )

    echo.
    echo [提交] 正在提交更改...
    git commit -m "!commit_msg!"
    if errorlevel 1 (
        echo [错误] 提交失败，请检查文件状态。
        pause
        exit /b 1
    )

    echo.
    echo [推送] 正在推送到GitHub...
    git push origin main
    if errorlevel 1 (
        echo [错误] 推送失败, 请检查网络连接。
        choice /C YN /M "是否尝试强制推送"
        if errorlevel 1 (
            git push -f origin main
        ) else (
            goto end
        )
    )

    echo.
    echo [完成] 同步完成！
)

:end
echo.
echo ===========================================
endlocal
pause