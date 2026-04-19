#!/usr/bin/env python3
"""
depth_bridge.py

The real Arjuna robot publishes depth as a single Float32 on
/oak/depth_value (centre pixel depth in metres).

This node reads /oak/depth/image_raw from Gazebo's depth camera
plugin and republishes the centre-pixel value on /oak/depth_value,
keeping the interface identical to the real robot.
"""

import rospy
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import Float32

class DepthBridge:
    def __init__(self):
        rospy.init_node('depth_bridge', anonymous=False)

        self.depth_pub = rospy.Publisher('/oak/depth_value', Float32, queue_size=2)
        rospy.Subscriber('/oak/depth/image_raw', Image, self.depth_callback)

        rospy.loginfo("Depth bridge started: /oak/depth/image_raw -> /oak/depth_value")

    def depth_callback(self, msg):
        try:
            # Convert raw depth image bytes to float array
            depth_array = np.frombuffer(msg.data, dtype=np.float32).reshape(
                msg.height, msg.width)

            # Get centre pixel (same as real OAK-D Lite code)
            cx = msg.width  // 2
            cy = msg.height // 2

            depth_val = float(depth_array[cy, cx])

            # Filter invalid readings (same as real robot: min_depth = 100mm)
            if np.isnan(depth_val) or np.isinf(depth_val) or depth_val < 0.1:
                return

            self.depth_pub.publish(Float32(depth_val))

        except Exception as e:
            rospy.logwarn_throttle(5.0, f"Depth bridge error: {e}")

    def spin(self):
        rospy.spin()

if __name__ == '__main__':
    bridge = DepthBridge()
    bridge.spin()
