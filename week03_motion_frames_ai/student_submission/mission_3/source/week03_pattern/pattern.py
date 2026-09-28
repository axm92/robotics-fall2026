"""AI-assisted motion pattern implementation.

Preserve the original AI response in Streamlit. Review it, then implement a safe
version here. The node accepts only segments returned by ``build_pattern``.
"""
from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Segment:
    linear_x: float
    angular_z: float
    duration: float

def build_pattern(pattern_name: str) -> list[Segment]:
    """Return ordered, bounded motion segments for the assigned pattern.

    Supported assignments are ``rounded_rectangle``, ``l_path``, and
    ``alternating_arcs``. Do not include the final stop; the ROS wrapper always
    publishes it and the evaluator verifies it.
    """
    if pattern_name != 'alternating_arcs':
        raise ValueError(f'Unknown pattern name: "{pattern_name}"')

    linear_speed = 0.15
    angular_speed = 0.5
    turn_angle = math.pi / 4
    arc_duration = abs(turn_angle / angular_speed)

    turn_signs = [1, -1, 1, -1]  # +45°, -45°, +45°, -45°

    return [
        Segment(
            linear_x=linear_speed,
            angular_z=sign * angular_speed,
            duration=arc_duration,
        )
        for sign in turn_signs
    ]

