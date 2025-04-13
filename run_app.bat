@echo off
cd /d "%~dp0"

echo Starting Financial Audit Assistant...
echo Creating log directory...
if not exist "logs" mkdir logs

echo Starting application with logging...
"dist\Financial_Audit_Assistant.exe" > logs\app.log 2>&1

echo Waiting for server to start...
timeout /t 15 /nobreak

echo Attempting to open browser...
start http://localhost:8501

echo If the application doesn't open automatically, please:
echo 1. Wait a few more seconds and try refreshing your browser
echo 2. Check logs\app.log for any error messages
echo 3. Make sure no other Streamlit applications are running on port 8501

echo Press any key to exit this window...
pause > nul 