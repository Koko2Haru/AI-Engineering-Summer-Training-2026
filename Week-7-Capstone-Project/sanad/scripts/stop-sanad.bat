@echo off
REM ============================================================================
REM  Sanad - stop both background services
REM ============================================================================
REM  Kills the n8n and sanad_bridge processes started by start-sanad.bat.
REM  NOT INSTALLED / NOT ACTIVE - only runs when you double-click it.
REM
REM  Note: this kills ALL node and python processes matching those window
REM  titles. If you have other node/python work running, close the two Sanad
REM  windows by hand instead.
REM ============================================================================

echo Stopping Sanad services...

taskkill /FI "WINDOWTITLE eq Sanad Bridge*" /T /F >nul 2>&1
if %errorlevel%==0 (echo   - sanad-bridge stopped) else (echo   - sanad-bridge was not running)

taskkill /FI "WINDOWTITLE eq n8n*" /T /F >nul 2>&1
if %errorlevel%==0 (echo   - n8n stopped) else (echo   - n8n was not running)

echo.
echo Done.
timeout /t 4 >nul
