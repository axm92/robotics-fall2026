# Mission 3

## Assistive.prediction_draft

This revised policy will lower detection delay and reduce unnecessary stops compared with the baseline, without increasing false safe events. By giving sensor A more weight it should speed up the estimate's reaction to a sudden-step in. The median should still filter most of A's single outliers, though a higher weight could let through some error if two bad readings fall in one window. Replacing STOP with INSUFFICIENT on missing data keeps the robot from moving, so it stays as safe as the baseline. 


## Warehouse.prediction_draft

For this policy, I believe that it will lower the detection delay and reduce false safe and dangerous command events compared to the baseline. By giving sensor A more weight it should make the estimate react faster to a sudden obstacle. Just how delay fell in mission 2 when the weight increased. The larger margin moves the STOP zone further out to 0.95m, so the robot should stop earlier in a slow approach and hold STOP more reliably when the truth hovers near the 0.75m boundary. 

## context_comparison

The two final policies differ in the stopping threshold and the missing data rule. The assistive policy uses a threshold of 0.95 m instead of 0.75 m, which moves its STOP zone out to 1.15 m instead of 0.95 m, so it stops 0.20 m earlier. That extra distance gives a person with limited mobility more time and space, and the assistive robot had a 0% false safe rate. The second difference is the missing-data rule where the warehouse robot stops when both readings are missing, and it had a 5.61% unnecessary-stop rate, while the assistive robot abstains with Insufficient and had 0%. For a warehouse worker, that means occasional pauses in work, but for an assistive user it avoids repeated hard stops that wear down trust.


## error_costs

In the warehouse, the cost of a false-safe event falls on workers near the aisle and on the equipment owner, through injury risk and damage, while an unnecessary-stop mainly affects operators and coworkers waiting on work that is delayed. In the assistive setting, both errors fall on the same person. A false-safe MOVE can injure someone with limited mobility, and repeated unnecessary stops reduce their access and trust. 

In the warehouse, changing the margin from 0.1 to 0.2 m and the weight from 0.35 to 0.5 left the false-safe rate at 0.62% and the unnecessary-stop rate at 5.61%, and only cut the maximum detection delay from 0.1 s to 0 s. In the assistive setting, raising the weight to 0.5 and switching from Stop to Insufficient kept the false-safe rate at 0% and dropped the unnecessary-stop rate from 1.35% to 0%, with delay falling from 0.05 s to 0 s. From this we can see that neither policy produced a dangerous command event. 

## limitations

These seven tests establish how each policy behaves in scripted scenarios with simulated sensors and show that under certain conditions the policies can produce no dangerous command events or no false-safe or unnecessary-stop events. However, they do not establish real world safety. A stakeholder to consult here would be people with accessibility needs like those in a wheelchair. They would know what a safe approach is and what repeated stops does and how it affects others. An additional test that could be ran is a long dropout burst that begins while a person is approaching, because Insufficient and Stop have only been tested on short gaps.
