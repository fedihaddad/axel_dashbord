"""
Robot Controller - Command Interface

Handles robot control commands including:
- Joint position commands
- Gripper control
- Mode switching
- Command validation
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import threading


@dataclass
class JointCommand:
    """Command for a single joint."""
    name: str
    position: float
    velocity: float = 0.5  # rad/s
    acceleration: float = 0.1  # rad/s^2
    max_effort: float = 10.0  # Nm


class ControlMode:
    """Valid control modes."""
    IDLE = "IDLE"
    MANUAL = "MANUAL"
    SEMI_AUTONOMOUS = "SEMI_AUTO"
    AUTONOMOUS = "AUTONOMOUS"


class RobotController:
    """
    Commands the robot to perform actions.
    
    - Validates commands before sending
    - Maintains command queue
    - Coordinates with safety system
    """

    def __init__(self, state_manager=None, safety_manager=None):
        """
        Initialize robot controller.
        
        Args:
            state_manager: Reference to StateManager instance
            safety_manager: Reference to SafetyManager instance
        """
        self.state_manager = state_manager
        self.safety_manager = safety_manager
        self._command_queue: List[JointCommand] = []
        self._lock = threading.Lock()
        self._is_executing = False

    def move_joint(self, joint_name: str, position: float, velocity: float = 0.5) -> bool:
        """
        Send command to move a single joint.
        
        Args:
            joint_name: Name of joint to move
            position: Target position in radians
            velocity: Max velocity in rad/s
            
        Returns:
            True if command accepted, False if rejected (safety)
        """
        # Check safety constraints
        if self.safety_manager:
            if not self.safety_manager.validate_joint_command(joint_name, position):
                print(f"Command rejected by safety system: {joint_name} -> {position}")
                return False

        # Create command
        cmd = JointCommand(
            name=joint_name,
            position=position,
            velocity=velocity,
        )

        # Queue command
        with self._lock:
            self._command_queue.append(cmd)

        return True

    def move_joints(self, commands: Dict[str, float]) -> bool:
        """
        Move multiple joints simultaneously.
        
        Args:
            commands: Dict of {joint_name: position}
            
        Returns:
            True if all commands accepted
        """
        all_accepted = True
        for joint_name, position in commands.items():
            if not self.move_joint(joint_name, position):
                all_accepted = False

        return all_accepted

    def stop_all(self) -> None:
        """Stop all motion immediately."""
        with self._lock:
            self._command_queue.clear()
            self._is_executing = False

    def emergency_stop(self) -> None:
        """Trigger emergency stop."""
        self.stop_all()
        if self.safety_manager:
            self.safety_manager.activate_emergency_stop()
        if self.state_manager:
            self.state_manager.set_emergency_stop(True)

    def get_queued_commands(self) -> List[JointCommand]:
        """Get pending commands."""
        with self._lock:
            return self._command_queue.copy()

    def clear_queue(self) -> None:
        """Clear command queue."""
        with self._lock:
            self._command_queue.clear()
