@echo off
chcp 65001>nul
cls
echo ===========================================
echo          欢迎使用代码同步工具
echo ===========================================

REM 设置Git的完整路径
set "GIT_PATH=C:\Program Files\Git\cmd\git.exe"

REM --- 请在这里配置你的仓库信息 ---
set "GITEE_USERNAME=zeng03"
set "GITHUB_REPO_URL=https://github.com/你的用户名/你的仓库名.git"
REM ------------------------------------

REM 检查Git是否可用
"%GIT_PATH%" --version > nul 2>&1
if errorlevel 1 (
    echo [错误] 无法找到Git，请确保Git已正确安装
    echo 您可以从 https://git-scm.com/downloads 下载安装Git
    pause
    exit /b 1
)

REM 添加安全目录配置
echo [配置] 添加安全目录...
"%GIT_PATH%" config --global --add safe.directory "F:/PYTHON  ZUOYE/HAOWAN DAIMA/1Python抓取VIP电影免费看"

REM 检查是否是首次运行
if not exist ".git" (
    echo [初始化] 首次运行，正在初始化Git仓库...
    "%GIT_PATH%" init

    echo [配置] 设置远程仓库...
    "%GIT_PATH%" remote add gitee "https://gitee.com/%GITEE_USERNAME%/vip-video-parser.git"
    "%GIT_PATH%" remote add origin "%GITHUB_REPO_URL%"

    echo.
    echo [配置] 配置Git用户信息...
    set "GIT_NAME=zeng03"
    set "GIT_EMAIL=1263247980@qq.com"

    "%GIT_PATH%" config user.name "%GIT_NAME%"
    "%GIT_PATH%" config user.email "%GIT_EMAIL%"

    REM 创建并切换到master分支
    "%GIT_PATH%" checkout -b master

    echo.
    echo [初始化] 准备首次提交...
    "%GIT_PATH%" add .
    "%GIT_PATH%" commit -m "初始化项目"

    if errorlevel 1 (
        echo [错误] 提交失败，请检查文件状态
        pause
        exit /b 1
    )

    echo.
    echo [推送] 正在推送到Gitee...
    "%GIT_PATH%" push -u gitee master

    echo.
    echo [推送] 正在推送到GitHub...
    "%GIT_PATH%" push -u origin master:main

    if errorlevel 1 (
        echo [错误] 推送到GitHub失败，请检查 GITHUB_REPO_URL 是否正确
        pause
    )

    echo.
    echo [完成] 初始化完成！
) else (
    echo.
    echo [更新] 正在同步最新改动...
    "%GIT_PATH%" add .
    set /p commit_msg="请输入本次提交的说明 (直接回车将使用默认说明): "
    if "%commit_msg%"=="" (
        set "commit_msg=更新代码"
    )
    "%GIT_PATH%" commit -m "%commit_msg%"

    REM 获取当前分支名
    for /f "tokens=*" %%i in ('"%GIT_PATH%" rev-parse --abbrev-ref HEAD') do set CURRENT_BRANCH=%%i

    REM 推送到 Gitee
    echo.
    echo [推送] 正在推送到 Gitee...
    "%GIT_PATH%" push gitee %CURRENT_BRANCH%
    if errorlevel 1 (
        echo [错误] 推送到 Gitee 失败，请检查网络和权限��
    )

    REM 推送到 GitHub
    echo.
    echo [推送] 正在推送到 GitHub...
    "%GIT_PATH%" push origin %CURRENT_BRANCH%:main
    if errorlevel 1 (
        echo [错误] 推送到 GitHub 失败，请检查网络和权限。
    )

    echo.
    echo [完成] 同步完成！
)

echo.
echo ===========================================
pause
