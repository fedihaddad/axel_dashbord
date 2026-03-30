"""
AXEL Robot Software Package

Main package initialization and convenience imports.
"""

__name__ = "axel_robot_software"
__version__ = "0.1.0"
__author__ = "AXEL Development Team"
__description__ = "Desktop PC application for humanoid robot AXEL supervision and control"

# Core modules
from axel_core import (
    StateManager,
    RobotController,
    SafetyManager,
)

# ROS 2 integration
from axel_ros2 import (
    ROSBridge,
    NodeManager,
)

__all__ = [
    "StateManager",
    "RobotController", 
    "SafetyManager",
    "ROSBridge",
    "NodeManager",
]
