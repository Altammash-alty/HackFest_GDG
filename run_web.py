"""
Launcher script for MedMitra Web Application
Run this to start the web server
"""
from medmitra.app import app, socketio, setup_sample_medications, initialize_scheduler
import os

if __name__ == '__main__':
    # Setup sample medications
    setup_sample_medications()
    
    # Initialize scheduler
    initialize_scheduler()
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Try to get local IP address
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "YOUR_IP_ADDRESS"
    
    print("\n" + "="*70)
    print("  🏥 MedMitra Web Server Starting...")
    print("="*70)
    print(f"🌐 Local:    http://localhost:{port}")
    print(f"📱 Mobile:   http://{local_ip}:{port}")
    print(f"💻 Network:  http://0.0.0.0:{port}")
    print("="*70)
    print("\n📱 To access from mobile device:")
    print(f"   1. Connect mobile to same Wi-Fi network")
    print(f"   2. Open browser and go to: http://{local_ip}:{port}")
    print(f"   3. Install as app for easy access (PWA)")
    print("\n   See MOBILE_ACCESS.md for detailed instructions")
    print("\nPress Ctrl+C to stop the server\n")
    print("="*70 + "\n")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=debug, allow_unsafe_werkzeug=True)

