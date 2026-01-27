@echo off
REM Setup Verification - Run this BEFORE data collection

echo ========================================
echo SETUP VERIFICATION
echo ========================================
echo.
echo Checking if everything is ready...
echo.

REM Check 1: Python
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo    ERROR: Python not found!
    echo    Please install Python from python.org
    echo.
    pause
    exit /b 1
) else (
    python --version
    echo    ✓ Python is installed
)
echo.

REM Check 2: CodeBlocks
echo [2/4] Checking CodeBlocks...
where codeblocks.exe >nul 2>&1
if errorlevel 1 (
    echo    WARNING: CodeBlocks not in system PATH
    echo    If CodeBlocks is installed, you can ignore this
) else (
    echo    ✓ CodeBlocks found
)
echo.

REM Check 3: Collector script
echo [3/4] Checking collector script...
if exist "clean_collector.py" (
    echo    ✓ Collector script found
) else (
    echo    ERROR: clean_collector.py missing!
    pause
    exit /b 1
)
echo.

REM Check 4: Output folder access
echo [4/4] Checking Documents folder...
if not exist "%USERPROFILE%\Documents" (
    echo    ERROR: Cannot access Documents folder
    pause
    exit /b 1
) else (
    echo    ✓ Documents folder accessible
)
echo.

echo ========================================
echo VERIFICATION COMPLETE - ALL READY!
echo ========================================
echo.
echo You can now start data collection:
echo 1. Double-click START_CLEAN_COLLECTOR.bat
echo 2. Open CodeBlocks and code normally
echo 3. Press Ctrl+C when done
echo.
echo Data will be saved to:
echo %USERPROFILE%\Documents\AnxietyMonitorData\
echo.
pause
