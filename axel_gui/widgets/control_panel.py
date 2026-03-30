"""
Control Panel - Joint Slider Interface
Professional robot joint control with real-time feedback
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton,
    QGridLayout, QGroupBox, QSpinBox, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import math


class JointSlider(QWidget):
    """Single joint control widget with slider and display"""
    
    joint_moved = pyqtSignal(str, float)  # joint_name, radians
    
    def __init__(self, joint_name, min_pos=-180, max_pos=180, default_pos=0):
        super().__init__()
        self.joint_name = joint_name
        self.min_pos = min_pos
        self.max_pos = max_pos
        
        # Convert radians to degrees for display (if values look like radians)
        if abs(min_pos) > 10 or abs(max_pos) > 10:
            # Already in degrees
            self.min_degrees = int(min_pos)
            self.max_degrees = int(max_pos)
        else:
            # Convert from radians to degrees
            self.min_degrees = int(min_pos * 180 / math.pi)
            self.max_degrees = int(max_pos * 180 / math.pi)
        
        self.init_ui(default_pos)
    
    def init_ui(self, default_pos):
        """Initialize UI for single joint"""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 5, 0, 5)
        
        # Joint name label
        name_label = QLabel(self.joint_name)
        name_label.setMinimumWidth(120)
        name_font = QFont()
        name_font.setBold(True)
        name_label.setFont(name_font)
        layout.addWidget(name_label)
        
        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(self.min_degrees)
        self.slider.setMaximum(self.max_degrees)
        self.slider.setValue(int(default_pos))
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(30)
        self.slider.sliderMoved.connect(self.on_slider_moved)
        layout.addWidget(self.slider, 1)
        
        # Position display (degrees)
        self.pos_label = QLabel(f"{int(default_pos)}°")
        self.pos_label.setMinimumWidth(50)
        self.pos_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pos_font = QFont()
        pos_font.setPointSize(10)
        pos_font.setBold(True)
        self.pos_label.setFont(pos_font)
        layout.addWidget(self.pos_label)
        
        self.setLayout(layout)
    
    def on_slider_moved(self, value):
        """Handle slider movement"""
        # Convert degrees to radians
        radians = (value * math.pi) / 180.0
        
        # Update label
        self.pos_label.setText(f"{value}°")
        
        # Emit signal
        self.joint_moved.emit(self.joint_name, radians)
    
    def set_position(self, radians):
        """Update slider from external source (from robot feedback)"""
        degrees = int((radians * 180) / math.pi)
        self.slider.blockSignals(True)
        self.slider.setValue(degrees)
        self.pos_label.setText(f"{degrees}°")
        self.slider.blockSignals(False)
    
    def get_position(self):
        """Get current position in radians"""
        degrees = self.slider.value()
        return (degrees * math.pi) / 180.0


class ControlPanel(QWidget):
    """
    Professional robot joint control interface
    Provides sliders for all robot joints with real-time feedback
    """
    
    mode_changed = pyqtSignal(str)
    
    def __init__(self, robot_controller, state_manager, config=None):
        super().__init__()
        self.robot_controller = robot_controller
        self.state_manager = state_manager
        self.config = config or {}
        
        # Joint sliders (will be created in init_ui)
        self.joint_sliders = {}
        
        # Saved positions
        self.saved_positions = {}
        
        self.init_ui()
        
        # Register for state updates
        if self.state_manager:
            self.state_manager.register_callback(self.on_state_update)
    
    def init_ui(self):
        """Initialize control panel UI"""
        main_layout = QVBoxLayout()
        
        # ===== HEADER =====
        header = QLabel("Joint Control Panel")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("color: #0066cc; margin-bottom: 10px;")
        main_layout.addWidget(header)
        
        # ===== MODE SELECTOR =====
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Control Mode:"))
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["IDLE", "MANUAL", "SEMI_AUTO"])
        self.mode_combo.setCurrentText("MANUAL")
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_combo)
        
        mode_layout.addStretch()
        main_layout.addLayout(mode_layout)
        
        # ===== JOINT SLIDERS GROUP =====
        joints_box = QGroupBox("Joint Positions")
        joints_layout = QVBoxLayout()
        
        # Get joints from config or use defaults
        joints_config = self.config.get("robot", {}).get("joints", [])
        
        if joints_config:
            # Use configured joints
            for joint_cfg in joints_config:
                joint_name = joint_cfg.get("name", "unknown")
                min_pos = joint_cfg.get("min_position", -180)
                max_pos = joint_cfg.get("max_position", 180)
                
                slider = JointSlider(joint_name, min_pos, max_pos, 0)
                slider.joint_moved.connect(self.on_joint_moved)
                self.joint_sliders[joint_name] = slider
                joints_layout.addWidget(slider)
        else:
            # Use default joints (humanoid robot)
            default_joints = [
                ("head_pan", -90, 90),
                ("head_tilt", -45, 45),
                ("r_shoulder_pan", -90, 90),
                ("r_shoulder_lift", -90, 90),
                ("r_elbow", -120, 120),
                ("r_wrist_1", -90, 90),
                ("r_wrist_2", -180, 180),
            ]
            
            for joint_name, min_deg, max_deg in default_joints:
                slider = JointSlider(joint_name, min_deg, max_deg, 0)
                slider.joint_moved.connect(self.on_joint_moved)
                self.joint_sliders[joint_name] = slider
                joints_layout.addWidget(slider)
        
        joints_box.setLayout(joints_layout)
        main_layout.addWidget(joints_box)
        
        # ===== CONTROL BUTTONS =====
        button_layout = QHBoxLayout()
        
        # Home button
        home_btn = QPushButton("Home")
        home_btn.setStyleSheet("""
            QPushButton {
                background-color: #0066cc;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
        """)
        home_btn.clicked.connect(self.on_home_clicked)
        button_layout.addWidget(home_btn)
        
        # Save position button
        save_btn = QPushButton("Save Position")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #00aa00;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #008800;
            }
        """)
        save_btn.clicked.connect(self.on_save_position_clicked)
        button_layout.addWidget(save_btn)
        
        # Load position button
        load_btn = QPushButton("Load Position")
        load_btn.setStyleSheet("""
            QPushButton {
                background-color: #aa6600;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #884400;
            }
        """)
        load_btn.clicked.connect(self.on_load_position_clicked)
        button_layout.addWidget(load_btn)
        
        # Teach mode button
        teach_btn = QPushButton("Teach Mode")
        teach_btn.setStyleSheet("""
            QPushButton {
                background-color: #6600aa;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #550088;
            }
        """)
        teach_btn.clicked.connect(self.on_teach_mode_clicked)
        button_layout.addWidget(teach_btn)
        
        main_layout.addLayout(button_layout)
        
        # ===== STATUS DISPLAY =====
        status_box = QGroupBox("Current Status")
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("Ready | All joints at home position")
        self.status_label.setStyleSheet("color: #00aa00; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        
        status_box.setLayout(status_layout)
        main_layout.addWidget(status_box)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def on_joint_moved(self, joint_name, radians):
        """Handle joint slider movement"""
        try:
            # Send command to robot controller
            self.robot_controller.move_joint(joint_name, radians)
            
            # Update status
            degrees = int((radians * 180) / math.pi)
            self.status_label.setText(f"Moving {joint_name} to {degrees}°")
            self.status_label.setStyleSheet("color: #0066cc; font-weight: bold;")
        
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            self.status_label.setStyleSheet("color: #cc0000; font-weight: bold;")
    
    def on_state_update(self, state):
        """Handle robot state updates from StateManager"""
        # Update sliders with actual robot feedback
        for joint_name, joint_state in state.joints.items():
            if joint_name in self.joint_sliders:
                self.joint_sliders[joint_name].set_position(joint_state.position)
    
    def on_mode_changed(self, mode):
        """Handle control mode change"""
        self.robot_controller.set_mode(mode)
        self.status_label.setText(f"Mode changed to {mode}")
        self.status_label.setStyleSheet("color: #0066cc; font-weight: bold;")
    
    def on_home_clicked(self):
        """Move all joints to home position (0 degrees)"""
        for joint_name, slider in self.joint_sliders.items():
            slider.set_position(0.0)
            self.robot_controller.move_joint(joint_name, 0.0)
        
        self.status_label.setText("All joints moved to home position")
        self.status_label.setStyleSheet("color: #00aa00; font-weight: bold;")
    
    def on_save_position_clicked(self):
        """Save current position to memory"""
        position_data = {}
        for joint_name, slider in self.joint_sliders.items():
            position_data[joint_name] = slider.get_position()
        
        # Save with timestamp
        import time
        key = f"saved_{int(time.time())}"
        self.saved_positions[key] = position_data
        
        self.status_label.setText(f"Position saved as '{key}'")
        self.status_label.setStyleSheet("color: #00aa00; font-weight: bold;")
    
    def on_load_position_clicked(self):
        """Load last saved position"""
        if not self.saved_positions:
            self.status_label.setText("No saved positions available")
            self.status_label.setStyleSheet("color: #cc0000; font-weight: bold;")
            return
        
        # Load most recent position
        latest_key = sorted(self.saved_positions.keys())[-1]
        position_data = self.saved_positions[latest_key]
        
        # Apply position to all joints
        for joint_name, radians in position_data.items():
            if joint_name in self.joint_sliders:
                self.joint_sliders[joint_name].set_position(radians)
                self.robot_controller.move_joint(joint_name, radians)
        
        self.status_label.setText(f"Position loaded from '{latest_key}'")
        self.status_label.setStyleSheet("color: #00aa00; font-weight: bold;")
    
    def on_teach_mode_clicked(self):
        """Enter teach mode (allows manual positioning)"""
        mode = "MANUAL" if self.mode_combo.currentText() != "MANUAL" else "IDLE"
        self.mode_combo.setCurrentText(mode)
        
        self.status_label.setText(f"Teach mode: {mode}")
        self.status_label.setStyleSheet("color: #6600aa; font-weight: bold;")
    
    def get_all_joint_positions(self):
        """Get current positions of all joints"""
        positions = {}
        for joint_name, slider in self.joint_sliders.items():
            positions[joint_name] = slider.get_position()
        return positions
    
    def set_all_joint_positions(self, positions):
        """Set all joint positions from external source"""
        for joint_name, radians in positions.items():
            if joint_name in self.joint_sliders:
                self.joint_sliders[joint_name].set_position(radians)


if __name__ == "__main__":
    # Simple test
    import sys
    from PyQt6.QtWidgets import QApplication
    from axel_core import StateManager, RobotController, SafetyManager
    
    app = QApplication(sys.argv)
    
    # Create core modules
    state_manager = StateManager()
    safety_manager = SafetyManager()
    robot_controller = RobotController(state_manager, safety_manager)
    
    # Create and show control panel
    panel = ControlPanel(robot_controller, state_manager)
    panel.setGeometry(100, 100, 800, 600)
    panel.setWindowTitle("AXEL Control Panel")
    panel.show()
    
    sys.exit(app.exec())
