#!/usr/bin/env bash

set -e

#### 1.4 Download and install micro-ROS:
cd $HOME
# Source the ROS 2 installation
source /opt/ros/$ROS_DISTRO/setup.bash
# Create a workspace and download the micro-ROS tools
mkdir marrtinorobot2_ws
cd marrtinorobot2_ws
git clone  https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup
# Update dependencies using rosdep
sudo apt update && rosdep update
rosdep install --from-paths src --ignore-src -y

# Install pip
sudo apt-get install python3-pip

# Build micro-ROS tools and source them
colcon build
source install/local_setup.bash

ros2 run micro_ros_setup create_firmware_ws.sh host
# Build step
source install/local_setup.bash
ros2 run micro_ros_setup build_firmware.sh
source install/local_setup.bash



#### 1.5 Setup micro-ROS agent:
ros2 run micro_ros_setup create_agent_ws.sh
ros2 run micro_ros_setup build_agent.sh
source install/setup.bash

