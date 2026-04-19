# my_robot_code

Put all your ROS Python/C++ nodes here.

This folder is **live-mounted** into the Docker container at:
`/catkin_ws/src/my_robot_code`

You can edit files on your laptop (or EC2) and run them immediately inside
the container without rebuilding the image.

## Included examples

- `obstacle_avoidance.py` — subscribes to `/scan`, publishes to `/cmd_vel`
- `camera_viewer.py`      — subscribes to `/frames` and `/oak/depth_value`

## Running your code

```bash
docker exec -it arjuna_sim bash
source /catkin_ws/devel/setup.bash
python3 /catkin_ws/src/my_robot_code/your_script.py
```
