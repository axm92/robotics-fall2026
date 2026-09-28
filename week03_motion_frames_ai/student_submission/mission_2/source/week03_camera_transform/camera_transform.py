"""Mission 2 student implementation.

Complete only ``transform_camera_point`` after preserving the initial AI output
in the guide. Course tests supply both real and simulated TF buffers.
"""
from geometry_msgs.msg import PointStamped
import tf2_geometry_msgs  # noqa: F401  (registers PointStamped transform support)
import tf2_ros
from tf2_ros import TransformException


def transform_camera_point(tf_buffer, point: PointStamped) -> PointStamped | None:
    """Return a hall_camera point expressed in base_link, or None if unavailable."""
    if point.header.frame_id != 'hall_camera':
        raise ValueError(
            f'Expected point in frame "hall_camera", got "{point.header.frame_id}"'
        )

    try:
        return tf_buffer.transform(point, 'base_link')
    except TransformException:
        return None