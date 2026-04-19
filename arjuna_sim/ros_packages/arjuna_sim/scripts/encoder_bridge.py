#!/usr/bin/env python3
"""
encoder_bridge.py

Converts Gazebo wheel joint positions into integer tick counts on
/left_ticks and /right_ticks — the same topics published by the
real Arjuna robot (Arjuna_ticks_pub.py on Arduino/Jetson).

From real robot odometry code:
  TICKS_PER_REVOLUTION = 4095
  WHEEL_RADIUS         = 0.04 m
  WHEEL_BASE           = 0.28 m
  TICKS_PER_METER      = 20475
"""

import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Int64
import math

TICKS_PER_REVOLUTION = 4095

class EncoderBridge:
    def __init__(self):
        rospy.init_node('encoder_bridge', anonymous=False)

        self.left_ticks_pub  = rospy.Publisher('/left_ticks',  Int64, queue_size=10)
        self.right_ticks_pub = rospy.Publisher('/right_ticks', Int64, queue_size=10)

        # Track cumulative angle for each wheel
        self.prev_left_angle  = None
        self.prev_right_angle = None
        self.left_ticks_accum  = 0
        self.right_ticks_accum = 0

        rospy.Subscriber('/joint_states', JointState, self.joint_state_callback)
        rospy.loginfo("Encoder bridge started: /joint_states -> /left_ticks, /right_ticks")

    def joint_state_callback(self, msg):
        # Find front wheel indices (same rotation as rear on diff drive)
        try:
            fl_idx = msg.name.index('front_left_wheel_joint')
            fr_idx = msg.name.index('front_right_wheel_joint')
        except ValueError:
            return

        left_angle  = msg.position[fl_idx]
        right_angle = msg.position[fr_idx]

        if self.prev_left_angle is None:
            self.prev_left_angle  = left_angle
            self.prev_right_angle = right_angle
            return

        # Delta angle (radians) → delta ticks
        delta_left  = left_angle  - self.prev_left_angle
        delta_right = right_angle - self.prev_right_angle

        self.left_ticks_accum  += int((delta_left  / (2 * math.pi)) * TICKS_PER_REVOLUTION)
        self.right_ticks_accum += int((delta_right / (2 * math.pi)) * TICKS_PER_REVOLUTION)

        self.prev_left_angle  = left_angle
        self.prev_right_angle = right_angle

        self.left_ticks_pub.publish(Int64(self.left_ticks_accum))
        self.right_ticks_pub.publish(Int64(self.right_ticks_accum))

    def spin(self):
        rospy.spin()

if __name__ == '__main__':
    bridge = EncoderBridge()
    bridge.spin()
