@echo off
REM ============================================================================
REM  Rafid - start both background services
REM ============================================================================
REM  Rafid needs two processes running:
REM     1. n8n            - the workflow engine (http://localhost:5678)
REM     2. rafid_bridge   - n8n's way of reaching Claude Code (port 8900)
REM
REM  NOT INSTALLED / NOT ACTIVE.
REM  This file does nothing until you either double-click it, or copy it into
REM  your Startup folder (Win+R -> shell:startup) to run automatically at login.
REM
REM  Recommendation: keep it manual until the build is finished. During
REM  development you want to control when things restart, and an n8n you forgot
REM  was running is a confusing thing to debug against.
REM
REM  To stop: close the two windows it opens, or run stop-rafid.bat
REM ============================================================================

setlocal

REM Folder this script lives in (with trailing backslash)
set "RAFID_DIR=%~dp0"
REM The bridge lives in a sibling folder: rafid\scripts\ -> rafid\bridge\
set "BRIDGE=%RAFID_DIR%..\bridge\rafid_bridge.py"

echo Starting Rafid services...
echo.

REM --- 1. the Claude Code bridge -------------------------------------------
if not exist "%BRIDGE%" (
    echo [ERROR] rafid_bridge.py not found.
    echo         Expected at: %BRIDGE%
    pause
    exit /b 1
)
echo   - rafid-bridge  ^(http://127.0.0.1:8900^)
start "Rafid Bridge" /min cmd /c python "%BRIDGE%"

REM --- 2. n8n ---------------------------------------------------------------
echo   - n8n           ^(http://localhost:5678^)
start "n8n" /min cmd /c n8n start

echo.
echo Both services launching in minimised windows.
echo   n8n takes 20-30 seconds to boot the first time.
echo.
echo   Editor : http://localhost:5678
echo   Bridge : http://127.0.0.1:8900/health
echo.
echo Closing this window is fine - the services run in their own windows.
timeout /t 8 >nul

endlocal
