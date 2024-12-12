echo "Create WorkSpace"
cd $HOME
mkdir -p marrtinorobot2_ws/src

echo "Install Microros ....."
cd $HOME/marrtinorobot2_ws
git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup
sudo apt install -y python3-vcstool build-essential
sudo apt update && rosdep update
rosdep install --from-path src --ignore-src -y
colcon build
source  install/setup.bash

echo " Setup micro-ROS agent ......"
ros2 run micro_ros_setup create_agent_ws.sh
ros2 run micro_ros_setup build_agent.sh
source  install/setup.bash

echo "Create link ...."

cd $HOME/marrtinorobot2_ws/src
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_base .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_bringup .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_description .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_gazebo .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_navigation .
ln -s $HOME/src/m-explore-ros2/explore .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_vision .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_voice .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_social .
ln -s $HOME/src/marrtinorobot2/marrtinorobot2_cartographer .




echo " Install marrtinorobot2 package ...."
cd ..
rosdep update && rosdep install --from-path src --ignore-src -y --skip-keys microxrcedds_agent
colcon build 
source  install/setup.bash

cp $HOME/src/marrtinorobot2/install/script/*.sh .


