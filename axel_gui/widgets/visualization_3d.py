"""
3D Visualization Panel - Real-time Robot Visualization
Shows 3D representation of robot with joint positions
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D


class RobotVisualizer3D:
    """3D representation of AXEL humanoid robot (InMoov 2 clone with 20 joints)"""
    
    def __init__(self):
        """Initialize robot model"""
        # Base link at origin
        self.base_position = np.array([0, 0, 0])
        
        # Robot dimensions (AXEL/InMoov 2 humanoid)
        self.link_lengths = {
            'torso': 0.35,           # Torso height
            'neck': 0.05,            # Neck length
            'head': 0.15,            # Head height
            'shoulder_offset': 0.12, # Shoulder width from center
            'shoulder_to_elbow': 0.25,  # Upper arm length
            'elbow_to_wrist': 0.25,     # Forearm length
            'wrist_to_hand': 0.08,      # Hand length
            'finger_length': 0.05,      # Individual finger length
        }
        
        # Current joint angles (radians) - All 20 joints
        self.joint_angles = {
            # Head (2 DOF)
            'head_pan': 0.0,
            'head_tilt': 0.0,
            # Right Arm (4 DOF)
            'r_shoulder_pan': 0.0,
            'r_shoulder_lift': 0.0,
            'r_elbow': 0.0,
            'r_wrist': 0.0,
            # Right Hand (5 DOF - fingers)
            'r_thumb': 0.0,
            'r_index': 0.0,
            'r_middle': 0.0,
            'r_ring': 0.0,
            'r_pinky': 0.0,
            # Left Arm (4 DOF)
            'l_shoulder_pan': 0.0,
            'l_shoulder_lift': 0.0,
            'l_elbow': 0.0,
            'l_wrist': 0.0,
            # Left Hand (5 DOF - fingers)
            'l_thumb': 0.0,
            'l_index': 0.0,
            'l_middle': 0.0,
            'l_ring': 0.0,
            'l_pinky': 0.0,
        }
        
        # Link positions (updated by forward kinematics)
        self.link_positions = {}
        self.joint_colors = {}
    
    def update_joint_angles(self, joint_angles):
        """Update joint angles and compute positions"""
        self.joint_angles.update(joint_angles)
        self.compute_forward_kinematics()
    
    def compute_forward_kinematics(self):
        """Compute 3D positions of all 20 robot joints (AXEL humanoid)"""
        positions = {}
        
        # Base/torso at origin
        positions['base'] = self.base_position
        positions['torso'] = self.base_position + np.array([0, 0, self.link_lengths['torso']])
        
        # === HEAD (2 DOF) ===
        head_base = positions['torso'] + np.array([0, 0, self.link_lengths['neck']])
        head_pan = self.joint_angles.get('head_pan', 0)
        head_tilt = self.joint_angles.get('head_tilt', 0)
        
        head_offset = np.array([
            np.sin(head_pan) * 0.03,
            np.cos(head_pan) * 0.03,
            self.link_lengths['head']
        ])
        positions['head'] = head_base + head_offset
        
        # === RIGHT ARM (9 DOF: 4 arm + 5 fingers) ===
        # Shoulder position
        r_shoulder_pos = positions['torso'] + np.array([self.link_lengths['shoulder_offset'], 0, 0.1])
        positions['r_shoulder'] = r_shoulder_pos
        
        # Right shoulder pan and lift
        r_shoulder_pan = self.joint_angles.get('r_shoulder_pan', 0)
        r_shoulder_lift = self.joint_angles.get('r_shoulder_lift', 0)
        
        r_elbow_offset = np.array([
            np.sin(r_shoulder_pan) * self.link_lengths['shoulder_to_elbow'],
            np.cos(r_shoulder_pan) * self.link_lengths['shoulder_to_elbow'] * 0.7,
            -r_shoulder_lift * self.link_lengths['shoulder_to_elbow']
        ])
        r_elbow_pos = r_shoulder_pos + r_elbow_offset
        positions['r_elbow'] = r_elbow_pos
        
        # Right wrist
        r_elbow_angle = self.joint_angles.get('r_elbow', 0)
        r_wrist_offset = np.array([
            np.sin(r_shoulder_pan) * self.link_lengths['elbow_to_wrist'],
            np.cos(r_shoulder_pan) * self.link_lengths['elbow_to_wrist'] * 0.7,
            -r_elbow_angle * self.link_lengths['elbow_to_wrist']
        ])
        r_wrist_pos = r_elbow_pos + r_wrist_offset
        positions['r_wrist'] = r_wrist_pos
        
        # Right hand (palm)
        r_hand_offset = np.array([
            np.sin(r_shoulder_pan) * self.link_lengths['wrist_to_hand'],
            np.cos(r_shoulder_pan) * self.link_lengths['wrist_to_hand'] * 0.7,
            -0.02
        ])
        r_hand_pos = r_wrist_pos + r_hand_offset
        positions['r_hand'] = r_hand_pos
        
        # Right fingers (5 DOF)
        finger_names_r = ['r_thumb', 'r_index', 'r_middle', 'r_ring', 'r_pinky']
        finger_offsets = [
            np.array([-0.015, 0.015, 0]),      # Thumb
            np.array([-0.007, 0.02, 0.005]),   # Index
            np.array([0, 0.02, 0.008]),        # Middle
            np.array([0.007, 0.02, 0.005]),    # Ring
            np.array([0.015, 0.015, 0]),       # Pinky
        ]
        
        for i, finger_name in enumerate(finger_names_r):
            finger_angle = self.joint_angles.get(finger_name, 0)
            finger_pos = r_hand_pos + finger_offsets[i]
            finger_pos[2] -= finger_angle * self.link_lengths['finger_length'] * 0.3
            positions[finger_name] = finger_pos
        
        # === LEFT ARM (9 DOF: 4 arm + 5 fingers) ===
        # Shoulder position (mirrored)
        l_shoulder_pos = positions['torso'] + np.array([-self.link_lengths['shoulder_offset'], 0, 0.1])
        positions['l_shoulder'] = l_shoulder_pos
        
        # Left shoulder pan and lift
        l_shoulder_pan = self.joint_angles.get('l_shoulder_pan', 0)
        l_shoulder_lift = self.joint_angles.get('l_shoulder_lift', 0)
        
        l_elbow_offset = np.array([
            -np.sin(l_shoulder_pan) * self.link_lengths['shoulder_to_elbow'],
            np.cos(l_shoulder_pan) * self.link_lengths['shoulder_to_elbow'] * 0.7,
            -l_shoulder_lift * self.link_lengths['shoulder_to_elbow']
        ])
        l_elbow_pos = l_shoulder_pos + l_elbow_offset
        positions['l_elbow'] = l_elbow_pos
        
        # Left wrist
        l_elbow_angle = self.joint_angles.get('l_elbow', 0)
        l_wrist_offset = np.array([
            -np.sin(l_shoulder_pan) * self.link_lengths['elbow_to_wrist'],
            np.cos(l_shoulder_pan) * self.link_lengths['elbow_to_wrist'] * 0.7,
            -l_elbow_angle * self.link_lengths['elbow_to_wrist']
        ])
        l_wrist_pos = l_elbow_pos + l_wrist_offset
        positions['l_wrist'] = l_wrist_pos
        
        # Left hand (palm)
        l_hand_offset = np.array([
            -np.sin(l_shoulder_pan) * self.link_lengths['wrist_to_hand'],
            np.cos(l_shoulder_pan) * self.link_lengths['wrist_to_hand'] * 0.7,
            -0.02
        ])
        l_hand_pos = l_wrist_pos + l_hand_offset
        positions['l_hand'] = l_hand_pos
        
        # Left fingers (5 DOF)
        finger_names_l = ['l_thumb', 'l_index', 'l_middle', 'l_ring', 'l_pinky']
        finger_offsets_l = [
            np.array([0.015, 0.015, 0]),       # Thumb (mirrored)
            np.array([0.007, 0.02, 0.005]),    # Index
            np.array([0, 0.02, 0.008]),        # Middle
            np.array([-0.007, 0.02, 0.005]),   # Ring
            np.array([-0.015, 0.015, 0]),      # Pinky
        ]
        
        for i, finger_name in enumerate(finger_names_l):
            finger_angle = self.joint_angles.get(finger_name, 0)
            finger_pos = l_hand_pos + finger_offsets_l[i]
            finger_pos[2] -= finger_angle * self.link_lengths['finger_length'] * 0.3
            positions[finger_name] = finger_pos
        
        self.link_positions = positions
    
    def get_links(self):
        """Get list of robot links for visualization - All 20 joints (AXEL humanoid)"""
        links = [
            # Torso and head
            ('base', 'torso'),
            ('torso', 'head'),
            
            # Right arm chain (shoulder -> elbow -> wrist -> hand)
            ('torso', 'r_shoulder'),
            ('r_shoulder', 'r_elbow'),
            ('r_elbow', 'r_wrist'),
            ('r_wrist', 'r_hand'),
            
            # Right hand fingers
            ('r_hand', 'r_thumb'),
            ('r_hand', 'r_index'),
            ('r_hand', 'r_middle'),
            ('r_hand', 'r_ring'),
            ('r_hand', 'r_pinky'),
            
            # Left arm chain (shoulder -> elbow -> wrist -> hand)
            ('torso', 'l_shoulder'),
            ('l_shoulder', 'l_elbow'),
            ('l_elbow', 'l_wrist'),
            ('l_wrist', 'l_hand'),
            
            # Left hand fingers
            ('l_hand', 'l_thumb'),
            ('l_hand', 'l_index'),
            ('l_hand', 'l_middle'),
            ('l_hand', 'l_ring'),
            ('l_hand', 'l_pinky'),
        ]
        return links
    
    def get_link_position(self, link_name):
        """Get 3D position of a link"""
        return self.link_positions.get(link_name, np.array([0, 0, 0]))


class Visualization3DPanel(QWidget):
    """3D visualization of robot with matplotlib"""
    
    def __init__(self, state_manager, config=None):
        super().__init__()
        self.state_manager = state_manager
        self.config = config or {}
        
        # Create robot visualizer
        self.robot = RobotVisualizer3D()
        
        # Create matplotlib figure for 3D plot
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111, projection='3d')
        
        # Create canvas
        self.canvas = FigureCanvas(self.figure)
        
        self.init_ui()
        
        # Register for state updates
        if self.state_manager:
            self.state_manager.register_callback(self.on_state_update)
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("3D Robot Visualization")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("color: #0066cc; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Description
        desc = QLabel("Real-time 3D view of robot position")
        desc.setStyleSheet("color: #666666; font-size: 10px; margin-bottom: 10px;")
        layout.addWidget(desc)
        
        # Canvas
        layout.addWidget(self.canvas)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        reset_view_btn = QPushButton("Reset View")
        reset_view_btn.setStyleSheet("""
            QPushButton {
                background-color: #0066cc;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
        """)
        reset_view_btn.clicked.connect(self.reset_view)
        button_layout.addWidget(reset_view_btn)
        
        rotate_btn = QPushButton("Rotate View")
        rotate_btn.setStyleSheet("""
            QPushButton {
                background-color: #aa6600;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #884400;
            }
        """)
        rotate_btn.clicked.connect(self.rotate_view)
        button_layout.addWidget(rotate_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Draw initial visualization
        self.draw_robot()
    
    def on_state_update(self, state):
        """Update visualization with new robot state"""
        # Extract joint angles from state
        joint_angles = {}
        for joint_name, joint_state in state.joints.items():
            joint_angles[joint_name] = joint_state.position
        
        # Update robot model
        self.robot.update_joint_angles(joint_angles)
        
        # Redraw
        self.draw_robot()
    
    def draw_robot(self):
        """Draw 3D robot visualization - Full AXEL humanoid with 20 joints"""
        self.ax.clear()
        
        # Set up axes
        self.ax.set_xlabel('X (m)', fontsize=9, labelpad=8)
        self.ax.set_ylabel('Y (m)', fontsize=9, labelpad=8)
        self.ax.set_zlabel('Z (m)', fontsize=9, labelpad=8)
        
        # Set equal aspect ratio - Show full humanoid (170cm tall)
        self.ax.set_xlim([-0.6, 0.6])
        self.ax.set_ylim([-0.6, 0.6])
        self.ax.set_zlim([0, 1.2])
        
        # Draw ground plane
        xx, yy = np.meshgrid(np.linspace(-0.6, 0.6, 15),
                             np.linspace(-0.6, 0.6, 15))
        zz = np.zeros_like(xx)
        self.ax.plot_surface(xx, yy, zz, alpha=0.05, color='gray')
        
        # Color scheme for different body parts
        link_colors = {
            # Head
            'head': '#FFB6C1',  # Light pink
            # Right arm
            'r_shoulder': '#FF6B6B',  # Red
            'r_elbow': '#FF8C42',     # Orange
            'r_wrist': '#FFA500',     # Orange-yellow
            'r_hand': '#FFD700',      # Gold
            'r_thumb': '#87CEEB',     # Sky blue
            'r_index': '#87CEEB',
            'r_middle': '#87CEEB',
            'r_ring': '#87CEEB',
            'r_pinky': '#87CEEB',
            # Left arm
            'l_shoulder': '#4169E1',   # Royal blue
            'l_elbow': '#1E90FF',      # Dodger blue
            'l_wrist': '#00BFFF',      # Deep sky blue
            'l_hand': '#00CED1',       # Dark turquoise
            'l_thumb': '#90EE90',      # Light green
            'l_index': '#90EE90',
            'l_middle': '#90EE90',
            'l_ring': '#90EE90',
            'l_pinky': '#90EE90',
        }
        
        # Draw links (skeleton)
        links = self.robot.get_links()
        for link_start, link_end in links:
            start_pos = self.robot.get_link_position(link_start)
            end_pos = self.robot.get_link_position(link_end)
            
            # Determine link color
            link_color = link_colors.get(link_end, '#888888')
            
            # Draw line
            xs = [start_pos[0], end_pos[0]]
            ys = [start_pos[1], end_pos[1]]
            zs = [start_pos[2], end_pos[2]]
            
            self.ax.plot(xs, ys, zs, color=link_color, linewidth=4, alpha=0.8)
        
        # Draw joints as spheres (colored by body part)
        for link_name, pos in self.robot.link_positions.items():
            if link_name == 'base':
                # Base (pelvis) - large green sphere
                self.ax.scatter([pos[0]], [pos[1]], [pos[2]], 
                              c='#228B22', s=300, alpha=0.9, edgecolors='darkgreen', linewidth=2)
            elif link_name == 'torso':
                # Torso - cyan
                self.ax.scatter([pos[0]], [pos[1]], [pos[2]], 
                              c='#00CED1', s=250, alpha=0.8, edgecolors='darkturquoise', linewidth=1)
            elif link_name in link_colors:
                color = link_colors[link_name]
                size = 80 if 'finger' in link_name else 120
                self.ax.scatter([pos[0]], [pos[1]], [pos[2]], 
                              c=color, s=size, alpha=0.8, edgecolors='darkgray', linewidth=0.5)
        
        # Add title and info
        self.ax.set_title('AXEL Humanoid Robot - 20 Joint Configuration\n(InMoov 2 Clone)', 
                         fontsize=11, fontweight='bold', pad=10)
        
        # Set viewing angle
        self.ax.view_init(elev=20, azim=45)
        
        # Adjust layout
        self.figure.tight_layout()
        
        # Redraw canvas
        self.canvas.draw()
    
    def reset_view(self):
        """Reset viewing angle"""
        self.ax.view_init(elev=20, azim=45)
        self.canvas.draw()
    
    def rotate_view(self):
        """Rotate viewing angle"""
        current_azim = self.ax.azim if hasattr(self.ax, 'azim') else 45
        new_azim = (current_azim + 45) % 360
        self.ax.view_init(elev=20, azim=new_azim)
        self.canvas.draw()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    from axel_core import StateManager
    
    app = QApplication(sys.argv)
    
    # Create state manager
    state_manager = StateManager()
    
    # Create and show visualization
    viz = Visualization3DPanel(state_manager)
    viz.setGeometry(100, 100, 900, 700)
    viz.setWindowTitle("AXEL 3D Visualization")
    viz.show()
    
    sys.exit(app.exec())
