#!/usr/bin/env python3
"""
obstacle_avoidance.py  — Example node for Arjuna simulator

Mirrors the obstacle avoidance code from the Arjuna curriculum (Lab 9).
Works identically on the real robot and in the simulator since
it uses the same /scan and /cmd_vel topics.

Run in simulator:
    rosrun my_robot_code obstacle_avoidance.py

Run on real robot (same command, different ROS_MASTER_URI):
    ROS_MASTER_URI=http://<jetson-ip>:11311 rosrun my_robot_code obstacle_avoidance.py
"""

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

# ── Tuning parameters ──────────────────────────────────────────────
SAFE_DISTANCE  = 0.5   # metres — stop/turn if obstacle closer than this
LINEAR_SPEED   = 0.2   # m/s forward
ANGULAR_SPEED  = 0.4   # rad/s turning
# ───────────────────────────────────────────────────────────────────

pub = None

def get_regions(ranges):
    """
    Divide 720-sample scan into 6 named regions.
    Indices match the real robot's laser processing from the curriculum.
    """
    return {
        'front_L': min(min(ranges[0:130]),    10),
        'fleft':   min(min(ranges[131:230]),  10),
        'left':    min(min(ranges[231:280]),  10),
        'right':   min(min(ranges[571:620]),  10),
        'fright':  min(min(ranges[621:720]),  10),
        'front_R': min(min(ranges[721:850]),  10),
    }

def take_action(regions):
    """Decide velocity command based on nearest obstacle region."""
    msg = Twist()

    front_clear = (regions['front_L'] > SAFE_DISTANCE and
                   regions['front_R'] > SAFE_DISTANCE)
    left_clear   = regions['left']  > SAFE_DISTANCE
    right_clear  = regions['right'] > SAFE_DISTANCE

    if front_clear:
        # All clear — go straight
        msg.linear.x  =  LINEAR_SPEED
        msg.angular.z =  0.0
    elif not front_clear and left_clear:
        # Obstacle ahead, space on left → turn left
        msg.linear.x  =  0.0
        msg.angular_z =  ANGULAR_SPEED
    elif not front_clear and right_clear:
        # Obstacle ahead, space on right → turn right
        msg.linear.x  =  0.0
        msg.angular.z = -ANGULAR_SPEED
    else:
        # Blocked all around → reverse slowly
        msg.linear.x  = -LINEAR_SPEED * 0.5
        msg.angular.z =  ANGULAR_SPEED

    return msg

def clbk_laser(msg):
    """Callback for /scan — same as curriculum Lab 9."""
    # Guard against short scan arrays (e.g. during startup)
    if len(msg.ranges) < 860:
        return

    regions = get_regions(msg.ranges)
    cmd     = take_action(regions)
    pub.publish(cmd)

def main():
    global pub
    rospy.init_node('obstacle_avoidance')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rospy.Subscriber('/scan', LaserScan, clbk_laser)
    rospy.loginfo("Obstacle avoidance node started. Subscribed to /scan.")
    rospy.spin()

if __name__ == '__main__':
    main()
