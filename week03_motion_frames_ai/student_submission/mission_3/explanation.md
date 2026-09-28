# Mission 3

## Ai Disclosure

I used Claude ai as my ai assistant for this mission. I used it to verify my specification which caught an error I made with mistaking the 60 second limit for a target instead of the cap/ceiling. I also used it to generate an initial build_pattern implementation, and then had it explain what I wasn't familiar with, which was most of it to be honest. I also got assistance for proposing test cases and figuring out what errors were lying within the program when it wasn't running as it should. I had changed some of the lines of code that they had given me, like the ones where there was a full stop after every turn and that added to the segment count, which was not what our checks.py file was looking for. After making necessary changes I pasted in the new code to verify that it was good and would work as intended. I also used it at times to help me word some of the responses because a few of them I didn't know how to respond in a meaningful and accurate way. 

## Assigned Pattern

alternating_arcs

## Assumptions

The AI made several assumptions that weren't explicitly stated in the prompt but we necessary to produce working code. On units, it assumed linear_x is in m/s, angular_z is in rad/s and duration is in seconds, which matches the assignments stated units but it never actually verified against the actual segment class definition. On motion, it assumed a purely kinematic relationship where radius equals linear speed divided by angular speed remains steady with no acceleration ramp-up, wheel slip, or even control delay, meaning its expecting each segment to hold its commanded velocity for the full duration, which is very idealistic. In terms of timing it assumed pattern_node.py executes segments strictly in sequence, holding each velocity for exactly its stated duration before moving on to the next, without seeing the files actual implementation. 

## Evidence Analysis

The important tests established that everything was working as it was intended and expected to. For example, the tests for angular and linear limits were there to confirm that every segment's angular and linear speed stays within the 0.8 rad/s and 0.22 m/s limits. We can see that these worked from the true output with "commands_bounded" in the JSON output. Some of the points that were reflecting this is at the first checkpoint where the expected pose was (0.212, 0.088, theta=0.785 rad) and the observed pose was (0.187, 0.074, theta= 0.721 rad). There was a position error of 0.0287 m and a heading error of 0.0647 rad, which are both with the tolerances of 0.15 m /0.2 rad. However, these tests don't establish the same behavior under different conditions like starting poses, added sensor noise, a different simulated surface, or even on physical hardware. It is specific to the simulated environment it was written for. For this I would probably create another test where we change the conditions of the environment. 

## Live Pending

False

## Modifications

1: The radius is explicitly derived by |v/w| and no longer guessed. The linear speed being 0.15 and angular speed being 0.5 is so that we get R as 0.30, which matches the radius exactly and we don't have to pick a linear speed and then figure out what angular speed afterwards. This gets checked with the arc-radius test.

2: The turn duration is no longer hardcoded and is calculated by the turn angle/ angular speed. This makes the relationship between angle, angular speed, and duration explicit and consistent. If I ever change angular speed, the duration would still be correct.

3: So, before there were stop segments after every arc, including the last one and expecting 7-segments to be the total. This is simply not what the checks.py file was looking for and that gave it more actions/instructions than necessary. So, I adjusted the code to better reflect what the tests would be looking for. 

## Original Output

Assumptions:

Segment is a simple existing data class/namedtuple with fields linear_x, angular_z, duration (matching the parameter names given), and doesn't need to be redefined — only imported/used.
pattern_node.py handles actually publishing each segment for its duration in sequence and sending a final zero-velocity command itself — build_pattern only needs to return the list, not do any publishing, timing, or sleeping itself.
"Brief stop between arcs" means inserting an explicit zero-velocity Segment (linear_x=0, angular_z=0) with a short duration between each arc segment, since the wrapper just plays back whatever list it's given — a stop has to be a real segment in the list, not implied.
Positive angular_z = left turn, matching the body-frame convention given (+x forward, positive turning left), so the four arcs are +0.5, -0.5, +0.5, -0.5 rad/s in that order.
Since build_pattern takes a generic pattern_name, other pattern names may be added later by other students/tests — this implementation only owns the 'alternating_arcs' branch and raises ValueError for anything else, without assuming it's the only pattern this function will ever need to support.
Short stop duration: using 0.2 s as a small, safe pause — long enough to let velocity settle physically, short enough not to meaningfully affect the ~6.3 s total motion budget or approach the 60 s ceiling.
python
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

Sanity check against limits:

linear_speed = 0.15 ≤ 0.22 ✓
angular_speed = 0.5 ≤ 0.80 ✓
Each arc segment duration ≈ 1.5708 s, each stop = 0.2 s — all ≤ 30 s ✓
Total: 4 × 1.5708 + 3 × 0.2 ≈ 6.88 s, well under 60 s ✓
Radius check: linear_speed / angular_speed = 0.15 / 0.5 = 0.3 m ✓ matches spec exactly
Arc length per segment: radius × angle = 0.3 × (π/4) ≈ 0.2356 m ✓ matches "~0.24 m"

Proposed tests (mirroring the style of the Mission 2 test file, so they'd fit naturally alongside course-provided tests):

test_unknown_pattern_raises_value_error — call build_pattern('not_a_real_pattern') and assert it raises ValueError.
test_returns_four_arc_segments_with_correct_signs — filter the returned list for non-zero angular_z segments, assert there are exactly 4, and assert their signs are [+, -, +, -].
test_arc_speeds_within_limits — assert every segment's linear_x <= 0.22 and abs(angular_z) <= 0.80.
test_arc_radius_matches_spec — for each arc segment, assert abs(linear_x / angular_z) ≈ 0.30 within 0.02 m (skip/guard zero-angular_z stop segments to avoid division by zero).
test_arc_duration_matches_45_degrees — for each arc segment, assert abs(angular_z) * duration ≈ math.pi/4 within 0.04 rad.
test_all_durations_positive_and_bounded — assert every segment's duration > 0 and <= 30.
test_total_duration_under_60_seconds — sum all segment durations and assert the total is <= 60.
test_net_heading_change_is_zero — sum angular_z * duration across all segments and assert it's approximately 0 within tolerance (confirms the four turns cancel out).
test_no_stop_segment_appended_after_final_arc — assert the last segment in the returned list is an arc (non-zero angular_z), not an explicit stop, since pattern_node.py is responsible for the final zero command.

## Original Prompt

The robot should drive four connected arcs, consecutively with brief stops in between them. Each arc will have a radius of 0.3m and at first the robot will curve left 45 degrees, then right 45 degrees, then left the same amount, and finally right again the same amount. The value of 45 will be alternating between negative and positive depending on turn direction. With the lefts and rights being equal in number of times and degrees, they will cancel each other out and the robot will end up facing the same direction that it started in but just in a different position. In terms of speed I will drive at 0.15m/s forward and then to get a 0.3m radius I will need an angular speed of 0.5rad/s because 0.15/0.3 = 0.5. Both of these values are under the limits. After each arc finishes, the robot briefly stops before it will continue on to the next arc, so that the turns don't blend messily. After the final arc the robot will stop completely and stay stopped. To check that this was executed correctly they must check if each arc was about 0.24m long, and each turn should be 45 degrees or +-0.04 rad, and the arc's radius should be 0.3m. By the end the robot should match it's start heading, or at least close to. Overall it should happen in under 60 seconds.                  This is a ROS 2 Jazzy Python package. Implement only build_pattern(pattern_name: str) -> list[Segment] for 'alternating_arcs' in the existing pattern.py.
The course-provided pattern_node.py calls this function, publishes the returned segments repeatedly through /student_cmd_vel, and sends the final zero command.
Use the existing Segment class with linear_x (m/s), angular_z (rad/s), and duration (s).
Return the ordered segments for the assigned specification and raise ValueError for an unknown pattern name.
Stay within 0.22 m/s, 0.80 rad/s, 30 seconds per segment, and 60 seconds total.
Do not replace the wrapper or course checks. Explain assumptions and propose tests.

## Original Source

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

## Problems

The segment class constructor call assumes keyword arguments name exactly linear_x, angular_z, and duration, but the code doesn't inspect the real class definition. So if the class uses different names or positional arguments it would fail immediately. Therefore I need to actually check the class to make sure all the names are matching up and avoid any errors in that space. Secondly, the import statement was never written, its just assuming that it exists everywhere. 

## Saved Specification

The robot should drive four connected arcs, consecutively with brief stops in between them. Each arc will have a radius of 0.3m and at first the robot will curve left 45 degrees, then right 45 degrees, then left the same amount, and finally right again the same amount. The value of 45 will be alternating between negative and positive depending on turn direction. With the lefts and rights being equal in number of times and degrees, they will cancel each other out and the robot will end up facing the same direction that it started in but just in a different position. 
In terms of speed I will drive at 0.15m/s forward and then to get a 0.3m radius I will need an angular speed of 0.5rad/s because 0.15/0.3 = 0.5. Both of these values are under the limits. 
After each arc finishes, the robot briefly stops before it will continue on to the next arc, so that the turns don't blend messily. After the final arc the robot will stop completely and stay stopped. To check that this was executed correctly they must check if each arc was about 0.24m long, and each turn should be 45 degrees or +-0.04 rad, and the arc's radius should be 0.3m. By the end the robot should match it's start heading, or at least close to. Overall it should happen in under 60 seconds. 

## Specification

The robot should drive four connected arcs, consecutively with brief stops in between them. Each arc will have a radius of 0.3m and at first the robot will curve left 45 degrees, then right 45 degrees, then left the same amount, and finally right again the same amount. The value of 45 will be alternating between negative and positive depending on turn direction. With the lefts and rights being equal in number of times and degrees, they will cancel each other out and the robot will end up facing the same direction that it started in but just in a different position. 
In terms of speed I will drive at 0.15m/s forward and then to get a 0.3m radius I will need an angular speed of 0.5rad/s because 0.15/0.3 = 0.5. Both of these values are under the limits. 
After each arc finishes, the robot briefly stops before it will continue on to the next arc, so that the turns don't blend messily. After the final arc the robot will stop completely and stay stopped. To check that this was executed correctly they must check if each arc was about 0.24m long, and each turn should be 45 degrees or +-0.04 rad, and the arc's radius should be 0.3m. By the end the robot should match it's start heading, or at least close to. Overall it should happen in under 60 seconds. 

## Test Plan

The pattern behavior test checks that build_pattern('alternating_arcs') actually returns segments in the correct order with the correct alternating directions, and that when passing an unrecognized pattern name, it will raise an error instead of failing silently or crashing unpredictably. I am expecting the returned list to contain 4 segments with non-zero angular velocity, with alternating signs going +-+-, and for each of these segments to have a linear speed of 0.15 m/s. 

The velocity limit test checks that every segment in the returned list respects the assignments hard limits. So, the linear speed can't exceed 0.22 m/s, angular can't exceed 0.8 rad/s and so on. I expect all the checks to pass because each value sits comfortably under its max. 

The stop test checks that zero-velocity stop segments actually appear between each arc rather than them blending into one another. I expect the segments at the positions between arcs to have both linear and angular velocity at 0, exactly 0.  
