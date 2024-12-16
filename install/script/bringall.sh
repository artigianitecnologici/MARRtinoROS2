#!/bin/bash
#set -x  # Abilita il debug
source install/setup.bash
ros2 launch marrtinorobot2_bringup bringup.launch.py \
  use_camera:=true \
  use_tts:=true \
  use_ldlidar:=true


