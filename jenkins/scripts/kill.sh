@echo off

echo The following command terminates the "npm start" process using its PID
echo (written to ".pidfile"), all of which were conducted when "deliver.bat"
echo was executed.
echo on
set /p PID=<.pidfile
taskkill /F /PID %PID%
echo off
