"""
AXEL GUI Widgets Package
Contains reusable UI components for robot control
"""

from axel_gui.widgets.control_panel import ControlPanel, JointSlider
from axel_gui.widgets.visualization_3d import Visualization3DPanel

__all__ = [
    'ControlPanel',
    'JointSlider',
    'Visualization3DPanel',
]
