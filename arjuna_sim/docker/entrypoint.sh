#!/bin/bash
set -e

# Source ROS and workspace
source /opt/ros/melodic/setup.bash
source /catkin_ws/devel/setup.bash

# Export ROS environment
export ROS_MASTER_URI=http://localhost:11311
export ROS_HOSTNAME=localhost

exec "$@"
