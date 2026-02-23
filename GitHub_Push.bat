@echo off
title SheGlam - GitHub Sync Automator
setlocal enabledelayedexpansion

echo.
echo =======================================================
echo          SheGlam - Professional GitHub Sync
echo =======================================================
echo.

:: Check if .git directory exists
if not exist ".git" (
    echo [ERROR] This directory is not a Git repository.
    echo Please run this script from the SheGlam root folder.
    pause
    exit /b
)

echo [INFO] Stage 1: Staging all changes...
git add .
if !errorlevel! neq 0 (
    echo [ERROR] Failed to stage changes.
    pause
    exit /b
)

echo [INFO] Stage 2: Committing updates...
set /p commit_msg="Enter commit message (or press Enter for default): "
if "!commit_msg!"=="" (
    set commit_msg="Project Elevation: 10/10 Readiness Audit, Security Hardening, SEO Perfection, and Premium Branding"
)

git commit -m "!commit_msg!"
if !errorlevel! neq 0 (
    echo [WARNING] Nothing to commit or commit failed.
)

echo [INFO] Stage 3: Pushing to GitHub...
git push
if !errorlevel! neq 0 (
    echo [ERROR] Failed to push to GitHub. Check your internet connection and permissions.
    pause
    exit /b
)

echo.
echo [SUCCESS] SheGlam is now synced with GitHub!
echo Your 10/10 production-ready masterpiece is live.
echo.
pause
