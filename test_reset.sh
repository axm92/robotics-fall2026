source /opt/ros/jazzy/setup.bash
source /workspace/week01_ros_foundations/ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=24
time (ros2 topic pub --once /student_cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.0}, angular: {z: 0.0}}' >/dev/null && gz service -s /world/default/set_pose/blocking --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean --timeout 5000 --req 'name: "burger", position: {x: -2.0, y: -0.5, z: 0.01}, orientation: {w: 1.0}')