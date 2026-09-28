"""pattern.py — student implementation of build_pattern."""

import math

# Assuming Segment already exists elsewhere in this module or an import, e.g.:
# from .segment import Segment


def build_pattern(pattern_name: str) -> list[Segment]:
    """Return the ordered Segment list for a named motion pattern."""
    if pattern_name != 'alternating_arcs':
        raise ValueError(f'Unknown pattern name: "{pattern_name}"')

    linear_speed = 0.15   # m/s, within 0.22 m/s limit
    angular_speed = 0.5   # rad/s, within 0.80 rad/s limit
    turn_angle = math.pi / 4  # 45 degrees in radians
    arc_duration = turn_angle / angular_speed  # ≈ 1.5708 s per arc
    stop_duration = 0.2   # brief pause between arcs

    turn_signs = [1, -1, 1, -1]  # +45, -45, +45, -45 (left, right, left, right)

    segments: list[Segment] = []
    for i, sign in enumerate(turn_signs):
        segments.append(
            Segment(
                linear_x=linear_speed,
                angular_z=sign * angular_speed,
                duration=arc_duration,
            )
        )
        # Brief stop after each arc except skip trailing stop after the last one,
        # since pattern_node.py sends its own final zero command.
        if i < len(turn_signs) - 1:
            segments.append(
                Segment(linear_x=0.0, angular_z=0.0, duration=stop_duration)
            )

    return segments