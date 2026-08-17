@echo off
REM ============================================================================
REM  Rafid - stop both background services
REM ============================================================================
REM  Kills the n8n and rafid_bridge processes started by start-rafid.bat.
REM  NOT INSTALLED / NOT ACTIVE - only runs when you double-click it.
REM
REM  Note: this kills ALL node and python processes matching those window
REM  titles. If you have other node/python work running, close the two Rafid
REM  windows by hand instead.
REM ============================================================================

setlocal
set "RAFID_DIR=%~dp0"

echo Stopping Rafid services...

taskkill /FI "WINDOWTITLE eq Rafid Bridge*" /T /F >nul 2>&1
if %errorlevel%==0 (echo   - rafid-bridge stopped) else (echo   - rafid-bridge was not running)

taskkill /FI "WINDOWTITLE eq n8n*" /T /F >nul 2>&1
if %errorlevel%==0 (echo   - n8n stopped) else (echo   - n8n was not running)

REM --- checkpoint n8n's database ------------------------------------------
REM n8n runs windowless, so it cannot be asked to close gracefully - the kill
REM above is always a hard one. That leaves SQLite's write-ahead log
REM uncheckpointed, which is what produces "503 Database is not ready!" on the
REM next start. Merging the WAL back in here makes the next boot clean.
echo   - checkpointing the n8n database...
timeout /t 2 >nul
python -c "import os,sqlite3;d=os.path.join(os.path.expanduser('~'),'.n8n','database.sqlite');c=sqlite3.connect(d,timeout=120);c.execute('pragma wal_checkpoint(TRUNCATE)');c.close();print('     done')" 2>nul
if not %errorlevel%==0 echo      (skipped - python not on PATH)

echo.
echo Done.
timeout /t 4 >nul
endlocal
