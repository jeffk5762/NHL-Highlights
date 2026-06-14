@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Run-NHL-Cues.ps1" %*
set "EXIT_CODE=%ERRORLEVEL%"
exit /b %EXIT_CODE%
