# mission_3 Submission

- Name: Amaya Mangual
- Section: (not provided)

## Explanations

### technical_analysis

My prediction was that going faster or using too little Kd would make the robot's path error bigger and leave less room around the pedestrians. My run only partly matched that. At 0.40 m/s with Kd = 0.55, the robot reached 4/4 waypoints with a mean path error of 0.02 m and a max of 0.07 m. The green path stayed close to my blue route on the straight parts and only drifted off by rounding the corners near WP1 and WP3. I did not see the back and forth weaving I expected, so I think Kd = 0.55 is enough damping at this speed. The closest the robot got to a person was 0.35 m, and the corner rounding is what used up that space.

To get from the route to a heading command, the robot uses its estimated position to find the angle that points at the next route point. The difference between that angle and the way the robot is currently facing is the heading error. When the robot switches to the next waypoint, that error jumps by about 90 degrees, so the robot turns while still moving forward, which makes the rounded corners. The PID turns the error into steering. Kp reacts in proportion to the error, so it turns fast but can overshoot if it is too high. Ki builds up over time to remove a steady bias. Kd slows the turn as the heading gets close to the target, which stops the overshoot and weaving.

A wrong wheel radius can still make a well-tuned controller follow the wrong path because the controller only steers the estimated position, and that estimate comes from the wheel radius times how much the wheels turned. If the radius is off, the robot thinks it traveled farther or turned more than it really did. The PID can make the estimated path look perfect while the real path is stretched or angled wrong, and it could end up inside a pedestrian's safety zone. Changing Kp, Ki, or Kd cannot fix that because the mistake is in the measurement. In my run the orange estimate and green path matched, so the 51.0 mm radius looked good enough to trust the results.

### human_centered_analysis

The most serious failure for a pedestrian is a wrong odometry estimate that nobody notices. If the wheel radius is off, the robot still looks like it is following the route correctly, but its real path is shifted and could go into a pedestrian's safety zone. Weaving from low Kd is easy to see and fix, but a calibration error is silent, so the robot is confident and wrong and the person gets no warning.

For my trade-off, I would keep the speed at 0.40 m/s instead of raising it. A faster robot cuts corners wider and takes longer to stop, and my closest approach was only 0.35 m, so I do not have much space to give up. I would also route the robot farther from pedestrians than the minimum, so a small calibration or heading error still leaves a safe gap. I would accept a slower trip in exchange for a bigger safety buffer, because getting there a little faster is not worth risking someone getting hit.

Verifying this is a human job, because the robot cannot check its own safety when it only sees its estimated position. The engineers who tune the robot are responsible for calibrating the odometry and testing different pedestrian positions, not just one route that passed. A second person, like a safety lead, should review the results and sign off, since the person who tuned it is the most likely to miss problems. The organization that deploys the robot is responsible for the final decision and for adding a backup, like a distance sensor or emergency stop, that does not depend on odometry. One passing run is evidence, but it is not proof the robot is safe.