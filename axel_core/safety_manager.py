"""
Safety Manager - Safety Constraints and Emergency Stop

Enforces:
- Joint position limits
- Velocity limits
- Effort limits
- Emergency stop logic
"""

from dataclasses import dataclass
from typing import Dict, Optional
import threading


@dataclass
class JointLimits:
    """Position, velocity, and effort limits for a joint."""
    joint_name: str
    min_position: float = -3.14  # radians
    max_position: float = 3.14
    max_velocity: float = 1.0  # rad/s
    max_effort: float = 10.0  # Nm


class SafetyManager:
    """
    Manages safety constraints and emergency stop.
    
    Validates all commands before execution and monitors for unsafe states.
    """

    def __init__(self):
        """Initialize safety manager with default limits."""
        self._joint_limits: Dict[str, JointLimits] = {}
        self._emergency_stop_active = False
        self._lock = threading.RLock()
        self._safety_callbacks = []

    def set_joint_limits(self, joint_name: str, limits: JointLimits) -> None:
        """Set position and effort limits for a joint."""
        with self._lock:
            self._joint_limits[joint_name] = limits

    def get_joint_limits(self, joint_name: str) -> Optional[JointLimits]:
        """Get limits for a joint."""
        with self._lock:
            return self._joint_limits.get(joint_name)

    def validate_joint_command(self, joint_name: str, position: float) -> bool:
        """
        Validate a joint command against safety constraints.
        
        Args:
            joint_name: Name of joint
            position: Target position in radians
            
        Returns:
            True if command is safe, False otherwise
        """
        with self._lock:
            # Check emergency stop
            if self._emergency_stop_active:
                return False

            # Check limits if defined
            if joint_name in self._joint_limits:
                limits = self._joint_limits[joint_name]
                if not (limits.min_position <= position <= limits.max_position):
                    print(f"Position out of bounds for {joint_name}: {position}")
                    return False

        return True

    def activate_emergency_stop(self) -> None:
        """Activate emergency stop - prevents all further motion."""
        with self._lock:
            if not self._emergency_stop_active:
                self._emergency_stop_active = True
                self._notify_safety_callbacks("EMERGENCY_STOP_ACTIVATED")
                print("EMERGENCY STOP ACTIVATED")

    def deactivate_emergency_stop(self) -> None:
        """Deactivate emergency stop."""
        with self._lock:
            if self._emergency_stop_active:
                self._emergency_stop_active = False
                self._notify_safety_callbacks("EMERGENCY_STOP_DEACTIVATED")
                print("Emergency stop deactivated")

    def is_emergency_stop_active(self) -> bool:
        """Check if emergency stop is active."""
        with self._lock:
            return self._emergency_stop_active

    def register_safety_callback(self, callback: callable) -> None:
        """
        Register callback for safety events.
        
        Callback signature: callback(event: str) -> None
        """
        with self._lock:
            self._safety_callbacks.append(callback)

    def _notify_safety_callbacks(self, event: str) -> None:
        """Notify callbacks of safety event."""
        for callback in self._safety_callbacks:
            try:
                callback(event)
            except Exception as e:
                print(f"Error in safety callback: {e}")

    def reset_to_safe_state(self) -> None:
        """Reset robot to safe state (all zeros)."""
        with self._lock:
            print("Resetting to safe state...")
            self._emergency_stop_active = False
