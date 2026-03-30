"""
AXEL Launcher - Standalone starter with better error handling
Run this to start the AXEL application
"""

import sys
import os

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    try:
        from PyQt6.QtWidgets import QApplication
        from axel_gui.main_window import AXELMainWindow
        
        print("=" * 70)
        print("🤖 AXEL Robot Control System")
        print("=" * 70)
        
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Create main window
        main_window = AXELMainWindow()
        main_window.app = app
        
        print("\n🚀 Starting application...\n")
        
        # Run application
        exit_code = main_window.run()
        
        # Cleanup
        main_window.shutdown()
        
        sys.exit(exit_code)
    
    except ImportError as e:
        print(f"❌ ERROR: Missing required module: {e}")
        print("\n📦 Please install dependencies:")
        print("   pip install PyQt6 PyYAML pydantic")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
