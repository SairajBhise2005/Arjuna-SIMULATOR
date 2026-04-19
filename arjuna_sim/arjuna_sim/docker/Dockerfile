FROM ros:melodic-robot

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=melodic

# ── apt timeout config — prevents hanging on slow/dead mirrors ──────────────
RUN echo 'Acquire::http::Timeout "30";'   >  /etc/apt/apt.conf.d/99timeout \
 && echo 'Acquire::ftp::Timeout "30";'    >> /etc/apt/apt.conf.d/99timeout \
 && echo 'Acquire::Retries "3";'          >> /etc/apt/apt.conf.d/99timeout \
 && echo 'Acquire::ForceIPv4 "true";'     >> /etc/apt/apt.conf.d/99timeout

# ── Layer 1: Fix apt sources and base utilities ─────────────────────────────
RUN sed -i 's|http://archive.ubuntu.com|http://us-east-1.ec2.archive.ubuntu.com|g' \
        /etc/apt/sources.list \
 && sed -i 's|http://security.ubuntu.com|http://us-east-1.ec2.archive.ubuntu.com|g' \
        /etc/apt/sources.list \
 && apt-get update && apt-get install -y --no-install-recommends \
        curl wget gnupg2 lsb-release ca-certificates git \
 && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc \
        | apt-key add - \
 && echo "deb http://packages.ros.org/ros/ubuntu bionic main" \
        > /etc/apt/sources.list.d/ros1-latest.list

# ── Layer 2: System / display packages ─────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        x11vnc xvfb novnc websockify \
        xfce4 xfce4-terminal dbus-x11 \
        python3-pip python3-numpy python3-setuptools \
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
# - setuptools must be upgraded first so pip can build wheels
# - opencv-python-headless installs via pre-built wheel (no compilation)
RUN pip3 install --no-cache-dir --upgrade setuptools pip \
 && pip3 install --no-cache-dir \
        catkin-tools \
        rospkg \
        catkin_pkg \
        opencv-python-headless \
        numpy

# ── Layer 6: Build catkin workspace ────────────────────────────────────────
RUN mkdir -p /catkin_ws/src
WORKDIR /catkin_ws

COPY ros_packages/      src/
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
