"""Five visual introductions, with progress stored alongside student responses."""
from __future__ import annotations
import json
import math
from pathlib import Path
import uuid
from lab.navigation import set_stage
from lab.evidence import frame_snapshot
from simulation.walkthroughs import motion_samples, point_in_base, forward_command

TITLES = ("The TurtleBot motion interface", "How two wheels produce motion",
          "ROS coordinate frames", "Predict, run, and measure", "AI-assisted programming")
ASSET = Path(__file__).resolve().parents[1] / "assets" / "walkthrough.html"


def visual(st, **payload):
    import streamlit.components.v1 as components
    components.html(ASSET.read_text(encoding="utf-8").replace(
        "__PAYLOAD__", json.dumps(payload).replace("<", "\\u003c")), height=450)


def record(st, item):
    progress = st.session_state["responses"].setdefault("walkthrough.runs", [])
    if item not in progress:
        progress.append(item)


def run(st, label, key, v, w, duration=3.0, scale=1.0):
    if st.button(label, key=key):
        record(st, key)
        st.session_state["walkthrough.animation"] = {
            "samples": motion_samples(v * scale, w * scale, duration),
            "v": v * scale, "w": w * scale, "duration": duration,
            "token": uuid.uuid4().hex, "owner": st.session_state["walkthrough.index"],
        }


def animation(st):
    payload = st.session_state.get("walkthrough.animation", {})
    if payload.get("owner") != st.session_state["walkthrough.index"]:
        payload = {"samples": motion_samples(0, 0, 0), "duration": 0, "v": 0, "w": 0}
    visual(st, mode="motion", **payload)


def interface(st):
    st.write("How can two numbers tell a robot to drive, turn, or stop?")
    st.markdown("**Gazebo** is the simulated environment. **TurtleBot3** is the two-wheeled robot inside it. "
                "**ROS 2** carries messages between programs. A **Twist** message describes velocity: "
                "`linear.x` is forward speed in meters per second; `angular.z` is turning speed in radians per second.")
    st.info("Before each run, picture the path. Then watch the forward arrow and trail. "
            "These browser runs use an ideal motion model; they do not move Gazebo.")
    st.write("Positive forward speed moves toward the arrow. Negative speed reverses. Positive turning speed "
             "turns left (counterclockwise from above); negative turns right. One radian is about 57 degrees.")
    for label, key, v, w in (("Run forward: v = 0.20, ω = 0", "forward", .2, 0),
                             ("Run turn: v = 0, ω = 0.50", "turn", 0, .5),
                             ("Run arc: v = 0.20, ω = 0.50", "arc", .2, .5),
                             ("Run stop: v = 0, ω = 0", "stop", 0, 0)):
        run(st, label, key, v, w)
    with st.expander("Try the signs"):
        v = st.slider("Forward speed (m/s)", -.2, .2, -.1, .01)
        w = st.slider("Turning speed (rad/s)", -.8, .8, -.5, .05)
        run(st, "Run these signed speeds", "signed", v, w)
    animation(st)
    st.markdown("**Stopping:** a message with both values zero requests a stop. If code exits without it, "
                "behavior depends on the receiving controller. The course guard also requests a stop after "
                "roughly 0.5 seconds without fresh commands, provided the guard and simulator are running.")
    with st.expander("Connect the diagram to the live robot"):
        st.write("After environment preflight, launch the lab in a virtual desktop terminal. Leave it running "
                 "and use a second terminal for inspection. Gazebo displays the robot; RViz displays ROS data.")
        st.code("cd /workspace/week03_motion_frames_ai\nbash scripts/launch_lab.sh", language="bash")
        st.code("source /opt/ros/jazzy/setup.bash\nsource /workspace/week03_motion_frames_ai/ros2_ws/install/setup.bash\nexport ROS_DOMAIN_ID=25\nros2 topic info /student_cmd_vel\nros2 interface show geometry_msgs/msg/Twist", language="bash")
        st.write("Find the linear and angular fields. The guard receives /student_cmd_vel and forwards "
                 "bounded commands to /cmd_vel. Mission 1 executes measured motion trials.")
    return ["forward", "turn", "arc", "stop"]


def wheels(st):
    st.write("Why does changing one wheel's speed make the robot turn?")
    st.markdown("**Wheel linear speed** is distance traveled by the wheel rim per second, in m/s. "
                "Here **L = 0.16 m** is an illustrative distance between wheels. The model assumes both "
                "wheels grip the floor without slipping. Predict the turn before each run.")
    for label, key, left, right in (("Equal forward speeds", "equal", .12, .12),
                                    ("Right wheel faster", "left_turn", .04, .16),
                                    ("Left wheel faster", "right_turn", .16, .04),
                                    ("Equal and opposite", "opposite", -.06, .06)):
        run(st, label, key, (right + left)/2, (right-left)/.16)
    with st.expander("Choose your own wheel speeds"):
        left = st.slider("Left wheel vL (m/s)", -.16, .16, .08, .01)
        right = st.slider("Right wheel vR (m/s)", -.16, .16, .12, .01)
        st.caption(f"v = {(right+left)/2:.2f} m/s; ω = {(right-left)/.16:.2f} rad/s")
        run(st, "Run these wheel speeds", "custom_wheels", (right+left)/2, (right-left)/.16)
    animation(st)
    st.write("Watch the wheel stripes. Equal speeds produce a straight trail; a faster right wheel turns "
             "left; a faster left wheel turns right. Opposite equal speeds rotate in place.")
    st.latex(r"v=\frac{v_R+v_L}{2},\qquad \omega=\frac{v_R-v_L}{L}")
    st.write("The average gives forward speed; the difference determines turning. In ROS you normally "
             "request v and ω, and the controller handles the wheels.")
    with st.expander("Under the hood: inverse kinematics"):
        st.latex(r"v_R=v+\frac{\omega L}{2},\qquad v_L=v-\frac{\omega L}{2}")
        st.write("These relationships convert desired forward and turning speed into wheel speeds.")
    return ["equal", "left_turn", "right_turn", "opposite"]


def frames(st):
    st.write("How can one target have two different coordinate descriptions?")
    st.markdown("A **frame** has an origin and axis directions. A **pose** is position and orientation. "
                "A **transform** describes one frame relative to another. `odom` is the odometry reference, "
                "`base_link` follows the body, and `base_scan` follows the LiDAR. Odometry estimates movement and can drift.")
    x = st.slider("Robot x in odom (m)", 0.0, 2.0, 1.0, .1)
    y = st.slider("Robot y in odom (m)", 0.0, 2.0, 1.0, .1)
    heading = st.slider("Robot heading in odom (degrees)", -180, 180, 90, 15)
    bx, by = point_in_base(2, 1, x, y, math.radians(heading))
    visual(st, mode="frames", x=x, y=y, heading=heading)
    st.write(f"Target in odom: (2.00, 1.00) m. Target in base_link: ({bx:.2f}, {by:.2f}) m. "
             "In the body frame, x means forward and y means left.")
    st.info("At robot position (1, 1), compare heading 90° with 0°. The target changes from right "
            "of the robot, (0, -1), to ahead, (1, 0). Then move the position sliders and watch the axes.")
    poses = st.session_state.setdefault("walkthrough.frame_poses", [])
    pose = [x, y, heading]
    if pose not in poses:
        poses.append(pose)
    if len(poses) > 1:
        record(st, "frames_compared")
    st.write("The sensor is fixed to the body, so their relative transform is usually constant. "
             "Their transforms relative to odom change during motion. A sensor message identifies its frame "
             "in header.frame_id. LaserScan contains ranges and angles; points calculated from them initially "
             "use the sensor frame. Transform those points before treating them as environmental coordinates.")
    with st.expander("Inspect the live transforms"):
        st.write("Use the second terminal prepared in Walkthrough 1, with the simulator running. "
                 "Run these separately; press Ctrl+C to stop each continuous display.")
        st.code("ros2 run tf2_ros tf2_echo odom base_link\nros2 run tf2_ros tf2_echo base_link base_scan\nros2 topic echo /scan --once --field header\nros2 run course_motion_tools frame_probe", language="bash")
        st.write("Translation gives the origin offset; rotation gives orientation. The frame tree may "
                 "include intermediate frames. Gazebo world, odom, and a SLAM map frame are not interchangeable. "
                 "The probe saves a snapshot for Mission 2. Compare the body-to-sensor offset with the diagram.")
        snapshot = frame_snapshot()
        if snapshot:
            st.caption("Saved ROS snapshot; not a continuously updating measurement")
            st.json(snapshot.get("transforms", snapshot))
        else:
            st.caption("No saved snapshot yet. The diagram is illustrative; its sensor offset is not a measured TurtleBot dimension.")
    return ["frames_compared"]


def measure(st):
    st.write("How far should the robot travel, and what would a difference tell us?")
    st.write("Start at (0 m, 0 m), heading 0° toward +x. Command v = 0.20 m/s, ω = 0, for 5 s.")
    st.latex(r"d=vt=0.20\times5=1.00\ \mathrm{m}")
    st.write("The predicted final pose is (1.00 m, 0 m, 0°). Locate that endpoint before running.")
    run(st, "Run ideal prediction", "ideal_measure", .2, 0, 5)
    run(st, "Run illustrative reduced-speed example", "changed_measure", .2, 0, 5, .92)
    animation(st)
    st.caption("The second model deliberately uses 92% of the requested speed. This is not a Gazebo measurement or a prediction of its error.")
    st.table([{"Command": "0.20 m/s for 5 s", "Prediction": "x = 1.00 m", "Observation": "Modeled x = 0.92 m",
               "Difference": "Observed minus predicted = -0.08 m", "Possible explanation": "Reduced effective speed, imposed here"}])
    st.write("For a live trial, record starting and ending pose in the same frame. Along +x, subtract "
             "starting x from ending x. Odometry is a pose estimate, not simulator ground truth. A discrepancy "
             "alone does not identify a cause: timing, acceleration, slip, or the estimate could contribute.")
    with st.expander("Motion reference", expanded=True):
        st.latex(r"d=vt,\qquad \Delta\theta=\omega t,\qquad R=\frac{v}{\omega}\ (\omega\ne0)")
        st.write("d is signed straight-line displacement; heading change is in radians; R is signed turn radius. "
                 "For an arc, |v|t is path length, not start-to-end distance. Forward follows the current "
                 "heading. These formulas assume constant velocities.")
    return ["ideal_measure", "changed_measure"]


ORIGINAL = '''import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

rclpy.init()
node = Node("forward_example")
pub = node.create_publisher(Twist, "/cmd_vel", 10)
msg = Twist()
msg.linear.x = 0.2
pub.publish(msg)
time.sleep(3)
pub.publish(Twist())
node.destroy_node()
rclpy.shutdown()'''


def ai(st):
    import inspect
    st.write("How do we turn a plausible program into one we have evidence to trust?")
    st.write("Specification: forward at 0.20 m/s for 3 s, within course limits, then request a stop. "
             "Ideal travel: 0.60 m.")
    st.code("Write a ROS 2 Python node that moves the TurtleBot forward for three seconds and then stops.", language="text")
    st.caption("Instructor-authored example of a possible AI response. No live AI request was made. "
               "In Mission 3, preserve your actual assistant response before editing it.")
    st.code(ORIGINAL, language="python")
    st.warning("Inspect this example before execution: it publishes only once and bypasses the course guard.")
    if st.button("Inspect the example"):
        record(st, "ai_inspected")
    if "ai_inspected" in st.session_state["responses"].get("walkthrough.runs", []):
        st.table([
            {"Check": "Topic and type", "Finding": "Twist fits; use /student_cmd_vel to go through the guard."},
            {"Check": "Speed and units", "Finding": "0.20 m/s is below 0.22 m/s; angular velocity defaults to zero."},
            {"Check": "Timing", "Finding": "Sleeping does not guarantee three seconds of received commands."},
            {"Check": "Delivery", "Finding": "A single message can be missed during discovery. The guard needs a continuing stream."},
            {"Check": "Stopping", "Finding": "Interruption can skip the final stop. Add cleanup and retain the independent timeout."}])
        st.write("Revision: separate velocity decisions from ROS communication so timing boundaries can be tested directly.")
        st.code(inspect.getsource(forward_command), language="python")
        st.write("This excerpt handles only the decision. A complete node still needs publisher discovery, "
                 "periodic publication to /student_cmd_vel, a bounded run, and interruption cleanup.")
        if st.button("Run the decision tests"):
            record(st, "ai_tested")
        if "ai_tested" in st.session_state["responses"].get("walkthrough.runs", []):
            st.table([{"Elapsed (s)": t, "Expected (v, ω)": str(expected), "Actual": str(forward_command(t)),
                       "Pass": forward_command(t) == expected}
                      for t, expected in ((0, (.2, 0)), (2.99, (.2, 0)), (3, (0, 0)), (4, (0, 0)))])
            try:
                forward_command(0, speed=.3)
            except ValueError:
                st.success("Speed limit test passed: 0.30 m/s was rejected.")
            else:
                st.error("Speed limit test failed.")
            st.write("These tests establish outputs at the tested times and rejection of one excessive speed. "
                     "They do not establish message delivery, actual travel distance, or stopping during interruption. "
                     "Those require tests with ROS and the simulator.")
    st.markdown("**Keep the evidence:** specification → prompt → original output → inspection → revision → tests → evidence. "
                "Record what each significant change fixes. A successful run covers the conditions tested.")
    return ["ai_inspected", "ai_tested"]


def render(st):
    st.title("Lab 3 guided walkthroughs")
    st.write("Explore commands, wheels, coordinates, measurements, and code. "
             "Reuse the course Docker environment from Lab 1 for ROS inspection.")
    index = st.session_state.setdefault("walkthrough.index", 0)
    completed = st.session_state["responses"].setdefault("walkthrough.completed", [])
    st.progress(len(completed)/5, text=f"{len(completed)}/5 walkthroughs reviewed")
    # A callback keeps the selector and Next button on the same current page.
    st.session_state["walkthrough.selector"] = index
    def select():
        st.session_state["walkthrough.index"] = st.session_state["walkthrough.selector"]
        st.session_state["scroll_to_top_pending"] = True
    st.selectbox("Walkthrough", range(5), format_func=lambda i: f"{i+1}. {TITLES[i]}",
                 key="walkthrough.selector", on_change=select)
    st.header(f"{index+1}. {TITLES[index]}")
    needed = (interface, wheels, frames, measure, ai)[index](st)
    tried = st.session_state["responses"].get("walkthrough.runs", [])
    remaining = [key.replace("_", " ") for key in needed if key not in tried]
    if remaining:
        st.info("Still to try: " + ", ".join(remaining) + ". Watch each animation finish before marking reviewed.")
    if st.button("Mark reviewed", disabled=bool(remaining)):
        if index not in completed:
            completed.append(index)
        st.rerun()
    if index in completed:
        st.success("Walkthrough reviewed. You can revisit any example.")
    if index < 4:
        if st.button("Next walkthrough", disabled=index not in completed, type="primary"):
            st.session_state["walkthrough.index"] = index + 1
            st.session_state["scroll_to_top_pending"] = True
            st.rerun()
    elif st.button("Continue to environment preflight", disabled=len(completed) != 5, type="primary"):
        set_stage(st, "preflight")
