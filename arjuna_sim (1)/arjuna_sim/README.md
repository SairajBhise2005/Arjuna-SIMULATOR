# Arjuna Robot Simulator

Gazebo-based simulator for the **Arjuna AMR** (NEWRRO TECH LLP).  
Runs on any machine via Docker — developed for EC2 Ubuntu 22.04.  
Code you write here works **unchanged on the real robot**.

---

## Robot Specs Implemented

| Component | Real Robot | Simulator |
|-----------|-----------|-----------|
| Processor | Jetson Nano (Ubuntu 18) | Docker (Ubuntu 18 + ROS Melodic) |
| Drive | Quad motors, differential drive | Gazebo diff drive plugin |
| Lidar | RPLidar C1M1 — 360°, 0.15–12m, 10Hz | Ray sensor plugin, same params |
| Camera | OAK-D Lite (RGB + stereo depth) | RGB camera + depth plugin |
| IMU | BNO055 | Gazebo IMU plugin |
| Encoders | Optical, 4095 ticks/rev | Joint state → tick bridge |
| Wheel radius | 0.04 m | 0.04 m |
| Wheelbase | 0.28 m | 0.28 m |

## ROS Topics (identical to real robot)

| Topic | Type | Description |
|-------|------|-------------|
| `/cmd_vel` | `geometry_msgs/Twist` | Motor velocity commands |
| `/scan` | `sensor_msgs/LaserScan` | RPLidar 360° scan |
| `/odom` | `nav_msgs/Odometry` | Wheel odometry |
| `/frames` | `sensor_msgs/Image` | OAK-D RGB frames (640×480 @ 30fps) |
| `/oak/depth_value` | `std_msgs/Float32` | Centre-pixel depth in metres |
| `/oak/depth/points` | `sensor_msgs/PointCloud2` | Full depth point cloud |
| `/imu/data` | `sensor_msgs/Imu` | IMU orientation + angular velocity |
| `/left_ticks` | `std_msgs/Int64` | Left wheel encoder ticks |
| `/right_ticks` | `std_msgs/Int64` | Right wheel encoder ticks |

---

## EC2 Setup (Ubuntu 22.04)

### 1. Install Docker

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```

### 2. Open EC2 Security Group Ports

In your AWS console, add **inbound rules**:

| Port | Protocol | Description |
|------|----------|-------------|
| 6080 | TCP | noVNC browser UI |
| 11311 | TCP | ROS Master (for remote rosrun) |

### 3. Clone / Upload this project

```bash
# Upload from your laptop
scp -r arjuna_sim/ ubuntu@YOUR_EC2_IP:~/

# OR on the EC2 directly
cd ~
# (place the arjuna_sim folder here)
```

### 4. Build the Docker image

```bash
cd ~/arjuna_sim
docker compose build
# First build takes ~10–15 minutes (downloads ROS + Gazebo)
```

### 5. Start the simulator

```bash
docker compose up
```

### 6. Open in browser

```
http://YOUR_EC2_IP:6080/vnc.html
```

Click **Connect**. You'll see the Gazebo world with the Arjuna robot and RViz side by side.

---

## Writing & Running Your Code

Your code goes in `my_robot_code/`. This folder is **live-mounted** into the container — edit files locally, run them instantly inside Docker.

### Run a script inside the container

```bash
# Open a shell in the running container
docker exec -it arjuna_sim bash

# Inside the container:
source /catkin_ws/devel/setup.bash
python3 /catkin_ws/src/my_robot_code/obstacle_avoidance.py
```

### Teleoperate the robot (keyboard)

```bash
docker exec -it arjuna_sim bash
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```

### Check topics

```bash
docker exec -it arjuna_sim bash
rostopic list
rostopic echo /scan
rostopic echo /oak/depth_value
```

---

## Switching from Simulator to Real Robot

Your code does not change. You only change where ROS points:

```bash
# On your laptop / EC2, set these before running your node:
export ROS_MASTER_URI=http://<JETSON_NANO_IP>:11311
export ROS_HOSTNAME=<YOUR_MACHINE_IP>

python3 my_robot_code/obstacle_avoidance.py
```

The same `/scan`, `/cmd_vel`, `/frames`, `/oak/depth_value` topics will be there.

---

## Project Structure

```
arjuna_sim/
├── docker/
│   ├── Dockerfile          # Ubuntu 18 + ROS Melodic + Gazebo
│   ├── entrypoint.sh       # Sources ROS on container start
│   └── start_vnc.sh        # Starts Xvfb + VNC + noVNC + ROS
├── robot_description/      # ROS package: URDF/xacro robot model
│   └── urdf/
│       └── arjuna.urdf.xacro  # Full robot with all sensor plugins
├── ros_packages/
│   └── arjuna_sim/         # ROS package: launch, worlds, bridges
│       ├── launch/
│       │   └── arjuna_sim.launch   # Main launch file
│       ├── worlds/
│       │   └── arjuna_world.world  # Indoor room with obstacles
│       ├── scripts/
│       │   ├── encoder_bridge.py   # joint_states → /left_ticks, /right_ticks
│       │   └── depth_bridge.py     # depth image → /oak/depth_value
│       └── config/
│           └── arjuna.rviz         # RViz config (lidar, camera, odom)
├── my_robot_code/          # ← PUT YOUR CODE HERE (live-mounted)
│   ├── obstacle_avoidance.py
│   └── camera_viewer.py
└── docker-compose.yml
```

---

## Troubleshooting

**Gazebo is slow / laggy**  
EC2 t2/t3 instances have no GPU. Reduce Gazebo update rate:  
`export GAZEBO_RENDERING=ogre` inside the container, or use a `g4dn` instance.

**noVNC blank screen**  
Wait 15–20 seconds after `docker compose up` for Gazebo to fully load, then refresh.

**ROS topics not appearing**  
```bash
docker exec -it arjuna_sim bash
rostopic list    # should show /scan, /cmd_vel, /odom etc.
```
If empty, roscore may still be starting. Wait and retry.

**Port 6080 not reachable**  
Confirm your EC2 security group has port 6080 open for your IP.
