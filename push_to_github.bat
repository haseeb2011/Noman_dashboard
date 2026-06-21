@echo off
title Push Project to GitHub
echo ===================================================
echo   Yelp Dashboard GitHub Pusher
echo ===================================================
echo.

:: 1. Check if Git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Git is not installed or not in PATH.
    echo [*] Attempting to install Git via winget...
    echo [*] Please accept the Windows administrator prompt (UAC) if it appears.
    echo.
    winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
    if %errorlevel% neq 0 (
        echo.
        echo [x] Winget installation failed. Please install Git manually from https://git-scm.com/downloads
        goto end
    )
    echo.
    echo [+] Git installed successfully. Reloading environment PATH...
    :: Refresh PATH for the current CMD session
    set "PATH=%PATH%;C:\Program Files\Git\cmd;C:\Program Files\Git\bin"
) else (
    echo [+] Git is already installed.
)

:: 2. Initialize Git if not already done
if not exist .git (
    echo [*] Initializing Git repository...
    git init
) else (
    echo [*] Git repository already initialized.
)

:: 3. Configure Remote Origin
echo [*] Configuring remote origin to: https://github.com/haseeb2011/Noman_yelp_dashboard.git
git remote remove origin >nul 2>nul
git remote add origin https://github.com/haseeb2011/Noman_yelp_dashboard.git

:: 4. Add Files and Commit
echo [*] Staging files (ignoring raw datasets)...
git add .
echo [*] Creating commit...
git commit -m "Initial commit: Redesigned Tabbed BI Dashboard"

:: 5. Rename branch to main
git branch -M main

:: 6. Push to GitHub
echo.
echo [*] Pushing files to GitHub...
echo [*] Note: A browser window or login popup may appear. Please sign in to authorize the push.
echo.
git push -u origin main

if %errorlevel% eq 0 (
    echo.
    echo ===================================================
    echo [+] SUCCESS! Your project has been pushed to GitHub.
    echo ===================================================
) else (
    echo.
    echo [x] Push failed. If it was an authentication error, please try running the script again.
)

:end
echo.
echo Press any key to exit...
pause >nul
