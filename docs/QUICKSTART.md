"""
Quick Start Guide for AXEL Robot PC Software

Getting started with development and running the application.
"""

# Getting Started Guide

## Prerequisites

1. **Operating System**: Ubuntu 20.04 LTS or 22.04 LTS (recommended)
2. **Python**: 3.10 or newer
3. **ROS 2**: Humble or Iron distribution

## Installation Steps

### Step 1: Install ROS 2

```bash
# Set locale
locale  # check for UTF-8
sudo apt update && sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Setup ROS 2 repository
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install -y curl gnupg lsb-release ubuntu-keyring

curl -sSL https://raw.githubusercontent.com/ros/ros.key | sudo apt-key add -
sudo add-apt-repository "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main"

# Install ROS 2
sudo apt install -y ros-humble-desktop
sudo apt install -y python3-colcon-common-extensions

# Source setup script
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Step 2: Clone and Setup Project

```bash
# Navigate to workspace
cd ~/Desktop/pfe/dashbord

# Install Python dependencies
python3 -m venv venv
source venv/bin/activate

pip install -r axel_robot_software/requirements.txt
```

### Step 3: Install Gazebo and RViz

```bash
sudo apt install -y ros-humble-gazebo
sudo apt install -y ros-humble-rviz2
sudo apt install -y ros-humble-joint-state-publisher-gui
```

## Running the Application

### Scenario 1: Pure Simulation (No ROS)

```bash
cd axel_robot_software
source ../../venv/bin/activate

# Run the application in simulation mode
python axel_gui/main_window.py
```

### Scenario 2: With Gazebo Simulation

```bash
# Terminal 1: Launch Gazebo
source /opt/ros/humble/setup.bash
ros2 launch axel_simulation gazebo_launch.py

# Terminal 2: Launch RViz
rviz2 -d config/default.rviz

# Terminal 3: Run PC application
source venv/bin/activate
python axel_gui/main_window.py
```

### Scenario 3: Real Robot

```bash
# On robot (running ROS 2)
# Ensure robot ROS nodes are publishing to topics

# On PC
# Modify config/robot_config.yaml to match robot's domain ID
# Run application
source venv/bin/activate
python axel_gui/main_window.py
```

## Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_core.py -v

# Run with coverage
pytest tests/ --cov=axel_core --cov-report=html
```

## Project Structure

```
axel_robot_software/
├── README.md                      # Project overview
├── setup.py                       # Package configuration
├── requirements.txt               # Python dependencies
│
├── axel_core/                     # ← START HERE (core logic)
│   ├── state_manager.py           # Robot state tracking
│   ├── robot_controller.py        # Command execution
│   ├── safety_manager.py          # Safety constraints
│   └── __init__.py
│
├── axel_ros2/                     # ROS 2 integration
│   ├── ros_bridge.py              # ROS topic mapping
│   ├── node_manager.py            # Node lifecycle
│   └── __init__.py
│
├── axel_gui/                      # GUI (PyQt6)
│   ├── main_window.py             # Application entry point
│   ├── widgets/                   # UI components (TBD)
│   └── __init__.py
│
├── axel_simulation/               # Gazebo integration
│   ├── gazebo_interface.py
│   ├── robot_urdf/                # Robot URDF models
│   └── world_configs/             # Gazebo worlds
│
├── axel_monitoring/               # Performance tracking
├── axel_logging/                  # Logging system
│
├── config/
│   ├── robot_config.yaml          # Robot configuration
│   └── default.rviz               # RViz configuration
│
├── tests/
│   ├── test_core.py               # Unit tests for core modules
│   └── __init__.py
│
└── docs/
    ├── ARCHITECTURE.md            # System design
    └── QUICKSTART.md              # This file
```

## Common Issues & Solutions

### Issue: ROS 2 command not found
**Solution**: Source ROS 2 setup script
```bash
source /opt/ros/humble/setup.bash
```

### Issue: PyQt6 import error
**Solution**: Install PyQt6
```bash
pip install PyQt6
```

### Issue: Gazebo doesn't launch
**Solution**: Verify installation
```bash
gazebo --version
# Should output version 11.x or higher
```

### Issue: "Module not found" errors
**Solution**: Install from correct directory
```bash
cd axel_robot_software
pip install -e .
```

## Key Files to Understand First

1. **[README.md](../README.md)** - Project overview
2. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design
3. **[axel_core/state_manager.py](../axel_core/state_manager.py)** - Core logic
4. **[axel_gui/main_window.py](../axel_gui/main_window.py)** - Application entry
5. **[config/robot_config.yaml](../config/robot_config.yaml)** - Configuration

## Next Steps

1. Run tests to verify setup: `pytest tests/ -v`
2. Launch application: `python axel_gui/main_window.py`
3. Read ARCHITECTURE.md for design details
4. Start implementing GUI widgets in `axel_gui/widgets/`
5. Create URDF model in `axel_simulation/robot_urdf/`

## Resources

- **ROS 2 Documentation**: https://docs.ros.org/en/humble/
- **PyQt6 Documentation**: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- **Gazebo Documentation**: http://gazebosim.org/

---

Good luck with your PFE project! 🚀
