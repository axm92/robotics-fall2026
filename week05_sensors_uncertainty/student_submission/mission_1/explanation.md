# Mission 1

## bias

-0.0141

## bias_vs_variance

From the statistics the sensor didn't really match either of the patterns I described cleanly. The bias was -0.0141m and that accounted for a small percentage of the total error and from that the sensor isn't consistently biased. Then the variance was 0.004307, but this was heavily impacted by the outlier reading of 1.1m. Without the outlier the variance would drop. Bias and variance described different failures because bias measures how far the center of the readings are in comparison to the true value, while variance measures how widely the readings spread around their own center. 

## dropouts

6

## mean

1.9859

## median

2.0

## more_samples

I don't think that more samples would remove the senor's main problem because the main problem is that it sometimes produces outliers. If we were to have 2x the number of readings the standard error of the mean would likely decrease however as we see throughout our readings the outlier is a property of the sensor and not a result of not having enough readings. There was only 1 reading within 234 valid readings was off by 0.9m, and that single reading produced 78.5% if the variance. If the outliers would keep occurring at the current rate, each one will still pull the average down by about 0.004m (0.9*0.0043). 

## outliers

1

## prediction

A consistently biased sensor would go in the same direction and follow a consistent path every time, so the readings would cluster together around a single point that is displaced form 2.0m. The average reading would then differ noticeably from the 2.0m, the bias would be nonzero, and the variance would be small. Whereas a noisy sensor is a lot more unpredictable so there would be a lot of errors, and they'd most likely cancel out. The average reading would sit close to 2.0m, the bias would be near 0, and the variance would be pretty big, producing a wide spread of values. I would use these relationships between these values to determine if it is consistently biased or not.

## prediction_draft

A consistently biased sensor would go in the same direction and follow a consistent path every time, so the readings would cluster together around a single point that is displaced from 2.0m. The average reading would then differ noticeably from the 2.0m, the bias would be nonzero, and the variance would be small. Whereas a noisy sensor is a lot more unpredictable so there would be a lot of errors, and they'd most likely cancel out. The average reading would sit close to 2.0m, the bias would be near 0, and the variance would be pretty big, producing a wide spread of values. I would use these relationships between these values to determine if it is consistently biased or not. 

## profile

quantized

## robot_consequence

This could be a garbage robot that roams around a campus where there is a lot of heavy foot traffic, and it is programmed to stop when trash or a person/obstacle is detected closer than 1.5m or so. Majority of the readings will be accurate but that 1 in 234 chance is still a problem if that robot acts on that reading. It would view an object closer than it actually is and stop abruptly and this could cause delay in people walking around on the campus, and it could harm a person or the robot itself. 

## variance

0.004307
