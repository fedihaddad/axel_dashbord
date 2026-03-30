"""
Main Window - AXEL Control Application

AXEL is a copy/clone of InMoov 2 with full humanoid structure:
- 20 joints total (2 head + 2x9 arm/hand joints)
- 2 full arms with shoulder, elbow, wrist, hand
- 5 fingers per hand (thumb, index, middle, ring, pinky)
- Tendon-driven hand mechanism visualization

PyQt6 application entry point with splash screen and connection dialog.
Integrates all GUI panels and manages application lifecycle.
"""

import sys
import yaml
from pathlib import Path
from typing import Optional

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTabWidget, QStatusBar, QLabel, QMessageBox
    )
    from PyQt6.QtCore import Qt, QTimer
    from PyQt6.QtGui import QIcon, QFont
    PYQT6_AVAILABLE = True
except ImportError:
    PYQT6_AVAILABLE = False
    print("WARNING: PyQt6 not available. Install with: pip install PyQt6")

from axel_core import StateManager, RobotController, SafetyManager
from axel_ros2 import ROSBridge, NodeManager
from axel_gui.splash_screen import AXELSplashScreen
from axel_gui.connection_dialog import ConnectionDialog
from axel_gui.widgets import ControlPanel, Visualization3DPanel


class AXELMainWindow:
    """
    Main application window for AXEL robot control.
    
    AXEL is a copy/clone of InMoov 2 (same structure, 20 joints, 2 full arms).
    
    Manages:
    - Splash screen animation on startup
    - Robot connection dialog (Ethernet/WiFi)
    - Window layout with multi-tab control (Head, Arms, Hands)
    - 3D visualization of 2 full arms with fingers
    - Application state
    - ROS integration
    - Timer-based UI updates
    """

    def __init__(self):
        """Initialize main window."""
        if not PYQT6_AVAILABLE:
            raise RuntimeError("PyQt6 is required. Install with: pip install PyQt6")

        self.app = None
        self.window = None
        self.splash_screen = None
        
        # Core modules
        self.state_manager: Optional[StateManager] = None
        self.robot_controller: Optional[RobotController] = None
        self.safety_manager: Optional[SafetyManager] = None
        self.ros_bridge: Optional[ROSBridge] = None
        self.node_manager: Optional[NodeManager] = None
        
        # Configuration
        self.config = self._load_config()
        
        # Connection info
        self.connected = False
        self.connection_type = None
        self.connection_ip = None
        self.connection_port = None
        
        # UI state
        self.status_bar = None
        self.update_timer = None

    def _load_config(self) -> dict:
        """Load configuration from YAML file."""
        config_path = Path(__file__).parent.parent / "config" / "robot_config.yaml"
        try:
            with open(config_path) as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
            return {}

    def show_splash_screen(self) -> None:
        """Show animated splash screen on startup"""
        print("Showing splash screen...")
        self.splash_screen = AXELSplashScreen()
        self.splash_screen.show_with_animation()
        
        # Process events to show splash
        self.app.processEvents()

    def wait_for_splash_completion(self) -> None:
        """Wait for splash screen animation to complete"""
        if self.splash_screen:
            # Keep processing events until animation is done
            while self.splash_screen.animation_step < self.splash_screen.max_steps:
                self.app.processEvents()
                QTimer(self.app).singleShot(30, self.app.quit)
                self.app.exec()

    def show_connection_dialog(self) -> bool:
        """
        Show connection dialog for user to select Ethernet or WiFi.
        
        Returns:
            True if connection successful, False otherwise
        """
        print("Showing connection dialog...")
        
        # Create dialog without parent to ensure it shows
        dialog = ConnectionDialog(self.config, parent=None)
        dialog.connection_established.connect(self.on_connection_established)
        
        # Show dialog and wait for user response
        result = dialog.exec()
        
        return self.connected and result

    def on_connection_established(self, connection_type: str, ip: str, port: int) -> None:
        """
        Handle successful connection.
        
        Args:
            connection_type: "ethernet" or "wifi"
            ip: Robot IP address
            port: Robot port
        """
        self.connected = True
        self.connection_type = connection_type
        self.connection_ip = ip
        self.connection_port = port
        
        # Update state manager with connection info
        self.state_manager.update_connection_status("connected", connection_type)
        
        print(f"✓ Connected via {connection_type.upper()} at {ip}:{port}")
        print(f"Ready to control AXEL robot (20 joints, 2 full arms, 5 fingers per hand)!")

    def initialize_core_modules(self) -> None:
        """Initialize core robot modules."""
        print("Initializing core modules...")
        
        # Create core modules
        self.safety_manager = SafetyManager()
        self.state_manager = StateManager()
        self.robot_controller = RobotController(
            state_manager=self.state_manager,
            safety_manager=self.safety_manager
        )
        
        # Set up safety constraints from config
        if "robot" in self.config and "joints" in self.config["robot"]:
            for joint_config in self.config["robot"]["joints"]:
                from axel_core.safety_manager import JointLimits
                limits = JointLimits(
                    joint_name=joint_config["name"],
                    min_position=joint_config.get("min_position", -3.14),
                    max_position=joint_config.get("max_position", 3.14),
                    max_velocity=joint_config.get("max_velocity", 1.0),
                    max_effort=joint_config.get("max_effort", 10.0),
                )
                self.safety_manager.set_joint_limits(joint_config["name"], limits)
        
        print("[OK] Core modules initialized")

    def initialize_ros(self) -> None:
        """Initialize ROS 2 integration."""
        print("Initializing ROS 2...")
        try:
            # Create node manager
            ros_config = self.config.get("ros2", {})
            node_name = ros_config.get("node_name", "axel_control")
            
            self.node_manager = NodeManager(node_name=node_name)
            self.node_manager.create_node()
            self.node_manager.spin_in_thread()
            
            # Create ROS bridge
            self.ros_bridge = ROSBridge(
                state_manager=self.state_manager,
                robot_controller=self.robot_controller
            )
            self.ros_bridge.initialize_subscribers()
            self.ros_bridge.initialize_publishers()
            
            print("[OK] ROS 2 initialized (or running in simulation mode)")
        except Exception as e:
            print(f"⚠ ROS 2 initialization warning: {e}")
            print("  Continuing in simulation mode...")

    def setup_ui(self) -> None:
        """Set up the user interface."""
        if not PYQT6_AVAILABLE:
            return

        print("Setting up UI...")
        
        # Create main window
        self.window = QMainWindow()
        self.window.setWindowTitle("AXEL Robot Control Station - Full Humanoid with 20 Joints")
        
        # Get window size from config
        gui_config = self.config.get("gui", {})
        width = gui_config.get("window_width", 1400)
        height = gui_config.get("window_height", 900)
        self.window.resize(width, height)
        
        # Create central widget
        central_widget = QWidget()
        self.window.setCentralWidget(central_widget)
        
        # Create main layout
        layout = QVBoxLayout()
        
        # Create tab widget for different panels
        tabs = QTabWidget()
        
        # Control Panel (real implementation!)
        control_panel = ControlPanel(
            self.robot_controller,
            self.state_manager,
            self.config
        )
        
        # 3D Visualization (real implementation!)
        visualization_panel = Visualization3DPanel(
            self.state_manager,
            self.config
        )
        
        # Placeholder for other widgets (to be created later)
        monitoring_widget = self._create_placeholder_widget("Monitoring Panel")
        logs_widget = self._create_placeholder_widget("Logs & Alerts")
        safety_widget = self._create_placeholder_widget("Safety Control")
        
        # Add tabs
        tabs.addTab(monitoring_widget, "Monitoring")
        tabs.addTab(control_panel, "Control")
        tabs.addTab(visualization_panel, "Visualization")
        tabs.addTab(logs_widget, "Logs")
        tabs.addTab(safety_widget, "Safety")
        
        layout.addWidget(tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.window.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        central_widget.setLayout(layout)
        
        # Setup update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_ui)
        update_rate = gui_config.get("update_rate", 30)
        self.update_timer.start(int(1000 / update_rate))  # Convert Hz to ms
        
        print("[OK] UI setup complete")

    def _create_placeholder_widget(self, title: str) -> QWidget:
        """Create a placeholder widget for future implementation."""
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel(f"{title}\n(To be implemented)")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = label.font()
        font.setPointSize(14)
        label.setFont(font)
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

    def _update_ui(self) -> None:
        """Update UI with current robot state."""
        if self.state_manager:
            state = self.state_manager.get_current_state()
            status = f"Mode: {state.mode} | Connection: {state.connection_type.upper() if state.connection_type else 'N/A'} | " \
                     f"Temp: {state.cpu_temp:.1f}°C | E-STOP: {'ACTIVE' if state.emergency_stop else 'OK'}"
            self.status_bar.showMessage(status)

    def run(self) -> int:
        """Run the application."""
        if not PYQT6_AVAILABLE:
            print("ERROR: PyQt6 is required but not installed.")
            return 1

        try:
            # STEP 1: Show splash screen with AXEL animation
            self.show_splash_screen()
            
            # STEP 2: Initialize core modules (before UI setup)
            self.initialize_core_modules()
            self.initialize_ros()
            
            # STEP 3: Close splash screen
            if self.splash_screen:
                self.splash_screen.close()
            
            # Give system time to process events
            self.app.processEvents()
            
            # STEP 4: Show connection dialog (BEFORE main window)
            print("\nWaiting for robot connection...")
            if not self.show_connection_dialog():
                print("Connection cancelled by user")
                return 0
            
            # STEP 5: Create and show main window (after connection confirmed)
            self.setup_ui()
            self.window.show()
            
            print("=" * 60)
            print("="*60)
            print("AXEL Robot Control Station Started")
            print("Full humanoid (InMoov 2 clone) with 2 arms, 5 fingers per hand")
            print("="*60)
            print(f"Connected: {self.connection_type.upper()} | {self.connection_ip}:{self.connection_port}")
            print("=" * 60)
            
            # Run application
            return self.app.exec()
        
        except Exception as e:
            print(f"ERROR: Failed to start application: {e}")
            import traceback
            traceback.print_exc()
            return 1

    def shutdown(self) -> None:
        """Clean up and shutdown."""
        print("Shutting down...")
        
        if self.update_timer:
            self.update_timer.stop()
        
        if self.node_manager:
            self.node_manager.shutdown()
        
        if self.ros_bridge:
            self.ros_bridge.shutdown()
        
        print("[OK] Shutdown complete")


def main() -> int:
    """Application entry point."""
    if not PYQT6_AVAILABLE:
        print("ERROR: PyQt6 is required. Install with: pip install PyQt6")
        return 1
    
    app = QApplication(sys.argv)
    
    # Create and run main window
    main_window = AXELMainWindow()
    main_window.app = app
    
    exit_code = main_window.run()
    
    main_window.shutdown()
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
