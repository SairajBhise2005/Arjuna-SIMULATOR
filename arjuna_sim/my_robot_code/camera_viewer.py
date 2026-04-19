#!/usr/bin/env python3
"""
camera_viewer.py  — Example camera subscriber for Arjuna simulator

Subscribes to the same topics published by the real robot's OAK-D Lite:
  /frames          → sensor_msgs/Image  (RGB, 640x480 @ 30fps)
  /oak/depth_value → std_msgs/Float32   (centre pixel depth in metres)

Works identically on real robot and simulator.
"""

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import Float32

# Simple CvBridge replacement (same approach as real robot curriculum code)
class CustomCvBridge:
    def imgmsg_to_cv2(self, img_msg, desired_encoding="bgr8"):
        dtype = np.uint8
        n_channels = 3 if desired_encoding == "bgr8" else 1
        img = np.frombuffer(img_msg.data, dtype=dtype)
        img = img.reshape(img_msg.height, img_msg.width, n_channels)
        return img

class CameraViewer:
    def __init__(self):
        rospy.init_node('camera_viewer')
        self.bridge       = CustomCvBridge()
        self.rgb_frame    = None
        self.depth_value  = None

        rospy.Subscriber('/frames',           Image,   self.rgb_callback)
        rospy.Subscriber('/oak/depth_value',  Float32, self.depth_callback)

        rospy.loginfo("Camera viewer started. Topics: /frames, /oak/depth_value")

    def rgb_callback(self, msg):
        try:
            self.rgb_frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            rospy.logwarn(f"RGB callback error: {e}")

    def depth_callback(self, msg):
        self.depth_value = msg.data

    def run(self):
        rate = rospy.Rate(30)
        while not rospy.is_shutdown():
            if self.rgb_frame is not None:
                display = self.rgb_frame.copy()

                # Overlay depth value
                if self.depth_value is not None:
                    text = f"Depth: {self.depth_value:.2f} m"
                    cv2.putText(display, text, (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                                (0, 255, 0), 2)

                cv2.imshow("Arjuna Camera", display)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            rate.sleep()

        cv2.destroyAllWindows()

if __name__ == '__main__':
    viewer = CameraViewer()
    viewer.run()
