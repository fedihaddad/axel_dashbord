# NED2 Software Analysis & AXEL Development Roadmap

## 📊 NED2 Software Architecture Analysis

### What NED2 Has (Professional Robot Software)

#### 1. **Multi-Layer Control**
- **NiryoStudio**: Block-based programming (Blockly) - Visual programming
- **Python API**: Direct control via Python SDK
- **ROS 2**: Full ROS 2 integration for advanced users
- **MATLAB**: Compatible for academic work

#### 2. **Hardware Integration**
- **Physical Control Panel** with buttons:
  - Custom programmable button
  - Save position button
  - FreeMotion button (manual control)
  - Gripper connectors
  - Electromagnet connectors
  - Digital/Analog I/O
  
#### 3. **Desktop Software (NiryoStudio)**
- **No-code/Low-code interface** (Blockly)
- **Real-time visualization** of robot state
- **Program editor** with drag-drop blocks
- **Execution monitoring** with live feedback
- **Gripper control** in the GUI
- **Position saving** for teach pendant functionality

#### 4. **Sensor Integration**
- IR sensors
- Digital inputs (3)
- Analog inputs (2)
- Vacuum pump interface
- Conveyor interface
- LED ring feedback (status indication)

#### 5. **Safety & Features**
- Emergency stop on control panel
- Joint limits enforced
- Collision detection
- Workspace boundaries
- Soft/hard motion modes

#### 6. **Ecosystem**
- **NiryoAcademy**: Educational content platform
- **RoboDK**: Simulation and offline programming
- **TensorFlow/OpenCV**: AI/ML integration
- **Extensive accessories**: Grippers, sensors, tools

---

## 🔄 AXEL vs NED2 Comparison

| Feature | NED2 | AXEL (Current) | AXEL (Target) |
|---------|------|---|---|
| **GUI Application** | ✅ Full-featured | 🔄 Framework | ✅ Full-featured |
| **Block Programming** | ✅ Blockly | ❌ None | ✅ Needed |
| **3D Visualization** | ✅ Real-time | ❌ Placeholder | ✅ RViz Integration |
| **Joint Control** | ✅ Sliders/Buttons | ❌ None | ✅ Sliders/Buttons |
| **Position Teaching** | ✅ Save/Load | ❌ None | ✅ Needed |
| **Gripper Control** | ✅ In GUI | ❌ None | ✅ Needed |
| **Emergency Stop** | ✅ Hardware + GUI | ✅ Logic only | ✅ Hardware ready |
| **Sensor Display** | ✅ Real-time | 🔄 Framework | ✅ Real-time |
| **Logging/Recording** | ✅ Built-in | 🔄 Framework | ✅ Full rosbag support |
| **Multi-mode Control** | ✅ Yes | 🔄 Framework | ✅ Manual/Semi/Auto |

---

## 🎯 AXEL Phase 2-4 Development Plan (NED2-Style)

### Phase 2: GUI Expansion (Weeks 2-3) - Make It Look Professional

#### Core GUI Widgets

1. **Main Dashboard**
   ```
   ┌─────────────────────────────────────────────────────┐
   │  AXEL Robot Control Station                          │
   ├─────────────────────────────────────────────────────┤
   │ [Monitoring] [Control] [Visualization] [Teach] [Safety] │
   ├─────────────────────────────────────────────────────┤
   │                                                     │
   │  STATUS: Ready | Battery: 87% | Temp: 45°C         │
   │  E-STOP: ARMED ✓ | Mode: MANUAL                    │
   │                                                     │
   └─────────────────────────────────────────────────────┘
   ```

2. **Control Panel Tab** (Most Important)
   ```
   ┌─── Manual Control ────────────────────────┐
   │                                           │
   │  Head:                                    │
   │  Pan:   [====●========] -90° ... 90°    │
   │  Tilt:  [===●=========] -45° ... 45°    │
   │                                           │
   │  Right Arm:                               │
   │  Shoulder: [=====●====] 0° ... 180°     │
   │  Elbow:    [====●=====] 0° ... 160°     │
   │                                           │
   │  [Save Position] [Load Position]         │
   │  [Teach Mode ON/OFF]                     │
   │                                           │
   │  Gripper:                                 │
   │  [Open] [Close] [Attach Tool]            │
   │                                           │
   └───────────────────────────────────────────┘
   ```

3. **Monitoring Panel Tab**
   ```
   ┌─── Real-Time Status ──────────────────────┐
   │                                           │
   │  Joint States:                            │
   │  ┌────────────────────────────────────┐ │
   │  │ head_pan:     45.2°  @0.5 rad/s   │ │
   │  │ head_tilt:   -15.0°  @0.2 rad/s   │ │
   │  │ r_shoulder:   90.0°  @0.8 rad/s   │ │
   │  │ ...                                 │ │
   │  └────────────────────────────────────┘ │
   │                                           │
   │  System Health:                           │
   │  Battery: 87% ████████░  (4.5h remain)  │
   │  CPU Temp: 45°C [Good]                   │
   │  Comm Latency: 12ms [Good]               │
   │                                           │
   └───────────────────────────────────────────┘
   ```

4. **3D Visualization Tab**
   ```
   ┌─── Robot Visualization ───────────────────┐
   │                                           │
   │        (RViz embedded)                    │
   │   ╱\  Robot model with                    │
   │  ╱  ╲ real-time joint updates             │
   │ ╱    ╲ and trajectory overlay             │
   │        ╲                                  │
   │                                           │
   │  [+] Zoom  [-] Pan  [↻] Reset View       │
   │                                           │
   └───────────────────────────────────────────┘
   ```

5. **Teach & Playback Tab**
   ```
   ┌─── Position Management ───────────────────┐
   │                                           │
   │  Saved Positions:                         │
   │  ┌─────────────────────────────────────┐ │
   │  │ Home Position          [Load] [Del]  │ │
   │  │ Pickup Position        [Load] [Del]  │ │
   │  │ Place Position         [Load] [Del]  │ │
   │  │ Standby Position       [Load] [Del]  │ │
   │  └─────────────────────────────────────┘ │
   │                                           │
   │  [Save Current] [Record Sequence]         │
   │  [Play Sequence] [Stop]                   │
   │                                           │
   │  Current Position: [x, y, z, rx, ry, rz]│
   │                                           │
   └───────────────────────────────────────────┘
   ```

6. **Safety Panel Tab**
   ```
   ┌─── Safety Control ────────────────────────┐
   │                                           │
   │  Emergency Stop: [🔴 ACTIVATE]            │
   │  Status: ARMED ✓                          │
   │                                           │
   │  Joint Limits:                            │
   │  Head Pan:      -90° ... 90°   [✓OK]     │
   │  Shoulder Pan:  -160° ... 160° [✓OK]     │
   │  Elbow:         -160° ... 160° [✓OK]     │
   │                                           │
   │  Motion Constraints:                      │
   │  Max Velocity: 1.0 rad/s [OK]             │
   │  Max Effort: 15 Nm [OK]                   │
   │                                           │
   │  [Reset] [Shutdown] [Self-test]           │
   │                                           │
   └───────────────────────────────────────────┘
   ```

### Phase 2 Implementation Details

**New GUI Files to Create:**
- `axel_gui/widgets/control_panel.py` - Joint sliders + gripper
- `axel_gui/widgets/monitoring_panel.py` - Real-time status display
- `axel_gui/widgets/visualization_3d.py` - RViz integration
- `axel_gui/widgets/teach_panel.py` - Position saving/loading
- `axel_gui/widgets/safety_panel.py` - E-STOP and limits
- `axel_gui/styles/stylesheet.qss` - Professional styling

**New Core Features:**
- Position teaching (save/load)
- Trajectory recording
- Real-time state display
- Gripper control interface
- Performance metrics

---

### Phase 3: Simulation Integration (Weeks 3-4)

#### What to Build

1. **URDF Model** (axel.urdf)
   ```xml
   <robot name="axel">
     <!-- Base link -->
     <link name="base_link">
       <inertial>...</inertial>
       <visual>...</visual>
     </link>
     
     <!-- Head -->
     <link name="head_link">...</link>
     <joint name="head_pan" type="revolute">
       <parent link="base_link"/>
       <child link="head_link"/>
       <limit lower="-1.57" upper="1.57" effort="5" velocity="1.0"/>
     </joint>
     
     <!-- Arms (symmetric) -->
     <link name="r_shoulder_link">...</link>
     <joint name="r_shoulder_pan" type="revolute">...</joint>
     ...
     
     <!-- Gripper -->
     <link name="gripper_base_link">...</link>
     <joint name="gripper_joint" type="prismatic">...</joint>
   </robot>
   ```

2. **Gazebo World File** (axel.world)
   - Physics engine configuration
   - Lighting setup
   - Ground plane
   - Optional objects for pick-and-place tasks

3. **Launch Files** (axel_launch.py)
   ```python
   # Launch Gazebo with AXEL model
   # Launch RViz with visualization
   # Launch joint state publisher
   # Launch controllers
   ```

4. **RViz Configuration** (default.rviz)
   - Robot model visualization
   - Joint state display
   - TF frame visualization
   - Trajectory playback

---

### Phase 4: Advanced Features (Weeks 4-5)

#### 1. Block Programming (Optional but Cool)
- Create visual programming interface
- Drag-drop blocks for:
  - Move joint
  - Open/close gripper
  - Wait for time
  - Loop
  - Conditional

#### 2. AI Integration
- Object detection (camera)
- Pose estimation
- Task learning

#### 3. Performance Analytics
- Record execution times
- Latency analysis
- Energy consumption tracking
- Efficiency metrics

---

## 📝 Detailed Implementation Steps

### Week 2-3: Build GUI Widgets

**Step 1: Create Control Panel (Highest Priority)**
```python
# axel_gui/widgets/control_panel.py
class ControlPanel(QWidget):
    def __init__(self, robot_controller, state_manager):
        # Create sliders for each joint
        # Add buttons for gripper control
        # Add teach position buttons
        # Real-time position feedback
        pass
```

**Step 2: Create Monitoring Panel**
```python
# axel_gui/widgets/monitoring_panel.py
class MonitoringPanel(QWidget):
    def __init__(self, state_manager):
        # Display joint states in table
        # Show battery level (progress bar)
        # Show temperature (gauge)
        # Update every 100ms from state_manager callbacks
        pass
```

**Step 3: Create Teach Panel**
```python
# axel_gui/widgets/teach_panel.py
class TeachPanel(QWidget):
    def save_position(self, name):
        # Get current position from state_manager
        # Save to JSON file or database
        pass
    
    def load_position(self, name):
        # Load position from storage
        # Send command via robot_controller
        pass
```

**Step 4: Create Safety Panel**
```python
# axel_gui/widgets/safety_panel.py
class SafetyPanel(QWidget):
    def emergency_stop(self):
        # Call robot_controller.emergency_stop()
        # Disable all controls
        # Show red warning
        pass
```

**Step 5: Create 3D Visualization**
```python
# axel_gui/widgets/visualization_3d.py
class Visualization3D(QWidget):
    def __init__(self, state_manager):
        # Embed RViz or matplotlib 3D view
        # Update robot visualization based on state_manager
        # Show joint frames and end-effector
        pass
```

---

## 🏗️ New Directory Structure (After Phase 2-3)

```
axel_robot_software/
├── axel_core/
│   ├── state_manager.py      (already done)
│   ├── robot_controller.py   (already done)
│   └── safety_manager.py     (already done)
│
├── axel_gui/
│   ├── main_window.py        (update to use new widgets)
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── control_panel.py          ← BUILD THIS
│   │   ├── monitoring_panel.py       ← BUILD THIS
│   │   ├── visualization_3d.py       ← BUILD THIS
│   │   ├── teach_panel.py            ← BUILD THIS
│   │   └── safety_panel.py           ← BUILD THIS
│   ├── styles/
│   │   ├── stylesheet.qss
│   │   └── theme.py
│   └── resources/
│       └── icons/
│
├── axel_simulation/
│   ├── urdf/
│   │   └── axel.urdf                 ← CREATE THIS
│   ├── worlds/
│   │   └── axel_lab.world            ← CREATE THIS
│   ├── launch/
│   │   ├── gazebo_launch.py          ← CREATE THIS
│   │   └── rviz_launch.py
│   ├── config/
│   │   └── joint_controllers.yaml
│   └── meshes/                       (optional: 3D models)
│
├── axel_api/                         ← NEW (Python SDK)
│   ├── robot.py                      (high-level API)
│   ├── trajectories.py               (motion planning)
│   └── gestures.py                   (predefined motions)
│
└── tests/
    ├── test_core.py          (already done)
    ├── test_gui.py           ← ADD
    ├── test_simulation.py    ← ADD
    └── test_integration.py   ← ADD
```

---

## 📊 Development Timeline

```
Week 1-2: ✅ DONE (Foundation)
  ✓ Core modules
  ✓ Tests
  ✓ Documentation
  ✓ Windows setup

Week 2-3: 🔄 BUILD GUI WIDGETS
  • Control Panel (joint sliders)
  • Monitoring Panel (real-time display)
  • Teach Panel (position management)
  • Safety Panel (E-STOP)
  • 3D Visualization

Week 3-4: 🔄 SIMULATION
  • Create URDF model
  • Setup Gazebo world
  • RViz configuration
  • Launch files
  • Integration testing

Week 4-5: 🔄 ADVANCED FEATURES
  • Block programming (optional)
  • Performance analytics
  • Real-time logging
  • Multi-robot support (optional)

Week 5-6: 🔄 POLISH & PREP
  • Integration testing
  • Performance optimization
  • PFE presentation prep
  • Final documentation
```

---

## 🎯 Priority Order (Do This First)

### Must Have (Week 2-3)
1. **Control Panel with Joint Sliders** - Users can move robot
2. **Monitoring Panel** - See what's happening
3. **Teach/Playback** - Save and replay positions
4. **Safety Panel** - E-STOP interface
5. **Professional Styling** - Make it look good

### Should Have (Week 3-4)
1. **URDF Model** - Define robot geometry
2. **Gazebo Simulation** - Test without hardware
3. **RViz Visualization** - 3D rendering
4. **Trajectory Recording** - Save motion sequences

### Nice to Have (Week 4-5)
1. **Block Programming** - Visual programming
2. **Advanced Analytics** - Performance metrics
3. **AI Integration** - Object detection
4. **Multi-robot** - Control multiple robots

---

## 💡 Tips

1. **Use Qt Designer** - Create .ui files for GUI layouts, then convert to Python
2. **Separate Logic from GUI** - Keep all button callbacks clean and simple
3. **Use signals/slots** - Qt's event system (not callbacks) for GUI
4. **Background threads** - Use QThread for state updates, not blocking main thread
5. **Configuration files** - All robot parameters in YAML (already done!)
6. **Real-time updates** - Use timers (30 Hz) to refresh display from StateManager

---

## 🎓 Your PFE Presentation Will Show

✅ Professional desktop robot control software (NED2-style)
✅ Multiple control modes (manual, teach, playback)
✅ Real-time 3D visualization
✅ Safety systems with E-STOP
✅ Clean architecture and professional code
✅ Simulation-to-real transition capability
✅ Educational and industrial-grade design

---

**You now have a clear roadmap to build professional robot control software!** 🚀
