# AWS DeepRacer Reward Function

I participated in the Kumo Torakku contest of DeepRacer Virtual Circuit.
It is a reward function at that time.
The lap time was about 25 seconds after repeated training.

## Environment simulation

- Kumo Torakku Training

## Action space

| Action space                 | Value       |
|------------------------------|-------------|
| Maximum steering angle       | 30 degrees  |
| Steering angle granularity   | 7           |
| Maximum speed                | 1 m/s       |
| Speed granularity            | 3           |

## Hyperparameters

| Hyperparameters                                                | Value           |
|----------------------------------------------------------------|-----------------|
| Gradient Descent Batch Size                                    | 64              |
| Entropy                                                        | 0.01            |
| Discount Factor                                                | 0.999           |
| Loss Type                                                      | Huber           |
| Learning Rate                                                  | 0.0003 or 0.001 |
| No# Experience Episodes between each policy-updating iteration | 20              |
| No# of Epochs                                                  | 3 or 10         |

## Stop conditions

- 60 or 120 mins

## Reference

- https://forums.aws.amazon.com/forum.jspa?forumID=318
- https://github.com/aws-samples/aws-deepracer-workshops
- https://github.com/sasasavic82/deeracer-reward
- https://qiita.com/kai_kou/items/8a45c687baca8c9465f6
- https://qiita.com/Alt_Shift_N/items/2c37fbb26d739b7f3046
