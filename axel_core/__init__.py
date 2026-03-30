"""
AXEL Core Module

This module provides the core robotics logic independent of ROS 2.
It handles robot state management, control, and safety constraints.
"""

__version__ = "0.1.0"
__author__ = "AXEL Team"

from .state_manager import StateManager
from .robot_controller import RobotController
from .safety_manager import SafetyManager

__all__ = [
    "StateManager",
    "RobotController",
    "SafetyManager",
]
