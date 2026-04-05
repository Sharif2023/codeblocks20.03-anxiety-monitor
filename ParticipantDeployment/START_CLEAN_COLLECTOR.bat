@echo off
REM Anxiety Monitor - Research Data Collector
REM Campus Lab Deployment Version

cls
echo ============================================================
echo    PROGRAMMING ANXIETY MONITOR - RESEARCH DATA COLLECTOR
echo ============================================================
echo.
echo   Please enter your Student ID before the session starts.
echo   You will be asked to enter it TWICE to confirm.
echo.
echo ============================================================
echo.

:ASK_ID
set "STUDENT_ID="
set /p STUDENT_ID="Enter your Student ID: "

if "%STUDENT_ID%"=="" (
    echo.
    echo   [!] Student ID cannot be empty. Please try again.
    echo.
    goto ASK_ID
)

:CONFIRM_ID
set "STUDENT_ID_CONFIRM="
set /p STUDENT_ID_CONFIRM="Re-enter your Student ID to confirm: "

if "%STUDENT_ID_CONFIRM%"=="" (
    echo.
    echo   [!] Confirmation cannot be empty. Please try again.
    echo.
    goto CONFIRM_ID
)

if /I NOT "%STUDENT_ID%"=="%STUDENT_ID_CONFIRM%" (
    echo.
    echo   [!] IDs do not match. Please start over.
    echo.
    goto ASK_ID
)

cls
echo ============================================================
echo    PROGRAMMING ANXIETY MONITOR - RESEARCH DATA COLLECTOR
echo ============================================================
echo.
echo   Student ID : %STUDENT_ID%
echo   Data file  : %STUDENT_ID%.csv
echo   Location   : Documents\AnxietyMonitorData\
echo.
echo   * Do NOT close this window during your session. *
echo   * Press Ctrl+C only when your session is DONE.  *
echo.
echo ============================================================
echo.
pause

python clean_collector.py %STUDENT_ID%

echo.
echo ============================================================
echo   Session complete. Your data has been saved.
echo   File: Documents\AnxietyMonitorData\%STUDENT_ID%.csv
echo ============================================================
echo.
pause
