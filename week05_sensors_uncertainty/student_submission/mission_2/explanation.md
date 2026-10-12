# Mission 2

## comparison

For the moving average at weight 0.25, increasing the window from 3 to 7 and then 11 raised the RMSE from 0.1395 to 0.1504 to 0.1601, this is a 14.8% increase overall and raised the maximum error from 1.1254 to 1.2064, while the MAE stayed nearly the same, and the response delay didn't change at all. Here we can see that longer windows made the overall and worst-case error worse without improving typical error or response. For the matched pair at window and weight 0.25, the median had slightly better typical error than the moving average, but a larger maximum error by about 13%, and the delay was the same. Neither filter was clearly better than the other. 

## fusion_choice

Comparing 3 fusion weights using the median filter with a window of 3 we can see that a weight of 0.25 on sensor A had RMSE as 0.1389 and the delay 1.1. A weight of 0.5, the RMSE dropped to 0.1270 and the delay to 0.9. At 0.75, the RMSE was 0.1335 and the delay was just 0.45, but the maximum error climbed to 1.6049. The weight of 0.50 would be the one that I choose because it has the lowest RMSE and responded noticeably faster than 0.25, and its only real costs were a slightly higher MAE and a larger maximum error. This choice fits what we know about the sensors since A is fast but noisy and outlier prone more weight sped up the response but led to bad readings, which is why the max error climbed with each increase. Sensor B is steadier but biased and only samples every fourth time step, so giving it more weight kept the output calmer but slower, since the estimate sits on an old value between B's updates, and B's bias carried into the result. A weight of 0.25 leaned too much on B's slowness and bias, while 0.75 leaned too much on A's outliers. An even split let each sensor offset the other's weakness. 

## manual_average

4.1667

## manual_fusion

2.25

## manual_median

2.3

## prediction_draft

The delay here would be in the middle in comparison to the rest of the configurations, slower than with a window of 3, but faster than a window of 11. The outlier effect here would be smaller but lasts for a longer period. 

## responsiveness

The measured delays show that window size did not affect responsiveness. All the windows had a delay of 1.1, but the weight changed it. For the weight of 0.25 it was 1.1, 0.50 was 0.9, and 0.75 was 0.45. The cost of heavier smoothing appeared in the error instead, as the higher RMSE and maximum error at larger windows. This differs from the expected pattern that longer windows add lag, so the delay metric could be influenced heavily by something other than the filter, like the slower response of the other sensor. For a nearby person, delay is very important because if there is a significant delay within how a robot perceives a new reading that robot could be directly in the path of a person and most likely run into them. 

## selected

6
