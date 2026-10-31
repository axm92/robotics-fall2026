"""Camera line controller used by the ROS node.
Edit one choice at a time, save, stop the old controller, reset the world and run.
The initial steering gain is intentionally weak. Diagnose it, do not assume it
will follow bends. The ROS node keeps the freshness and motion safeguards.
"""
GAIN = 0.08
SPEED = 0.16  # metres per second before slowing for large image errors
ROI_TOP = 0.60  # fraction of image height, measured from the top
ROI_BOTTOM = 0.95
HUE_LOW = 140  # OpenCV hue, 0 to 179
HUE_HIGH = 169
MIN_FRACTION = 0.002  # smallest selected contour area / region area


def angular_velocity(error, gain):
    """Image right is positive error. ROS left turn is positive angular speed."""
    return -gain * error
