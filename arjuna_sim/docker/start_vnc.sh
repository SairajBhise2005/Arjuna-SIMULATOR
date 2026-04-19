#!/bin/bash

# Start virtual display
export DISPLAY=:1
Xvfb :1 -screen 0 1280x800x24 &
sleep 1

# Start desktop
startxfce4 &
sleep 2

# Start VNC server (no password for dev use - add one for production)
x11vnc -display :1 -nopw -forever -shared -rfbport 5900 &

# Start noVNC (browser-accessible VNC on port 6080)
websockify --web=/usr/share/novnc/ 6080 localhost:5900 &

echo "======================================"
echo "  Arjuna Simulator Ready"
echo "  Open browser: http://YOUR_EC2_IP:6080/vnc.html"
echo "======================================"

# Start roscore
roscore &
sleep 3

# Launch the full simulation
roslaunch arjuna_sim arjuna_sim.launch &

# Keep container running
wait
