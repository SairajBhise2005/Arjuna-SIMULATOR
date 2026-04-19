cmake_minimum_required(VERSION 3.0.2)
project(arjuna_sim)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  sensor_msgs
  nav_msgs
  geometry_msgs
)

catkin_package()

install(PROGRAMS
  scripts/encoder_bridge.py
  scripts/depth_bridge.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch worlds config
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
