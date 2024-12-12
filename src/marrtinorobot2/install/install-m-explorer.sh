cd $HOME/src
git clone https://github.com/robo-friends/m-explore-ros2.git
cd $HOME/marrtinorobot2_ws/src
ln -s $HOME/src/m-exploer-ros2 .
cd ..
rosdep install --from-path src --ignore-src -y
colcon build
source  install/setup.bash