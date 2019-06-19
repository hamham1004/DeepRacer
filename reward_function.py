def reward_function(params):
    '''
    In @params object:
    {
        "all_wheels_on_track": Boolean,    # flag to indicate if the vehicle is on the track
        "x": float,                        # vehicle's x-coordinate in meters
        "y": float,                        # vehicle's y-coordinate in meters
        "distance_from_center": float,     # distance in meters from the track center 
        "is_left_of_center": Boolean,      # Flag to indicate if the vehicle is on the left side to the track center or not. 
        "heading": float,                  # vehicle's yaw in degrees
        "progress": float,                 # percentage of track completed
        "steps": int,                      # number steps completed
        "speed": float,                    # vehicle's speed in meters per second (m/s)
        "streering_angle": float,          # vehicle's steering angle in degrees
        "track_width": float,              # width of the track
        "waypoints": [[float, float], a?| ], # list of [x,y] as milestones along the track center
        "closest_waypoints": [int, int]    # indices of the two nearest waypoints.
    }
    '''

    import math

    # Constants
    INITIAL_REWARD = 1.0
    MIN_REWARD = 0.001
    DIRECTION_THRESHOLD = 10.0
    ABS_STEERING_THRESHOLD = 30

    # Input parameters
    on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    keep_left = params['is_left_of_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle for calculations
    speed = params['speed']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints'] 
    heading = params['heading']
    progress = params['progress']

    # negative exponential penalty
    reward = math.exp(-6 * distance_from_center)

    # Reward functions
    def on_track_reward(current_reward, on_track):
        if not on_track:
            current_reward = MIN_REWARD
        else:
            current_reward = INITIAL_REWARD
        return current_reward

    def distance_from_center_reward(current_reward, track_width, distance_from_center):
        # Calculate 4 marks that are farther and father away from the center line
        marker_1 = 0.1 * track_width
        marker_2 = 0.25 * track_width
        marker_3 = 0.5 * track_width

        # Give higher reward if the car is closer to center line and vice versa
        if distance_from_center <= marker_1:
            current_reward *= 1.2
        elif distance_from_center <= marker_2:
            current_reward *= 0.8
        elif distance_from_center <= marker_3:
            current_reward *= 0.5
        else:
            current_reward = MIN_REWARD  # likely crashed/ close to off track
        return current_reward

    def straight_line_reward(current_reward, steering, speed):
        # Positive reward if the car is in a straight line going fast
        if abs(steering) < 0.1 and speed > 6:
            current_reward *= 1.5
        elif abs(steering) < 0.2 and speed > 5:
            current_reward *= 1.2
        return current_reward

    def direction_reward(current_reward, waypoints, closest_waypoints, heading):

        '''
        Calculate the direction of the center line based on the closest waypoints    
        '''

        next_point = waypoints[closest_waypoints[1]]
        prev_point = waypoints[closest_waypoints[0]]

        # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
        direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
        # Convert to degrees
        direction = math.degrees(direction)

        # Cacluate difference between track direction and car heading angle
        direction_diff = abs(direction - heading)

        # Penalize if the difference is too large
        if direction_diff > DIRECTION_THRESHOLD:
            current_reward *= 0.75

        return current_reward

    def steering_reward(current_reward, steering):
        # Penalize reward if the car is steering too much (your action space will matter)
        if abs(steering) > ABS_STEERING_THRESHOLD:
            current_reward *= 0.9
        return current_reward

    def throttle_reward(current_reward, speed, steering):
        # Decrease throttle while steering
        if speed > 3.0 - (0.4 * abs(steering)):
            current_reward *= 0.8
        return current_reward
        
    def keep_left_reward(current_reward, keep_left):
        if keep_left:
            current_reward *= 1.2
        else:
            current_reward *= 0.9
        return current_reward

    def progress_reward(current_reward, progress):
        if progress > 75:
            current_reward *= 1.1
        return current_reward
        
    def speed_reward(current_reward, progress):
        if speed < 4:
            current_reward *= 0.75
        elif speed > 6:
            current_reward *= 1.25
        return current_reward

    # Execute Rewards
    reward = on_track_reward(reward, on_track)
    reward = distance_from_center_reward(reward, track_width, distance_from_center)
    reward = straight_line_reward(reward, steering, speed)
    reward = direction_reward(reward, waypoints, closest_waypoints, heading)
    reward = steering_reward(reward, steering)
    reward = throttle_reward(reward, speed, steering)
    reward = keep_left_reward(reward, keep_left)
    reward = progress_reward(reward, progress)
    reward = speed_reward(reward, speed)

    return float(reward)
