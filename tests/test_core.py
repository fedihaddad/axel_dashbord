"""
Unit Tests for AXEL Core Modules

Tests for state manager, robot controller, and safety manager.
"""

import pytest
from datetime import datetime

from axel_core import StateManager, RobotController, SafetyManager
from axel_core.safety_manager import JointLimits


class TestStateManager:
    """Tests for StateManager class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.state_manager = StateManager()

    def test_joint_state_update(self):
        """Test updating joint state."""
        self.state_manager.update_joint_state("joint1", position=1.0, velocity=0.5)
        
        state = self.state_manager.get_current_state()
        assert "joint1" in state.joints
        assert state.joints["joint1"].position == 1.0
        assert state.joints["joint1"].velocity == 0.5

    def test_battery_update(self):
        """Test connection status update (battery removed - always powered)."""
        self.state_manager.update_connection_status("connected", "ethernet")
        state = self.state_manager.get_current_state()
        assert state.connection_status == "connected"
        assert state.connection_type == "ethernet"

    def test_mode_change(self):
        """Test control mode switching."""
        self.state_manager.set_mode("MANUAL")
        state = self.state_manager.get_current_state()
        assert state.mode == "MANUAL"

    def test_invalid_mode_rejected(self):
        """Test that invalid modes are rejected."""
        with pytest.raises(ValueError):
            self.state_manager.set_mode("INVALID_MODE")

    def test_emergency_stop(self):
        """Test emergency stop flag."""
        self.state_manager.set_emergency_stop(True)
        state = self.state_manager.get_current_state()
        assert state.emergency_stop is True

    def test_callback_registration(self):
        """Test state change callback."""
        callback_called = []
        
        def test_callback(state):
            callback_called.append(True)
        
        self.state_manager.register_callback(test_callback)
        self.state_manager.set_mode("MANUAL")  # Changed from battery update
        
        assert len(callback_called) > 0


class TestSafetyManager:
    """Tests for SafetyManager class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.safety_manager = SafetyManager()

    def test_joint_limits_setting(self):
        """Test setting joint limits."""
        limits = JointLimits(
            joint_name="joint1",
            min_position=-1.57,
            max_position=1.57,
            max_velocity=1.0,
            max_effort=10.0
        )
        self.safety_manager.set_joint_limits("joint1", limits)
        
        retrieved = self.safety_manager.get_joint_limits("joint1")
        assert retrieved.min_position == -1.57
        assert retrieved.max_position == 1.57

    def test_command_validation_within_limits(self):
        """Test that valid commands are accepted."""
        limits = JointLimits(
            joint_name="joint1",
            min_position=-1.57,
            max_position=1.57
        )
        self.safety_manager.set_joint_limits("joint1", limits)
        
        assert self.safety_manager.validate_joint_command("joint1", 0.0) is True
        assert self.safety_manager.validate_joint_command("joint1", 1.0) is True

    def test_command_validation_out_of_bounds(self):
        """Test that out-of-bounds commands are rejected."""
        limits = JointLimits(
            joint_name="joint1",
            min_position=-1.57,
            max_position=1.57
        )
        self.safety_manager.set_joint_limits("joint1", limits)
        
        assert self.safety_manager.validate_joint_command("joint1", 2.0) is False
        assert self.safety_manager.validate_joint_command("joint1", -2.0) is False

    def test_emergency_stop_activation(self):
        """Test emergency stop."""
        assert self.safety_manager.is_emergency_stop_active() is False
        
        self.safety_manager.activate_emergency_stop()
        assert self.safety_manager.is_emergency_stop_active() is True
        
        # Commands should be rejected when E-STOP is active
        assert self.safety_manager.validate_joint_command("joint1", 0.0) is False

    def test_emergency_stop_deactivation(self):
        """Test emergency stop deactivation."""
        self.safety_manager.activate_emergency_stop()
        self.safety_manager.deactivate_emergency_stop()
        
        assert self.safety_manager.is_emergency_stop_active() is False


class TestRobotController:
    """Tests for RobotController class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.safety_manager = SafetyManager()
        self.state_manager = StateManager()
        self.controller = RobotController(
            state_manager=self.state_manager,
            safety_manager=self.safety_manager
        )

    def test_joint_command_queueing(self):
        """Test that commands are queued."""
        # Set up limits
        limits = JointLimits(
            joint_name="joint1",
            min_position=-1.57,
            max_position=1.57
        )
        self.safety_manager.set_joint_limits("joint1", limits)
        
        # Send command
        result = self.controller.move_joint("joint1", 1.0)
        assert result is True
        
        commands = self.controller.get_queued_commands()
        assert len(commands) == 1
        assert commands[0].name == "joint1"

    def test_command_rejection_by_safety(self):
        """Test that unsafe commands are rejected."""
        limits = JointLimits(
            joint_name="joint1",
            min_position=-1.57,
            max_position=1.57
        )
        self.safety_manager.set_joint_limits("joint1", limits)
        
        # Try to send out-of-bounds command
        result = self.controller.move_joint("joint1", 2.0)
        assert result is False
        
        commands = self.controller.get_queued_commands()
        assert len(commands) == 0

    def test_emergency_stop_clears_queue(self):
        """Test that emergency stop clears command queue."""
        limits = JointLimits(
            joint_name="joint1",
            min_position=-1.57,
            max_position=1.57
        )
        self.safety_manager.set_joint_limits("joint1", limits)
        
        # Queue some commands
        self.controller.move_joint("joint1", 0.5)
        self.controller.move_joint("joint1", 1.0)
        
        assert len(self.controller.get_queued_commands()) == 2
        
        # Emergency stop
        self.controller.emergency_stop()
        
        assert len(self.controller.get_queued_commands()) == 0
        assert self.safety_manager.is_emergency_stop_active() is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
