"""
ROS 2 Integration Module

Bridge between ROS 2 middleware and AXEL core logic.
Handles:
- ROS node management
- Topic subscriptions and publications
- Service calls
"""

__version__ = "0.1.0"

from .ros_bridge import ROSBridge
from .node_manager import NodeManager

__all__ = ["ROSBridge", "NodeManager"]
