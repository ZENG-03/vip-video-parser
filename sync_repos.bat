@echo off
chcp 65001 > nul
setlocal

cls
echo ===========================================
echo          GitHub Pages 部署工具
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
echo [清理] 正在删除不需要的文件...

REM 如果存在.gitignore文件，则创建一个
if not exist .gitignore (
    echo [创建] 正在创建.gitignore文件...
    (
        echo # 忽略Python生成的文件
        echo __pycache__/
        echo *.py[cod]
        echo *$py.class
        echo *.so
        echo .Python
        echo env/
        echo build/
        echo develop-eggs/
        echo dist/
        echo downloads/
        echo eggs/
        echo .eggs/
        echo lib/
        echo lib64/
        echo parts/
        echo sdist/
        echo var/
        echo *.egg-info/
        echo .installed.cfg
        echo *.egg
        echo # 忽略IDE文件
        echo .idea/
        echo .vscode/
        echo # 忽略VLC目录
        echo vlc-3.0.0/
    ) > .gitignore
)

echo.
echo [更新] 正在添加所有更改...
git add index.html README.md sync_repos.bat .gitignore

echo.
set /p commit_msg="请输入本次提交的说明 (直接回车将使用默认说明): "
if "%commit_msg%"=="" set "commit_msg=更新为纯前端版本，优化GitHub Pages部署"

echo.
echo [提交] 正在提交更改...
git commit -m "%commit_msg%"
if errorlevel 1 (
    if not "%errorlevel%"=="0" (
        echo [提示] 可能没有需要提交的更改。将继续尝试推送。
    )
)

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
    pause
) else (
    echo [完成] 同步成功！
    echo.
    echo [GitHub Pages] 请检查GitHub仓库设置，确保已启用GitHub Pages：
    echo 1. 访问 https://github.com/ZENG-03/vip-video-parser/settings/pages
    echo 2. 在"Source"部分选择"main"分支
    echo 3. 点击"Save"保存设置
    echo.
    echo 部署成功后，您的网站将可以通过以下地址访问：
    echo https://zeng-03.github.io/vip-video-parser
)

echo.
echo ===========================================
endlocal
pause