# 🚀 QUICK ACTION PLAN - Build NED2-Style AXEL Software

## This Week: Priority Tasks

### PRIORITY 1: Control Panel (Start TODAY)
**Goal**: Users can move each joint with sliders

```python
# File: axel_gui/widgets/control_panel.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSlider, 
                             QLabel, QPushButton, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal

class ControlPanel(QWidget):
    command_sent = pyqtSignal(str, float)  # Signal: joint_name, position
    
    def __init__(self, robot_controller, state_manager):
        super().__init__()
        self.robot_controller = robot_controller
        self.state_manager = state_manager
        self.sliders = {}
        self.labels = {}
        
        self.init_ui()
        self.state_manager.register_callback(self.update_display)
    
    def init_ui(self):
        layout = QGridLayout()
        
        # Create sliders for each joint (example)
        joints = ["head_pan", "head_tilt", "r_shoulder_pan", "r_elbow"]
        
        row = 0
        for joint in joints:
            # Label
            label = QLabel(joint)
            layout.addWidget(label, row, 0)
            
            # Slider (-180 to +180 degrees)
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(-180, 180)
            slider.setValue(0)
            slider.sliderMoved.connect(lambda v, j=joint: self.on_slider_move(j, v))
            self.sliders[joint] = slider
            layout.addWidget(slider, row, 1)
            
            # Position display
            pos_label = QLabel("0°")
            self.labels[joint] = pos_label
            layout.addWidget(pos_label, row, 2)
            
            row += 1
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(QPushButton("Save Position"))
        button_layout.addWidget(QPushButton("Load Position"))
        button_layout.addWidget(QPushButton("Home"))
        layout.addLayout(button_layout, row, 0, 1, 3)
        
        self.setLayout(layout)
    
    def on_slider_move(self, joint_name, value):
        # Convert degrees to radians
        radians = (value * 3.14159) / 180.0
        
        # Send command to robot
        self.robot_controller.move_joint(joint_name, radians)
        
        # Update label
        self.labels[joint_name].setText(f"{value}°")
    
    def update_display(self, state):
        # Update slider positions when state changes (from robot feedback)
        for joint_name, joint_state in state.joints.items():
            if joint_name in self.sliders:
                # Convert radians back to degrees
                degrees = int((joint_state.position * 180.0) / 3.14159)
                self.sliders[joint_name].blockSignals(True)
                self.sliders[joint_name].setValue(degrees)
                self.sliders[joint_name].blockSignals(False)
                self.labels[joint_name].setText(f"{degrees}°")
```

**Time to implement**: 1-2 hours

---

### PRIORITY 2: Monitoring Panel
**Goal**: Display real-time robot status

```python
# File: axel_gui/widgets/monitoring_panel.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QProgressBar, QLabel)
from PyQt6.QtCore import Qt

class MonitoringPanel(QWidget):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        self.init_ui()
        self.state_manager.register_callback(self.update_status)
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Joint states table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Joint", "Position", "Velocity", "Effort"])
        layout.addWidget(self.table)
        
        # Battery status
        battery_layout = QVBoxLayout()
        battery_label = QLabel("Battery:")
        self.battery_bar = QProgressBar()
        battery_layout.addWidget(battery_label)
        battery_layout.addWidget(self.battery_bar)
        layout.addLayout(battery_layout)
        
        # Temperature
        temp_layout = QVBoxLayout()
        temp_label = QLabel("Temperature:")
        self.temp_label = QLabel("0°C")
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(self.temp_label)
        layout.addLayout(temp_layout)
        
        self.setLayout(layout)
    
    def update_status(self, state):
        # Update table with joint states
        self.table.setRowCount(len(state.joints))
        
        for i, (joint_name, joint) in enumerate(state.joints.items()):
            self.table.setItem(i, 0, QTableWidgetItem(joint_name))
            self.table.setItem(i, 1, QTableWidgetItem(f"{joint.position:.2f}"))
            self.table.setItem(i, 2, QTableWidgetItem(f"{joint.velocity:.2f}"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{joint.effort:.2f}"))
        
        # Update battery
        self.battery_bar.setValue(int(state.battery_level))
        
        # Update temperature
        self.temp_label.setText(f"{state.cpu_temp:.1f}°C")
```

**Time to implement**: 1-2 hours

---

### PRIORITY 3: Safety Panel
**Goal**: E-STOP button and status display

```python
# File: axel_gui/widgets/safety_panel.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

class SafetyPanel(QWidget):
    def __init__(self, robot_controller, safety_manager, state_manager):
        super().__init__()
        self.robot_controller = robot_controller
        self.safety_manager = safety_manager
        self.state_manager = state_manager
        self.init_ui()
        self.state_manager.register_callback(self.update_status)
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # E-STOP Button (BIG and RED)
        self.estop_btn = QPushButton("🔴 EMERGENCY STOP")
        self.estop_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-size: 24px;
                padding: 20px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.estop_btn.clicked.connect(self.on_estop)
        layout.addWidget(self.estop_btn)
        
        # Status label
        self.status_label = QLabel("E-STOP: ARMED ✓")
        font = self.status_label.font()
        font.setPointSize(16)
        font.setBold(True)
        self.status_label.setFont(font)
        self.status_label.setStyleSheet("color: green;")
        layout.addWidget(self.status_label)
        
        # Joint limits info
        limits_label = QLabel("All joints within limits ✓")
        limits_label.setStyleSheet("color: green;")
        layout.addWidget(limits_label)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def on_estop(self):
        self.robot_controller.emergency_stop()
        self.estop_btn.setEnabled(False)
        self.estop_btn.setText("🔴 E-STOP ACTIVATED")
    
    def update_status(self, state):
        if state.emergency_stop:
            self.status_label.setText("⚠ E-STOP ACTIVE ⚠")
            self.status_label.setStyleSheet("color: red;")
        else:
            self.status_label.setText("E-STOP: ARMED ✓")
            self.status_label.setStyleSheet("color: green;")
```

**Time to implement**: 1 hour

---

### PRIORITY 4: Update Main Window
**Goal**: Add the new widgets as tabs

```python
# Update: axel_gui/main_window.py

# In setup_ui() method, replace placeholder code:

from axel_gui.widgets.control_panel import ControlPanel
from axel_gui.widgets.monitoring_panel import MonitoringPanel
from axel_gui.widgets.safety_panel import SafetyPanel

# Create real widgets
control_widget = ControlPanel(self.robot_controller, self.state_manager)
monitoring_widget = MonitoringPanel(self.state_manager)
safety_widget = SafetyPanel(self.robot_controller, self.safety_manager, 
                            self.state_manager)

# Add to tabs
tabs.addTab(monitoring_widget, "Monitoring")
tabs.addTab(control_widget, "Control")
tabs.addTab(safety_widget, "Safety")
```

---

## 📋 Week 2-3 Checklist

- [ ] **Day 1**: Control Panel
  - [ ] Create control_panel.py
  - [ ] Implement joint sliders
  - [ ] Test with state_manager
  
- [ ] **Day 2**: Monitoring Panel
  - [ ] Create monitoring_panel.py
  - [ ] Implement status display
  - [ ] Add battery/temperature display

- [ ] **Day 3**: Safety Panel
  - [ ] Create safety_panel.py
  - [ ] Implement E-STOP button
  - [ ] Update main_window.py to use all widgets

- [ ] **Day 4**: Testing & Styling
  - [ ] Test all widgets together
  - [ ] Add professional styling (colors, fonts)
  - [ ] Verify all callbacks work

- [ ] **Day 5**: Polish
  - [ ] Add icons to buttons
  - [ ] Improve layout
  - [ ] Write documentation

---

## 🎨 Professional Styling Tips

```python
# Add to main_window.py

STYLESHEET = """
    QMainWindow {
        background-color: #f0f0f0;
    }
    QPushButton {
        background-color: #0066cc;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #0052a3;
    }
    QSlider::groove:horizontal {
        border: 1px solid #999999;
        height: 8px;
        background: #cccccc;
        margin: 2px 0;
    }
    QSlider::handle:horizontal {
        background: #0066cc;
        border: 1px solid #5c5c5c;
        width: 18px;
        margin: -5px 0;
        border-radius: 9px;
    }
    QTableWidget {
        gridline-color: #d0d0d0;
        background-color: white;
    }
    QTableWidget::item {
        padding: 5px;
    }
"""

self.setStyleSheet(STYLESHEET)
```

---

## 🧪 Test Your Work

After each widget, test like this:

```python
# Run with test data
python axel_gui/main_window.py

# Then in Python console:
from axel_core import StateManager
state = StateManager()
state.update_joint_state("test", 1.5, 0.5)
state.update_battery_status(75)
# Verify display updates
```

---

## 🎯 After Week 3, You'll Have

✅ Professional control panel (like NED2)
✅ Real-time monitoring display
✅ Safety controls with E-STOP
✅ Beautiful GUI that looks professional
✅ Ready for simulation integration in Week 3-4

---

**START WITH CONTROL PANEL TODAY! It's the core of everything.** 💪

