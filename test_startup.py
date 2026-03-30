"""
Quick Test - Verify Splash Screen and Connection Dialog
Run this to test the startup flow without fully launching the app
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add project to path
sys.path.insert(0, str(__file__).rsplit('\\', 1)[0])

from axel_gui.splash_screen import AXELSplashScreen
from axel_gui.connection_dialog import ConnectionDialog


def test_splash_screen():
    """Test splash screen animation"""
    print("Testing splash screen...")
    
    app = QApplication.instance() or QApplication(sys.argv)
    
    splash = AXELSplashScreen()
    splash.show_with_animation()
    
    print("✓ Splash screen created and animation started")
    
    # Keep it running for 5 seconds
    QTimer.singleShot(5000, app.quit)
    return app.exec()


def test_connection_dialog():
    """Test connection dialog"""
    print("\nTesting connection dialog...")
    
    app = QApplication.instance() or QApplication(sys.argv)
    
    config = {
        "connection": {
            "default_connection": "ethernet",
            "ethernet": {
                "ip_address": "192.168.1.100",
                "port": 5005,
                "timeout": 5
            },
            "wifi": {
                "ip_address": "192.168.1.200",
                "port": 5005,
                "timeout": 5
            }
        }
    }
    
    dialog = ConnectionDialog(config)
    
    def on_connection(conn_type, ip, port):
        print(f"✓ Connection established: {conn_type} at {ip}:{port}")
        app.quit()
    
    dialog.connection_established.connect(on_connection)
    
    print("✓ Connection dialog created and displayed")
    
    # Auto-timeout after 10 seconds
    QTimer.singleShot(10000, app.quit)
    
    return dialog.exec()


if __name__ == "__main__":
    print("=" * 60)
    print("AXEL Startup Components Test")
    print("=" * 60)
    
    try:
        # Test splash
        print("\n[1/2] Testing Splash Screen...")
        test_splash_screen()
        
        # Test connection dialog
        print("\n[2/2] Testing Connection Dialog...")
        print("(Dialog will auto-close in 10 seconds if not closed manually)")
        test_connection_dialog()
        
        print("\n" + "=" * 60)
        print("✓ All startup components working!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
