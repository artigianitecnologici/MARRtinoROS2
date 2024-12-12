

set -e

ROSDISTRO="$(printenv ROS_DISTRO)"
BASE=$1
LASER_SENSOR=$2
DEPTH_SENSOR=$3
ARCH="$(uname -m)"
WORKSPACE="$HOME/marrtinorobot2_ws"

#### 1.4 Download and install micro-ROS:
cd $HOME/marrtinorobot2_ws
git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup
sudo apt install -y python3-vcstool build-essential
sudo apt update && rosdep update
rosdep install --from-path src --ignore-src -y
colcon build
source install/setup.bash

#### 1.5 Setup micro-ROS agent:
ros2 run micro_ros_setup create_agent_ws.sh
ros2 run micro_ros_setup build_agent.sh
source  install/setup.bash



mkdir -p $HOME/src
cd $HOME/src
#### 1.6 Download marrtinorobot2:
cd $WORKSPACE
git clone -b $ROS_DISTRO https://github.com/lartigianitecnologici/marrtinorobot2 


cd $WORKSPACE/src
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_base .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_bringup .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_description .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_gazebo .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_navigation .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_vision .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_voice .


### 2.3 Install marrtinorobot2 package:
cd $WORKSPACE
rosdep update && rosdep install --from-path src --ignore-src -y --skip-keys microxrcedds_agent
colcon build
source $WORKSPACE/install/setup.bash


# prerequisite teleop and video server
sudo apt install -y ros-$ROS_DISTRO-usb-cam
sudo apt install -y ros-$ROS_DISTRO-async-web-server-cpp 
sudo apt install -y ros-$ROS_DISTRO-rosbridge-server
sudo apt-get install -y ros-$ROS_DISTRO-teleop-twist-keyboard
#sudo apt-get -y install libegl-mesa0
sudo apt install -y ros-$ROS_DISTRO-teleop-twist-joy
##### no --> sudo apt-get install ros-$ROS_DISTRO-web-video-server
# launch rosbridge server
# run the executable with default settings (without params file)
ros2 run usb_cam usb_cam_node_exe

# run the executable while passing in parameters via a yaml file
ros2 run usb_cam usb_cam_node_exe --ros-args --params-file /path/to/colcon_ws/src/usb_cam/config/params.yaml

# launch the usb_cam executable that loads parameters from the same `usb_cam/config/params.yaml` file as above
# along with an additional image viewer node
ros2 launch usb_cam camera.launch.py
ros2 run web_video_server web_video_server


ros2 launch rosbridge_server rosbridge_websocket_launch.xml
ros2 launch teleop_twist_joy teleop-launch.py joy_config:='xbox'
# important
# hold R2 or X 
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo apt install ros-$ROS_DISTRO-depthai-ros

##install nodejs
sudo apt-get update
sudo apt-get install nodejs -y
sudo apt install npm
# cartographer 
sudo apt install ros-$ROS_DISTRO-cartographer -y
sudo apt install ros-$ROS_DISTRO-cartographer-ros -y
#  Navigation Stack for ROS 2

sudo apt install ros-$ROS_DISTRO-navigation2 -y
sudo apt install ros-$ROS_DISTRO-nav2-bringup -y 
sudo apt install ros-$ROS_DISTRO-gazebo-ros-pkgs -y
sudo apt install ros-$ROS_DISTRO-robot-localization -y
##### no -->  git clone -b ros2 https://github.com/RobotWebTools/web_video_server.git