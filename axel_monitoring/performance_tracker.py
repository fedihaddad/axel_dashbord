"""
AXEL Monitoring Module

Real-time performance tracking and analysis.
"""


class PerformanceTracker:
    """
    Tracks application performance metrics.
    
    Monitors:
    - GUI update frequency (FPS)
    - ROS communication latency
    - CPU and memory usage
    """

    def __init__(self):
        """Initialize performance tracker."""
        self.metrics = {}

    def record_latency(self, label: str, latency_ms: float) -> None:
        """Record latency measurement."""
        if label not in self.metrics:
            self.metrics[label] = []
        self.metrics[label].append(latency_ms)

    def get_average_latency(self, label: str) -> float:
        """Get average latency for a label."""
        if label in self.metrics and self.metrics[label]:
            return sum(self.metrics[label]) / len(self.metrics[label])
        return 0.0
