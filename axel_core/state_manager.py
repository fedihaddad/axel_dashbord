"""
State Manager - Core Robot State Tracking

Maintains the current state of the robot including:
- Joint positions and velocities
- Sensor readings
- Battery status
- System health
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import threading


@dataclass
class JointState:
    """Represents state of a single joint."""
    name: str
    position: float = 0.0
    velocity: float = 0.0
    effort: float = 0.0
    is_healthy: bool = True


@dataclass
class RobotState:
    """Represents complete robot state snapshot."""
    timestamp: datetime
    joints: Dict[str, JointState] = field(default_factory=dict)
    cpu_temp: float = 0.0
    connection_status: str = "disconnected"  # disconnected, connecting, connected
    connection_type: str = ""  # ethernet, wifi
    is_moving: bool = False
    emergency_stop: bool = False
    mode: str = "IDLE"  # IDLE, MANUAL, SEMI_AUTO, AUTONOMOUS


class StateManager:
    """
    Manages and tracks robot state in real-time.
    
    Thread-safe access to robot state with callbacks for state changes.
    """

    def __init__(self, max_history: int = 1000):
        """
        Initialize state manager.
        
        Args:
            max_history: Maximum number of state snapshots to maintain
        """
        self._current_state: RobotState = RobotState(timestamp=datetime.now())
        self._state_history: List[RobotState] = []
        self._max_history = max_history
        self._lock = threading.RLock()
        self._callbacks: List[callable] = []

    def update_joint_state(
        self, 
        joint_name: str, 
        position: float, 
        velocity: float = 0.0, 
        effort: float = 0.0
    ) -> None:
        """
        Update position/velocity/effort for a joint.
        
        Args:
            joint_name: Name of the joint
            position: Joint position in radians
            velocity: Joint velocity in rad/s
            effort: Joint effort in Nm
        """
        with self._lock:
            if joint_name not in self._current_state.joints:
                self._current_state.joints[joint_name] = JointState(name=joint_name)
            
            joint = self._current_state.joints[joint_name]
            joint.position = position
            joint.velocity = velocity
            joint.effort = effort
            
            self._notify_callbacks()

    def update_connection_status(self, status: str, connection_type: str = "") -> None:
        """
        Update robot connection status.
        
        Args:
            status: One of "disconnected", "connecting", "connected"
            connection_type: One of "ethernet", "wifi"
        """
        valid_statuses = {"disconnected", "connecting", "connected"}
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}")
        
        with self._lock:
            self._current_state.connection_status = status
            self._current_state.connection_type = connection_type
            self._notify_callbacks()

    def update_temperature(self, temp: float) -> None:
        """Update CPU temperature in Celsius."""
        with self._lock:
            self._current_state.cpu_temp = temp
            self._notify_callbacks()

    def set_mode(self, mode: str) -> None:
        """
        Set robot control mode.
        
        Args:
            mode: One of IDLE, MANUAL, SEMI_AUTO, AUTONOMOUS
        """
        valid_modes = {"IDLE", "MANUAL", "SEMI_AUTO", "AUTONOMOUS"}
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode: {mode}. Must be one of {valid_modes}")
        
        with self._lock:
            self._current_state.mode = mode
            self._notify_callbacks()

    def set_emergency_stop(self, value: bool) -> None:
        """Set emergency stop status."""
        with self._lock:
            self._current_state.emergency_stop = value
            self._notify_callbacks()

    def get_current_state(self) -> RobotState:
        """Get a copy of current robot state (thread-safe)."""
        with self._lock:
            return self._snapshot_state()

    def get_joint_state(self, joint_name: str) -> Optional[JointState]:
        """Get state of a specific joint."""
        with self._lock:
            return self._current_state.joints.get(joint_name)

    def register_callback(self, callback: callable) -> None:
        """
        Register callback to be called on state changes.
        
        Callback signature: callback(state: RobotState) -> None
        """
        with self._lock:
            self._callbacks.append(callback)

    def _notify_callbacks(self) -> None:
        """Notify all registered callbacks of state change."""
        state_copy = self._snapshot_state()
        for callback in self._callbacks:
            try:
                callback(state_copy)
            except Exception as e:
                print(f"Error in state callback: {e}")

    def _snapshot_state(self) -> RobotState:
        """Create a snapshot of current state."""
        return RobotState(
            timestamp=datetime.now(),
            joints={k: JointState(**vars(v)) for k, v in self._current_state.joints.items()},
            cpu_temp=self._current_state.cpu_temp,
            connection_status=self._current_state.connection_status,
            connection_type=self._current_state.connection_type,
            is_moving=self._current_state.is_moving,
            emergency_stop=self._current_state.emergency_stop,
            mode=self._current_state.mode,
        )

    def clear_history(self) -> None:
        """Clear state history."""
        with self._lock:
            self._state_history.clear()
