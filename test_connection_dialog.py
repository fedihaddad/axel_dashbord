"""
Quick Connection Dialog Test
Test if connection dialog appears properly
"""

import sys
import yaml
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from axel_gui.connection_dialog import ConnectionDialog


def load_config():
    """Load robot config"""
    config_path = Path(__file__).parent / "config" / "robot_config.yaml"
    try:
        with open(config_path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Warning: Could not load config: {e}")
        return {}


if __name__ == "__main__":
    print("=" * 60)
    print("🔌 Connection Dialog Test")
    print("=" * 60)
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Load config
    config = load_config()
    
    # Create dialog
    print("\n🔗 Creating connection dialog...")
    dialog = ConnectionDialog(config, parent=None)
    
    # Handle connection
    def on_connected(conn_type, ip, port):
        print(f"\n✅ SUCCESS: Connected via {conn_type.upper()}")
        print(f"   IP: {ip}:{port}")
        app.quit()
    
    dialog.connection_established.connect(on_connected)
    
    # Show dialog
    print("🖼  Showing dialog (should appear on screen)...")
    dialog.show()
    
    # Process events
    app.processEvents()
    
    # Run dialog
    print("\n⏳ Waiting for user input (dialog should be visible)...\n")
    result = dialog.exec()
    
    if result == 0:
        print("\n❌ Dialog cancelled or closed")
    
    sys.exit(0)
