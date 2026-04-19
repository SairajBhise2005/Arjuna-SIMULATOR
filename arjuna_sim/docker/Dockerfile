FROM ros:melodic-robot

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=melodic

# Core dependencies
RUN apt-get update && apt-get install -y \
    python3-pip python3-catkin-tools \
    ros-melodic-gazebo-ros-pkgs \
    ros-melodic-gazebo-ros-control \
    ros-melodic-robot-state-publisher \
    ros-melodic-joint-state-publisher \
    ros-melodic-joint-state-publisher-gui \
    ros-melodic-teleop-twist-keyboard \
    ros-melodic-rplidar-ros \
    ros-melodic-hector-slam \
    ros-melodic-robot-pose-ekf \
    ros-melodic-map-server \
    ros-melodic-navigation \
    ros-melodic-tf2-ros \
    ros-melodic-cv-bridge \
    ros-melodic-image-transport \
    ros-melodic-sensor-msgs \
    ros-melodic-nav-msgs \
    ros-melodic-geometry-msgs \
    ros-melodic-xacro \
    python-rospy python-catkin-pkg \
    python3-opencv python3-numpy \
    git wget curl \
    # VNC / display
    x11vnc xvfb novnc websockify \
    xfce4 xfce4-terminal dbus-x11 \
    && rm -rf /var/lib/apt/lists/*

# Python3 packages
RUN pip3 install opencv-python numpy rospkg catkin_pkg

# Workspace
RUN mkdir -p /catkin_ws/src
WORKDIR /catkin_ws

# Copy robot packages
COPY ros_packages/ src/
COPY robot_description/ src/arjuna_description/

# Build workspace
RUN /bin/bash -c "source /opt/ros/melodic/setup.bash && catkin_make"

# Startup scripts
COPY docker/entrypoint.sh /entrypoint.sh
COPY docker/start_vnc.sh /start_vnc.sh
RUN chmod +x /entrypoint.sh /start_vnc.sh

EXPOSE 6080 11311

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start_vnc.sh"]
