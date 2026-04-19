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
# On Ubuntu 18.04 the web root is /usr/share/novnc
NOVNC_DIR=/usr/share/novnc
if [ ! -d "$NOVNC_DIR" ]; then
    NOVNC_DIR=$(find /usr -name "vnc.html" 2>/dev/null | head -1 | xargs dirname)
fi
websockify --web="$NOVNC_DIR" 6080 localhost:5900 &

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
