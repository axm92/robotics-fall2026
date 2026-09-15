from __future__ import annotations
import math
from lab.evidence import evidence_id, frame_snapshot
from lab.frame_learning import reference_snapshot, valid_snapshot, correct_point
from lab.navigation import set_stage
from lab.session import complete_mission, response, set_response
from lab.submissions import save_mission
from lab.ui import render_check
from missions.mission_2 import evaluate
from pages.concepts import visual


def answer(st,key,label):
    full=f"mission_2.{key}"
    widget=f"m2.{key}"
    if widget not in st.session_state:
        st.session_state[widget]=str(response(st,full,""))
    value=st.text_area(label,key=widget)
    set_response(st,full,value)


def render(st):
    st.title("Mission 2: Coordinate frames")
    st.write("Use a frame to explain where a point is, then investigate what happens when software "
             "uses the wrong frame. This mission inspects data and diagrams; it does not command robot motion.")
    st.info("A frame combines an origin with axis directions. A transform gives the translation "
            "(origin offset) and rotation between frames. Always attach a frame name and units to coordinates.")

    st.header("Part A: Identify the frame system")
    st.markdown("**odom:** the reference used to estimate robot motion; it can drift over time. "
                "**base_link:** attached to the robot body, with +x forward and +y left. "
                "**base_scan:** attached to the LiDAR sensor. Its mounting transform relative to the body is normally fixed.")
    with st.expander("Capture the live ROS evidence",expanded=True):
        st.write("Keep Gazebo and the course launch running. Open a second terminal in the virtual desktop "
                 "and run the following preparation commands there:")
        st.code("cd /workspace/week03_motion_frames_ai\nsource /opt/ros/jazzy/setup.bash\nsource ros2_ws/install/setup.bash\nexport ROS_DOMAIN_ID=25\nexport WEEK03_EVIDENCE_DIR=/workspace/week03_motion_frames_ai/runtime/evidence",language="bash")
        st.write("Run the next commands individually. tf2_echo prints a changing transform; Ctrl+C ends "
                 "that display. You do not need to interpret the quaternion rotation fields yet; yaw is the planar heading.")
        st.code("ros2 run tf2_ros tf2_echo odom base_link\nros2 run tf2_ros tf2_echo base_link base_scan\nros2 topic echo /scan --once --field header\nros2 run course_motion_tools frame_probe",language="bash")
        st.write("Read the translation values and frame names. The sensor header names the frame for its "
                 "ranges and angles. The final command saves a snapshot; select it below. "
                 "The actual TF tree can contain intermediate frames such as base_footprint.")
        if st.button("Load latest live snapshot"):
            candidate=frame_snapshot()
            latest=dict(candidate) if isinstance(candidate,dict) else {}
            latest["source"]="live"
            if valid_snapshot(latest):
                set_response(st,"mission_2.snapshot",latest)
                st.rerun()
            else:
                st.warning("No complete snapshot is available. Check that the simulator is running, "
                           "run frame_probe again, or use reference evidence below.")
    with st.expander("Use reference evidence if ROS is unavailable"):
        st.write("The reference uses a robot at odom (1, 1) m, heading 90°, with a sensor mounted "
                 "0.20 m forward of the body origin. These are teaching values, not measurements of your robot.")
        if st.button("Use reference snapshot"):
            set_response(st,"mission_2.snapshot",reference_snapshot())
            st.rerun()
    snapshot=response(st,"mission_2.snapshot",{})
    if valid_snapshot(snapshot):
        st.success(f"Selected evidence: {snapshot['source']}. Captured/created: {snapshot['captured_at']}")
        st.caption("This selection stays fixed until you explicitly load or select another snapshot.")
        rows=[]
        for key,label in (("base_scan_to_base_link","Sensor origin expressed in base_link"),
                          ("base_scan_to_odom","Sensor origin expressed in odom")):
            t=snapshot["transforms"][key]
            rows.append({"Relationship":label,"x (m)":t["translation"]["x"],"y (m)":t["translation"]["y"],
                         "z (m)":t["translation"]["z"],"Yaw (degrees)":math.degrees(t["yaw"])})
        st.table(rows)
        st.write("In the first row, translation describes the mounting offset. In the second, it describes "
                 "the sensor's location in the odometry reference. A snapshot does not establish how values change over time.")
    else:
        st.info("Select a live or reference snapshot for Part A. You can explore the remaining parts while preparing ROS.")
    answer(st,"frame_roles","In your own words, what do odom, base_link, and base_scan describe? Which relationship changes as the robot moves?")
    answer(st,"mounting","Cite one value from your selected snapshot. What does it tell you about the sensor's position or orientation, and why does software need it?")

    st.header("Part B: Interpret and transform a point")
    st.write("Use this fixed reference scene for the calculation, even if your live snapshot has different values. "
             "Robot: odom (1, 1) m, facing 90° toward +y. Target: odom (2, 1) m. "
             "The target stays still while we change the robot's heading.")
    heading=st.session_state.setdefault("m2.scene_heading",90)
    left,right=st.columns(2)
    with left:
        if st.button("View heading 90°"):
            st.session_state["m2.scene_heading"]=90
            set_response(st,"mission_2.seen90",True)
            st.rerun()
    with right:
        if st.button("View heading 0°"):
            st.session_state["m2.scene_heading"]=0
            set_response(st,"mission_2.seen0",True)
            st.rerun()
    set_response(st,"mission_2.compared",bool(response(st,"mission_2.seen90",False) and response(st,"mission_2.seen0",False)))
    visual(st,mode="frames",x=1.,y=1.,heading=heading)
    st.caption("Reference scene. The sensor mounting shown here is illustrative. Click both heading views to compare them.")
    st.markdown("**Calculate for heading 90°:** first subtract the robot position from the target position. "
                "Then rotate that displacement by the negative robot heading to describe it using the robot's axes.")
    st.latex(r"\begin{aligned}d_x&=x_t-x_r,&d_y&=y_t-y_r\\x_b&=\cos\theta\,d_x+\sin\theta\,d_y\\y_b&=-\sin\theta\,d_x+\cos\theta\,d_y\end{aligned}")
    st.write("Subscripts t, r, and b mean target, robot, and body frame. At 90°, cosine is 0 and sine is 1. "
             "A negative body y means right, not behind.")
    prior=response(st,"mission_2.point_answer",{})
    with st.form("m2.point_form"):
        x=st.number_input("Target x in base_link at heading 90° (m)",value=float(prior.get("x",0.)),step=.1)
        y=st.number_input("Target y in base_link at heading 90° (m)",value=float(prior.get("y",0.)),step=.1)
        if st.form_submit_button("Check my transformation"):
            set_response(st,"mission_2.point_answer",{"x":x,"y":y})
            attempts=list(response(st,"mission_2.point_attempts",[])); attempts.append({"x":x,"y":y})
            set_response(st,"mission_2.point_attempts",attempts)
    checked=response(st,"mission_2.point_answer",{})
    if checked:
        if correct_point(checked):
            st.success("The target is at base_link (0, -1) m: one meter to the right.")
        else:
            st.info("Use the worked steps below and revise your coordinates. Think about which side of the robot faces the target.")
        with st.expander("Worked transformation",expanded=not correct_point(checked)):
            st.latex(r"(d_x,d_y)=(2-1,1-1)=(1,0),\qquad (x_b,y_b)=(0\times1+1\times0,-1\times1+0\times0)=(0,-1)")
            st.write("At heading 0° the same target is (1, 0): directly ahead. With the illustrated sensor "
                     "0.20 m forward of base_link and aligned with it, the target in base_scan is (-0.20, -1). "
                     "Adding the mounting offset gives base_link (0, -1); rotating and translating gives odom (2, 1).")
    answer(st,"point_meaning","Explain what the target's (0, -1) coordinates mean in base_link at heading 90°. Why are these different from odom (2, 1)?")
    answer(st,"moving_coordinates","Compare the two heading views. Which target coordinates change, which stay the same, and why?")

    st.header("Part C: Diagnose a wrong-frame mistake")
    st.write("The robot is again at (1, 1), facing 90°. A program receives target coordinates odom (2, 1), "
             "but mistakenly treats them as a body-relative target: 2 m forward and 1 m left. "
             "This is a position-target interpretation, not a Twist velocity command.")
    if st.button("Show the wrong destination"):
        set_response(st,"mission_2.wrong_viewed",True)
    if response(st,"mission_2.wrong_viewed",False):
        visual(st,mode="frames",x=1.,y=1.,heading=90,show_wrong=True)
        st.write("The mistaken destination becomes odom (0, 3): from (1, 1), two meters forward goes toward "
                 "+y and one meter left goes toward -x. The intended target is (2, 1). The lines show destination "
                 "differences, not a planned or collision-checked robot trajectory.")
    answer(st,"wrong_source","Identify the source frame and required destination frame. What transform should the program apply before interpreting the target as robot-relative?")
    answer(st,"wrong_behavior","Where could the mistaken target send the robot? Explain the difference from the intended destination using the diagram.")

    st.header("Part D: Consequences and safeguards")
    st.write("Imagine a person standing near the mistaken destination. Consider what a robot following "
             "that target might do and how to catch the error before motion.")
    st.markdown("Possible checks include verifying frame IDs, using a transform valid for the measurement's "
                "timestamp, visualizing transformed targets, and testing known points. A stale transform is "
                "one that describes an earlier pose; it may be wrong for a moving robot. "
                "Speed limits can reduce consequences, but cannot prove coordinates are correct.")
    answer(st,"consequence","Describe one consequence of this frame mistake for someone near the robot.")
    answer(st,"safeguard","Specify one technical safeguard that would detect or prevent this mistake. What should the robot do if the transform is missing or invalid?")
    answer(st,"test_plan","Describe a test with a known input frame, robot pose, expected result, and pass condition. What would this test still not establish?")
    responses=st.session_state["responses"]
    check=evaluate(snapshot,responses); render_check(st,check)
    current_id=evidence_id({k:v for k,v in responses.items() if k.startswith("mission_2.")})
    if st.button("Check and save Mission 2",disabled=not check.passed,type="primary"):
        save_mission("mission_2",{"evidence_id":current_id,"snapshot":snapshot,
            "reference_scene":{"robot_odom":[1,1,90],"target_odom":[2,1],"units":"meters and degrees"},
            "live_verification_pending":snapshot["source"]!="live",
            "check":[item.__dict__ for item in check.requirements]},responses)
        complete_mission(st,"mission_2",current_id); st.rerun()
    if check.passed and st.session_state.get("checked_evidence_ids",{}).get("mission_2")==current_id:
        st.success("Mission 2 saved with your frame evidence, calculation, diagnosis, and safeguard.")
        if st.button("Continue to Mission 3",type="primary"):
            set_stage(st,"mission_3")
