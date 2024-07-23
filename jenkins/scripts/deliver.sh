@echo off

echo The following command builds your Node.js/React application for
echo production in the local "build" directory (i.e. within the
echo "/var/jenkins_home/workspace/simple-node-js-react-app" directory),
echo correctly bundles React in production mode and optimizes the build for
echo the best performance.
echo on
npm run build
echo off

echo The following command runs your Node.js/React application in
echo development mode and makes the application available for web browsing.
echo The "npm start" command runs as a background process (i.e. asynchronously).
echo "npm start" is followed by another command that retrieves the process ID (PID)
echo of the previously run process (i.e. "npm start") and writes this value to
echo the file ".pidfile".
echo on
start npm start
REM Wait a bit to ensure the process starts and gets a PID
ping 127.0.0.1 -n 5 > nul
for /f "tokens=2 delims=," %%a in ('tasklist /fi "imagename eq node.exe" /fo csv') do set PID=%%a
echo %PID% > .pidfile
echo off

echo Now...
echo Visit http://localhost:3000 to see your Node.js/React application in action.
echo (This is why you specified the "args ''-p 3000:3000''" parameter when you
echo created your initial Pipeline as a Jenkinsfile.)
