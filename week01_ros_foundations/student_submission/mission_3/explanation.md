# Mission 3

## Data To Command

front_distance() gets a bunch of readings that cover multiple directions but then narrows them down to ones that are in the front and have valid values, then picks the closest one. Decide_velocity uses that closest number and applies rules to it so it knows when to stop or continue moving.

## Missing Data Safety

This is because it is the safest and most reasonable option. No valid front measurement doesn't mean all clear so if we assume the path is clear that could be problematic because there is a high chance it is not clear. We can't treat the unknown like all clear because that is not the most careful option.

## System Layers

The decision functions, the ROS node and command guard form a layered pipeline, where each piece is responsible for different parts of safety logic. The ROS node handles the ROS-specific tasks, like subscribing to /scan. It recieves raw LiDAR data and then publishes the result to ..cmd_vel. Every new scan the node with call the 2 functions in their respective sequence. frontD_distance() reduces the LiDAR ranges down to the closest valid obstacle that is directly ahead. Then that number gets converted into a forward speed with limits. The functions don't know anything about the ROS itself, they are just funtions who take in values and returns one singular value. The command guard is the safety check for messages that get published to cmd_vel. It can override or stop the robot if something is not right. 
