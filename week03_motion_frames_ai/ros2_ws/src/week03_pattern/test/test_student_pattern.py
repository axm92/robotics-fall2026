import math
import os
import unittest
from week03_pattern.pattern import build_pattern


class MyPatternTests(unittest.TestCase):
    def test_my_pattern_geometry(self):
        segments = build_pattern(os.environ["WEEK03_ASSIGNED_PATTERN"])

        # Expect exactly 4 arc segments, no stop segments between them
        self.assertEqual(len(segments), 4)

        arc_segments = [seg for seg in segments if seg.angular_z != 0.0]
        self.assertEqual(len(arc_segments), 4)

        # Each arc: radius = |v / w| should be ~0.30 m within 0.02 m
        for seg in arc_segments:
            radius = abs(seg.linear_x / seg.angular_z)
            self.assertAlmostEqual(radius, 0.30, delta=0.02)

        # Each arc: angle = |w * t| should be ~pi/4 within 0.04 rad
        for seg in arc_segments:
            angle = abs(seg.angular_z * seg.duration)
            self.assertAlmostEqual(angle, math.pi / 4, delta=0.04)

        # Every speed stays inside course limits
        for seg in segments:
            self.assertLessEqual(abs(seg.linear_x), 0.22)
            self.assertLessEqual(abs(seg.angular_z), 0.80)
            self.assertGreater(seg.duration, 0.0)
            self.assertLessEqual(seg.duration, 30.0)

        # Total duration under 60 seconds
        total_duration = sum(seg.duration for seg in segments)
        self.assertLessEqual(total_duration, 60.0)

    def test_my_pattern_order(self):
        segments = build_pattern(os.environ["WEEK03_ASSIGNED_PATTERN"])

        # First segment moves forward (positive linear_x)
        self.assertGreater(segments[0].linear_x, 0.0)

        # Turn signs alternate: +45, -45, +45, -45 (left, right, left, right)
        expected_signs = [1, -1, 1, -1]
        actual_signs = [1 if seg.angular_z > 0 else -1 for seg in segments]
        self.assertEqual(actual_signs, expected_signs)

        # Last segment is still an arc (no trailing stop segment appended)
        self.assertNotEqual(segments[-1].angular_z, 0.0)

        # Net heading change across all segments should cancel to ~0
        net_heading = sum(seg.angular_z * seg.duration for seg in segments)
        self.assertAlmostEqual(net_heading, 0.0, delta=0.04)


if __name__ == "__main__":
    unittest.main()