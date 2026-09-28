#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from rclpy.time import Time

from geometry_msgs.msg import PointStamped
import tf2_ros
from tf2_geometry_msgs import do_transform_point  # registers PointStamped support


class CameraPointToBaseLink(Node):
    def __init__(self):
        super().__init__('camera_point_to_base_link')

        # Frame this node will publish/consume points in
        self.target_frame = 'base_link'

        # TF2 buffer + listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Subscribe to detected points from the hallway camera
        # Adjust topic/frame_id to match your camera driver / detector node
        self.sub = self.create_subscription(
            PointStamped,
            '/hallway_camera/detected_point',
            self.point_callback,
            10
        )

        # Publish the transformed point
        self.pub = self.create_publisher(
            PointStamped,
            '/hallway_camera/detected_point_base_link',
            10
        )

    def point_callback(self, msg: PointStamped):
        try:
            # Look up the transform at the timestamp of the incoming point,
            # waiting briefly if it hasn't arrived in the TF tree yet
            transform = self.tf_buffer.lookup_transform(
                self.target_frame,
                msg.header.frame_id,
                msg.header.stamp,
                timeout=Duration(seconds=0.2)
            )

            transformed_point = do_transform_point(msg, transform)
            transformed_point.header.frame_id = self.target_frame

            self.pub.publish(transformed_point)

            self.get_logger().debug(
                f'Point in {self.target_frame}: '
                f'({transformed_point.point.x:.3f}, '
                f'{transformed_point.point.y:.3f}, '
                f'{transformed_point.point.z:.3f})'
            )

        except (tf2_ros.LookupException,
                tf2_ros.ConnectivityException,
                tf2_ros.ExtrapolationException) as e:
            self.get_logger().warn(f'Could not transform point: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = CameraPointToBaseLink()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()