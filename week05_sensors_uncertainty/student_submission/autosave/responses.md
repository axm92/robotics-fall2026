# Week 5: Sensors, Noise, and Uncertainty

- course_id: CSCI 39536
- email: amaya.mangual74@login.cuny.edu
- name: Amaya Mangual

## concepts.observation

When I increased the noise there was a lot more commotion shown in both graphs. The distances that were lower before increased and there were fewer noticeably high spikes in distance. The distribution graph had more distance bars as well, within the 1.5 to 2.5 range. When looking at the statistics below I can see that the mean had a very slight increase, there was more variance, and the bias also increased while the rest of the values remained the same. 

When I increased the bias majority of the points in the measurement sequence graph were above the 2.0m line and in the other graph majority of the bars with significant data were to the right of the 2.0m line. The mean and median both increased slightly but the rest of the values remained the same. 

## final.course_reflection



## final.synthesis



## mission_1.bias

-0.0141

## mission_1.bias_vs_variance

From the statistics the sensor didn't really match either of the patterns I described cleanly. The bias was -0.0141m and that accounted for a small percentage of the total error and from that the sensor isn't consistently biased. Then the variance was 0.004307, but this was heavily impacted by the outlier reading of 1.1m. Without the outlier the variance would drop. Bias and variance described different failures because bias measures how far the center of the readings are in comparison to the true value, while variance measures how widely the readings spread around their own center. 

## mission_1.dropouts

6

## mission_1.mean

1.9859

## mission_1.median

2.0

## mission_1.more_samples

I don't think that more samples would remove the senor's main problem because the main problem is that it sometimes produces outliers. If we were to have 2x the number of readings the standard error of the mean would likely decrease however as we see throughout our readings the outlier is a property of the sensor and not a result of not having enough readings. There was only 1 reading within 234 valid readings was off by 0.9m, and that single reading produced 78.5% if the variance. If the outliers would keep occurring at the current rate, each one will still pull the average down by about 0.004m (0.9*0.0043). 

## mission_1.outliers

1

## mission_1.prediction

A consistently biased sensor would go in the same direction and follow a consistent path every time, so the readings would cluster together around a single point that is displaced form 2.0m. The average reading would then differ noticeably from the 2.0m, the bias would be nonzero, and the variance would be small. Whereas a noisy sensor is a lot more unpredictable so there would be a lot of errors, and they'd most likely cancel out. The average reading would sit close to 2.0m, the bias would be near 0, and the variance would be pretty big, producing a wide spread of values. I would use these relationships between these values to determine if it is consistently biased or not.

## mission_1.prediction_draft

A consistently biased sensor would go in the same direction and follow a consistent path every time, so the readings would cluster together around a single point that is displaced from 2.0m. The average reading would then differ noticeably from the 2.0m, the bias would be nonzero, and the variance would be small. Whereas a noisy sensor is a lot more unpredictable so there would be a lot of errors, and they'd most likely cancel out. The average reading would sit close to 2.0m, the bias would be near 0, and the variance would be pretty big, producing a wide spread of values. I would use these relationships between these values to determine if it is consistently biased or not. 

## mission_1.profile

quantized

## mission_1.robot_consequence

This could be a garbage robot that roams around a campus where there is a lot of heavy foot traffic, and it is programmed to stop when trash or a person/obstacle is detected closer than 1.5m or so. Majority of the readings will be accurate but that 1 in 234 chance is still a problem if that robot acts on that reading. It would view an object closer than it actually is and stop abruptly and this could cause delay in people walking around on the campus, and it could harm a person or the robot itself. 

## mission_1.variance

0.004307

## mission_2.comparison

For the moving average at weight 0.25, increasing the window from 3 to 7 and then 11 raised the RMSE from 0.1395 to 0.1504 to 0.1601, this is a 14.8% increase overall and raised the maximum error from 1.1254 to 1.2064, while the MAE stayed nearly the same, and the response delay didn't change at all. Here we can see that longer windows made the overall and worst-case error worse without improving typical error or response. For the matched pair at window and weight 0.25, the median had slightly better typical error than the moving average, but a larger maximum error by about 13%, and the delay was the same. Neither filter was clearly better than the other. 

## mission_2.fusion_choice

Comparing 3 fusion weights using the median filter with a window of 3 we can see that a weight of 0.25 on sensor A had RMSE as 0.1389 and the delay 1.1. A weight of 0.5, the RMSE dropped to 0.1270 and the delay to 0.9. At 0.75, the RMSE was 0.1335 and the delay was just 0.45, but the maximum error climbed to 1.6049. The weight of 0.50 would be the one that I choose because it has the lowest RMSE and responded noticeably faster than 0.25, and its only real costs were a slightly higher MAE and a larger maximum error. This choice fits what we know about the sensors since A is fast but noisy and outlier prone more weight sped up the response but led to bad readings, which is why the max error climbed with each increase. Sensor B is steadier but biased and only samples every fourth time step, so giving it more weight kept the output calmer but slower, since the estimate sits on an old value between B's updates, and B's bias carried into the result. A weight of 0.25 leaned too much on B's slowness and bias, while 0.75 leaned too much on A's outliers. An even split let each sensor offset the other's weakness. 

## mission_2.manual_average

4.1667

## mission_2.manual_fusion

2.25

## mission_2.manual_median

2.3

## mission_2.prediction_draft

The delay here would be in the middle in comparison to the rest of the configurations, slower than with a window of 3, but faster than a window of 11. The outlier effect here would be smaller but lasts for a longer period. 

## mission_2.responsiveness

The measured delays show that window size did not affect responsiveness. All the windows had a delay of 1.1, but the weight changed it. For the weight of 0.25 it was 1.1, 0.50 was 0.9, and 0.75 was 0.45. The cost of heavier smoothing appeared in the error instead, as the higher RMSE and maximum error at larger windows. This differs from the expected pattern that longer windows add lag, so the delay metric could be influenced heavily by something other than the filter, like the slower response of the other sensor. For a nearby person, delay is very important because if there is a significant delay within how a robot perceives a new reading that robot could be directly in the path of a person and most likely run into them. 

## mission_2.selected

6

## mission_3.Assistive.prediction_draft

This revised policy will lower detection delay and reduce unnecessary stops compared with the baseline, without increasing false safe events. By giving sensor A more weight it should speed up the estimate's reaction to a sudden-step in. The median should still filter most of A's single outliers, though a higher weight could let through some error if two bad readings fall in one window. Replacing STOP with INSUFFICIENT on missing data keeps the robot from moving, so it stays as safe as the baseline. 


## mission_3.Warehouse.prediction_draft

For this policy, I believe that it will lower the detection delay and reduce false safe and dangerous command events compared to the baseline. By giving sensor A more weight it should make the estimate react faster to a sudden obstacle. Just how delay fell in mission 2 when the weight increased. The larger margin moves the STOP zone further out to 0.95m, so the robot should stop earlier in a slow approach and hold STOP more reliably when the truth hovers near the 0.75m boundary. 

## mission_3.context_comparison

The two final policies differ in the stopping threshold and the missing data rule. The assistive policy uses a threshold of 0.95 m instead of 0.75 m, which moves its STOP zone out to 1.15 m instead of 0.95 m, so it stops 0.20 m earlier. That extra distance gives a person with limited mobility more time and space, and the assistive robot had a 0% false safe rate. The second difference is the missing-data rule where the warehouse robot stops when both readings are missing, and it had a 5.61% unnecessary-stop rate, while the assistive robot abstains with Insufficient and had 0%. For a warehouse worker, that means occasional pauses in work, but for an assistive user it avoids repeated hard stops that wear down trust.


## mission_3.error_costs

In the warehouse, the cost of a false-safe event falls on workers near the aisle and on the equipment owner, through injury risk and damage, while an unnecessary-stop mainly affects operators and coworkers waiting on work that is delayed. In the assistive setting, both errors fall on the same person. A false-safe MOVE can injure someone with limited mobility, and repeated unnecessary stops reduce their access and trust. 

In the warehouse, changing the margin from 0.1 to 0.2 m and the weight from 0.35 to 0.5 left the false-safe rate at 0.62% and the unnecessary-stop rate at 5.61%, and only cut the maximum detection delay from 0.1 s to 0 s. In the assistive setting, raising the weight to 0.5 and switching from Stop to Insufficient kept the false-safe rate at 0% and dropped the unnecessary-stop rate from 1.35% to 0%, with delay falling from 0.05 s to 0 s. From this we can see that neither policy produced a dangerous command event. 

## mission_3.limitations

These seven tests establish how each policy behaves in scripted scenarios with simulated sensors and show that under certain conditions the policies can produce no dangerous command events or no false-safe or unnecessary-stop events. However, they do not establish real world safety. A stakeholder to consult here would be people with accessibility needs like those in a wheelchair. They would know what a safe approach is and what repeated stops does and how it affects others. An additional test that could be ran is a long dropout burst that begins while a person is approaching, because Insufficient and Stop have only been tested on short gaps.
