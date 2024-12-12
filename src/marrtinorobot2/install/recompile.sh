
### 1.0 Create WorkSpaces
cd $HOME/src
# git clone https://github.com/orbbec/OrbbecSDK_ROS2.git
# assume you have sourced ROS environment, same blow
sudo apt install -y libgflags-dev nlohmann-json3-dev libgoogle-glog-dev \
ros-$ROS_DISTRO-image-transport ros-$ROS_DISTRO-image-publisher ros-$ROS_DISTRO-camera-info-manager

cd $HOME
mkdir -p marrtinorobot2_ws/src

### 1.1 Install Microros 
cd $HOME/marrtinorobot2_ws
git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup
sudo apt install -y python3-vcstool build-essential
sudo apt update && rosdep update
rosdep install --from-path src --ignore-src -y
colcon build
source  install/setup.bash

#### 1.2 Setup micro-ROS agent:
ros2 run micro_ros_setup create_agent_ws.sh
ros2 run micro_ros_setup build_agent.sh
source  install/setup.bash
### 2.3 Clone  marrtinorobot2

cd $HOME/src
git clone -b humble-devel https://github.com/ROBOTIS-GIT/dynamixel-workbench.git
git clone -b humble-devel https://github.com/ROBOTIS-GIT/dynamixel-workbench-msgs.git
git clone -b humble-devel https://github.com/ROBOTIS-GIT/DynamixelSDK.git
git clone -b ros2 https://github.com/MoffKalast/vizanti.git
git clone https://github.com/robo-friends/m-explore-ros2.git
git clone https://github.com/ldrobotSensorTeam/ldlidar_stl_ros2.git



cd $HOME/marrtinorobot2_ws/src
ln -s $HOME/src/DynamixelSDK .
ln -s $HOME/src/dynamixel-workbench .
ln -s $HOME/src/dynamixel-workbench-msgs .

#
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_base .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_bringup .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_description .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_webinterface .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_gazebo .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_navigation .
ln -s $HOME/src/m-explore-ros2/explore .
#ln -s $HOME/src/OrbbecSDK_ROS2 .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_vision .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_voice .
#ln -s $HOME/src/marrtinorobot2/marrtinorobot2_ui .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_cartographer .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_dynamixel .
ln -s $HOME/src/depthai-ros .
ln -s $HOME/src/ldlidar-stl-ros2 .
ln -s $HOME/src/vizanti .
sudo apt install tmux -y


### 2.3 Install marrtinorobot2 package:
cd ..
rosdep update && rosdep install --from-path src --ignore-src -y --skip-keys microxrcedds_agent
source  install/setup.bash
cp $HOME/src/marrtinorobot2/install/script/*.sh .

sudo apt install gazebo -y
sudo apt install -y ros-$ROS_DISTRO-rplidar-ros
sudo apt-get install -y ros-${ROS_DISTRO}-v4l2-camera
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
# oak d lite
sudo apt install -y ros-$ROS_DISTRO-depthai-ros
# navigation
sudo apt install -y ros-$ROS_DISTRO-rtabmap-ros
## cartographer
sudo apt install -y ros-$ROS_DISTRO-cartographer 
sudo apt install -y ros-$ROS_DISTRO-cartographer-ros
sudo apt install -y ros-$ROS_DISTRO-localization
## Navigation Stack for ROS 2
sudo apt install -y ros-$ROS_DISTRO-navigation2 
sudo apt install -y ros-$ROS_DISTRO-nav2-bringup
## camera
sudo apt-get install -y ros-${ROS_DISTRO}-v4l2-camera
sudo apt install -y v4l-utils
sudo apt install -y ros-$ROS_DISTRO-camera-calibration-parsers
sudo apt install -y ros-$ROS_DISTRO-camera-info-manager
sudo apt install -y ros-$ROS_DISTRO-launch-testing-ament-cmake
## gazebo
sudo apt install -y ros-$ROS_DISTRO-gazebo-ros-pkg
sudo apt install -y ros-$ROS_DISTRO-robot-localization
## web interface 
sudo apt install ros-$ROS_DISTRO-rosbridge-server -y
### 2.3 Install prerequisite gazebo
sudo apt install ros-$ROS_DISTRO-gazebo-ros-pkgs -y
sudo apt install ros-$ROS_DISTRO-robot-localization -y
# joy 
sudo apt install -y ros-$ROS_DISTRO-joy 
sudo apt install -y ros-$ROS_DISTRO-teleop-twist-joystick

sudo apt install -y ros-$ROS_DISTRO-joint-state-publisher
sudo apt-get install -y ros-humble-rosbridge-suite


# astra camera
# sudo apt install ros-$ROS_DISTRO-image-pipeline libuvc-dev
# prerequisite marrtinorobot2_voice
pip3 install gtts
sudo apt install mpg321 sox  libttspico-utils -y
# prerequisiti vision
pip3 install opencv-python opencv-python-headless




