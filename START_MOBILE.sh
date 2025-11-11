#!/bin/bash

echo "========================================"
echo "  MedMitra Mobile Access Helper"
echo "========================================"
echo ""
echo "Finding your IP address..."
echo ""

# Try different commands to get IP
if command -v ip &> /dev/null; then
    ip addr show | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | cut -d/ -f1
elif command -v ifconfig &> /dev/null; then
    ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}'
else
    hostname -I | awk '{print $1}'
fi

echo ""
echo "========================================"
echo ""
echo "Your IP address is shown above."
echo ""
echo "On your mobile device:"
echo "1. Connect to the same Wi-Fi network"
echo "2. Open browser and go to: http://YOUR_IP:5000"
echo "3. Replace YOUR_IP with the address shown above"
echo ""
echo "Starting MedMitra server..."
echo ""
echo "========================================"
echo ""

python3 run_web.py

