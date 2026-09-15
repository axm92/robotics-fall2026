# Mission 2

## Measurement Explanation

The estimated amount is great than the start-to-end amount in both trials because they both are measuring similar but different things. The estimated path or arc length is measuring the distance the robot moved along its curved path while the start-to-end is measuring the distance from the start to end using a straight line. So the straight line would be like the hypotenuse of a right triangle and then the estimated is the base + height, which is greater than the hypotenuse.

## Modified Settings

{'linear_x': 0.12, 'angular_z': 0.6, 'duration': 4.0}

## Motion Comparison

The rotation trial results validated my hypothesis. The start to end distance is 0m meaning it didn't travel anywhere. Then the direction change was 73.9 degrees, meaning it turned to the right and was not facing the right. Both of these were in my prediction.

## Prediction Locks

{'curve': '2026-09-14T00:45:47.610789+00:00', 'curve_modified': '2026-09-14T00:58:05.677333+00:00', 'rotation': '2026-09-13T04:15:37.702557+00:00', 'straight': '2026-09-13T03:23:54.200456+00:00'}

## Predictions

{'curve': 'I predict that it will have a very short straight path that curves gradually to the right. Like the turn right symbol when driving. \n', 'curve_modified': 'This curve would be tighter because the angular velocity would be faster in relation to the speed, which would make a tighter curve.', 'rotation': "I predict that its physical position won't change, while its direction will and it will now face the left. ", 'straight': 'I predict the robot will finish 0.45m straight forward from its starting position.\n\n'}

## Safety Explanation

The command guard checks the commands given to the robot before it actually makes it to the robot so that it is safe. The final zero command lets the robot know that this is the final command/end of a trial by making it no longer move forward or turn. The timeout is needed is a program doesn't work properly or communication with the robot is lost while it is in motion.
