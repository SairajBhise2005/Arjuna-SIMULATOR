FROM ros:melodic-robot

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=melodic

# ── Layer 1: Fix apt sources and base utilities ─────────────────────────────
# ros:melodic-robot ships with a stale apt cache and sometimes broken sources.
# We re-add the ROS key explicitly before doing anything else.
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl wget gnupg2 lsb-release ca-certificates git \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc \
        | apt-key add - \
    && echo "deb http://packages.ros.org/ros/ubuntu bionic main" \
        > /etc/apt/sources.list.d/ros1-latest.list

# ── Layer 2: System / display packages ─────────────────────────────────────
# novnc ships as 'novnc' on Bionic (Ubuntu 18.04).
# websockify is a separate package.
RUN apt-get update && apt-get install -y --no-install-recommends \
        x11vnc \
        xvfb \
        novnc \
        websockify \
        xfce4 \
        xfce4-terminal \
        dbus-x11 \
        python3-pip \
        python3-numpy \
    && rm -rf /var/lib/apt/lists/*

# ── Layer 3: Core ROS Melodic packages ─────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        ros-melodic-gazebo-ros-pkgs \
        ros-melodic-gazebo-ros-control \
        ros-melodic-robot-state-publisher \
        ros-melodic-joint-state-publisher \
        ros-melodic-joint-state-publisher-gui \
        ros-melodic-xacro \
        ros-melodic-tf2-ros \
        ros-melodic-cv-bridge \
        ros-melodic-image-transport \
        ros-melodic-sensor-msgs \
        ros-melodic-nav-msgs \
        ros-melodic-geometry-msgs \
    && rm -rf /var/lib/apt/lists/*

# ── Layer 4: Extra ROS packages (navigation stack etc.) ────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        ros-melodic-teleop-twist-keyboard \
        ros-melodic-rplidar-ros \
        ros-melodic-map-server \
        ros-melodic-navigation \
        ros-melodic-robot-pose-ekf \
        ros-melodic-hector-slam \
    && rm -rf /var/lib/apt/lists/*

# ── Layer 5: Python build tools ────────────────────────────────────────────
# catkin-tools from PyPI is more reliable than the apt package on Bionic.
# We do NOT install python-rospy (Python 2) to avoid conflicts.
RUN pip3 install --no-cache-dir \
        catkin-tools \
        rospkg \
        catkin_pkg \
        opencv-python \
        numpy

# ── Layer 6: Build catkin workspace ────────────────────────────────────────
RUN mkdir -p /catkin_ws/src
WORKDIR /catkin_ws

COPY ros_packages/   src/
COPY robot_description/ src/arjuna_description/

RUN /bin/bash -c "\
    source /opt/ros/melodic/setup.bash && \
    catkin_make -DCMAKE_BUILD_TYPE=Release"

# ── Layer 7: Startup scripts ────────────────────────────────────────────────
COPY docker/entrypoint.sh /entrypoint.sh
COPY docker/start_vnc.sh  /start_vnc.sh
RUN chmod +x /entrypoint.sh /start_vnc.sh

EXPOSE 6080 11311

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start_vnc.sh"]
