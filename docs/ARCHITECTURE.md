# AXEL Architecture Document

## System Architecture

### 1. Layered Architecture

The AXEL PC software follows a clean, layered architecture:

```
┌────────────────────────────────────────────┐
│  Presentation Layer (PyQt6)                │
│  - Main window, widgets, dialogs           │
│  - User interaction handling               │
│  - Real-time visualization                 │
└────────────────────────────────────────────┘
                    ▲ │
                    │ ▼
┌────────────────────────────────────────────┐
│  Application Layer (Core Modules)          │
│  - StateManager: Robot state tracking      │
│  - RobotController: Command execution      │
│  - SafetyManager: Safety constraints       │
└────────────────────────────────────────────┘
                    ▲ │
                    │ ▼
┌────────────────────────────────────────────┐
│  Integration Layer (ROS 2)                 │
│  - ROSBridge: Topic translation            │
│  - NodeManager: Lifecycle management       │
│  - Publishers/Subscribers                  │
└────────────────────────────────────────────┘
                    ▲ │
                    │ ▼
┌────────────────────────────────────────────┐
│  Execution Layer                           │
│  - Gazebo Simulation                       │
│  - Real Robot Hardware                     │
│  - Sensor Input (IMU, cameras, etc.)       │
└────────────────────────────────────────────┘
```

### 2. Module Responsibilities

#### **axel_core/**
- **StateManager**: Maintains robot state (joints, sensors, battery)
- **RobotController**: Executes movement commands
- **SafetyManager**: Enforces safety limits and E-STOP logic

*Design Principle*: Pure Python, no ROS dependencies (for portability and testability)

#### **axel_ros2/**
- **ROSBridge**: Translates ROS topics ↔ internal state
- **NodeManager**: Manages ROS node lifecycle

*Design Principle*: Isolated ROS integration (swap for other middleware if needed)

#### **axel_gui/**
- **MainWindow**: Application entry point and window management
- **Widgets**: Modular UI components (control, monitoring, logs, safety)

*Design Principle*: PyQt6 only, decoupled from business logic

#### **axel_simulation/**
- **GazeboInterface**: Simulator control
- URDF models and world files

#### **axel_monitoring/**
- **PerformanceTracker**: Latency and FPS monitoring

#### **axel_logging/**
- **AXELLogger**: File logging with rotation
- Rosbag recording

### 3. Data Flow

```
SENSOR INPUT
    │
    ▼
ROSBridge Subscriptions
    │
    ▼
StateManager (updates state)
    │
    ├──→ GUI Callbacks (update display)
    │
    └──→ Safety Checks (validate commands)
         │
         ▼
    RobotController (queues commands)
         │
         ▼
    ROS Publishers
         │
         ▼
ROBOT EXECUTION
```

### 4. Threading Model

- **Main Thread**: PyQt6 event loop (GUI)
- **ROS Spin Thread**: ROS executor (non-blocking)
- **Callback Threads**: State updates from ROS

*Safety*: All state access protected by locks (threading.RLock)

### 5. Safety Architecture

```
┌─────────────────────────┐
│  Command Source         │ (GUI, autonomous)
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  SafetyManager          │ ◄─── Joint limits
│  - E-STOP check         │ ◄─── Velocity limits
│  - Limit validation     │ ◄─── Effort limits
│  - Status checks        │
└────────────┬────────────┘
             │ (ACCEPT/REJECT)
             ▼
┌─────────────────────────┐
│  RobotController        │
│  - Command queueing     │
│  - Execution planning   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  ROSBridge Publisher    │
└────────────┬────────────┘
             │
             ▼
         ROBOT
```

### 6. Configuration Management

YAML-based configuration (`config/robot_config.yaml`):

```yaml
robot:
  joints:
    - name, min/max position, velocity, effort

safety:
  emergency_stop settings
  watchdog timeouts

ros2:
  node configuration
  topic names

gui:
  window size
  update rates
  panel settings

logging:
  file locations
  rosbag topics
```

## Development Workflow

### Phase 1: Foundation
- [ ] Core modules (StateManager, RobotController, SafetyManager)
- [ ] ROS 2 integration layer
- [ ] Basic PyQt6 GUI skeleton
- [ ] Configuration system

### Phase 2: Simulation
- [ ] Gazebo integration
- [ ] URDF model creation
- [ ] RViz visualization
- [ ] Joint control interface

### Phase 3: Features
- [ ] Real-time monitoring panel
- [ ] Control modes (manual, semi-auto, autonomous)
- [ ] Logging and rosbag recording
- [ ] Performance analytics

### Phase 4: Polish
- [ ] Error handling and recovery
- [ ] Testing and validation
- [ ] Documentation
- [ ] Performance optimization

## Best Practices Implemented

✅ **Modularity**: Each module has single responsibility
✅ **Testability**: Core logic independent of ROS/GUI
✅ **Thread Safety**: All shared state protected by locks
✅ **Configuration**: Centralized YAML configuration
✅ **Logging**: Comprehensive logging for debugging
✅ **Documentation**: Docstrings and comments throughout

## Future Extensions

- Multi-robot support
- Machine learning integration
- Advanced visualization (3D meshes, point clouds)
- Web-based remote interface
- Hardware-in-the-loop simulation
