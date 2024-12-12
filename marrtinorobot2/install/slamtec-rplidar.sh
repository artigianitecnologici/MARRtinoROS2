# install slamtec lidar
cd $HOME/src 
git clone  https://github.com/Slamtec/sllidar_ros2.git
cd $HOME/marrtinorobot2_ws/src
ln -s $HOME/src/sllidar_ros2 .
