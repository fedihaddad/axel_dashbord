"""
Node Manager - ROS 2 Node Lifecycle Management

Handles initialization and shutdown of ROS 2 nodes.
"""

import threading
from typing import Optional


class NodeManager:
    """
    Manages ROS 2 node lifecycle.
    
    Handles node creation, spinning, and shutdown.
    """

    def __init__(self, node_name: str = "axel_control"):
        """
        Initialize node manager.
        
        Args:
            node_name: Name of ROS node
        """
        self.node_name = node_name
        self._node = None
        self._executor = None
        self._spin_thread: Optional[threading.Thread] = None
        self._is_running = False

    def create_node(self) -> None:
        """Create ROS 2 node."""
        try:
            import rclpy
            if not rclpy.ok():
                rclpy.init()
            self._node = rclpy.create_node(self.node_name)
            print(f"ROS 2 node '{self.node_name}' created")
        except ImportError:
            print("WARNING: rclpy not available. Running in simulation mode.")
        except Exception as e:
            print(f"Error creating ROS node: {e}")

    def spin_in_thread(self) -> None:
        """Spin ROS executor in background thread."""
        if not self._is_running:
            try:
                import rclpy
                from rclpy.executors import SingleThreadedExecutor
                
                self._executor = SingleThreadedExecutor()
                self._executor.add_node(self._node)
                self._is_running = True
                
                self._spin_thread = threading.Thread(
                    target=self._spin,
                    daemon=True
                )
                self._spin_thread.start()
                print("ROS 2 executor spinning in background")
            except Exception as e:
                print(f"Error starting ROS executor: {e}")

    def _spin(self) -> None:
        """Internal spin method."""
        try:
            import rclpy
            while self._is_running and rclpy.ok():
                self._executor.spin_once(timeout_sec=0.1)
        except Exception as e:
            print(f"Error in spin loop: {e}")

    def shutdown(self) -> None:
        """Shutdown ROS node and executor."""
        self._is_running = False
        
        if self._spin_thread:
            self._spin_thread.join(timeout=2.0)
        
        if self._node:
            self._node.destroy_node()
        
        try:
            import rclpy
            if rclpy.ok():
                rclpy.shutdown()
        except Exception as e:
            print(f"Error during ROS shutdown: {e}")
        
        print("ROS 2 node shutdown complete")

    def get_node(self):
        """Get reference to ROS node."""
        return self._node

    def is_running(self) -> bool:
        """Check if node is running."""
        return self._is_running
