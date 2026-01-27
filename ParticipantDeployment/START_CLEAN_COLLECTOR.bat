@echo off
REM Clean Data Collector - Only Working Parameters

echo ========================================
echo CLEAN DATA COLLECTOR
echo 18 Working Columns Only
echo ========================================
echo.
echo All zero-filled columns removed
echo Only real or calculated data
echo.
echo Press Ctrl+C to stop
echo.
pause

python clean_collector.py

pause
