"""
AXEL Logging Module

File logging and rosbag recording.
"""

import logging
from pathlib import Path


class AXELLogger:
    """
    Application-wide logger.
    
    Handles:
    - File logging with rotation
    - Rosbag recording
    - Alert generation
    """

    def __init__(self, log_dir: str = "logs"):
        """Initialize logger."""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configure Python logging
        self.logger = logging.getLogger("AXEL")
        handler = logging.FileHandler(self.log_dir / "axel_application.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def info(self, message: str) -> None:
        """Log info message."""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log warning message."""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log error message."""
        self.logger.error(message)
