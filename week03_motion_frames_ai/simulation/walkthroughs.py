"""Ideal models used only in the browser walkthroughs."""
import math
from simulation.kinematics import Segment, integrate_segment


def motion_samples(v, omega, duration):
    steps = max(1, round(duration * 30))
    return [list(integrate_segment(0, 0, 0, Segment(v, omega, duration * i / steps)))
            for i in range(steps + 1)]


def point_in_base(px, py, x, y, heading):
    dx, dy = px - x, py - y
    c, s = math.cos(heading), math.sin(heading)
    return c * dx + s * dy, -s * dx + c * dy


def forward_command(elapsed, speed=0.2, duration=3.0):
    """Return (forward m/s, turning rad/s) for a periodic ROS publisher."""
    if not (0.0 <= speed <= 0.22):
        raise ValueError("Speed outside course limits")
    if elapsed >= duration:
        return 0.0, 0.0
    return speed, 0.0
