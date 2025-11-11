@echo off
echo ========================================
echo   MedMitra Mobile Access Helper
echo ========================================
echo.
echo Finding your IP address...
echo.

ipconfig | findstr /i "IPv4"

echo.
echo ========================================
echo.
echo Your IP address is shown above.
echo.
echo On your mobile device:
echo 1. Connect to the same Wi-Fi network
echo 2. Open browser and go to: http://YOUR_IP:5000
echo 3. Replace YOUR_IP with the address shown above
echo.
echo Starting MedMitra server...
echo.
echo ========================================
echo.

python run_web.py

pause

