#!/bin/bash

# Create User
USER=${USER:-root}
HOME=/root
if [ "$USER" != "root" ]; then
    echo "* enable custom user: $USER"
    useradd --create-home --shell /bin/bash --user-group --groups adm,sudo $USER
    echo "$USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
    if [ -z "$PASSWORD" ]; then
        echo "  set default password to \"ubuntu\""
        PASSWORD=ubuntu
    fi
    HOME=/home/$USER
    echo "$USER:$PASSWORD" | /usr/sbin/chpasswd 2> /dev/null || echo ""
    cp -r /root/{.config,.gtkrc-2.0,.asoundrc} ${HOME} 2>/dev/null
    chown -R $USER:$USER ${HOME}
    [ -d "/dev/snd" ] && chgrp -R adm /dev/snd
fi

# # Supervisor
# CONF_PATH=/etc/supervisor/conf.d/supervisord.conf
# cat << EOF > $CONF_PATH
# [supervisord]
# nodaemon=true
# user=root
# [program:vnc]
# command=gosu '$USER' bash '$VNCRUN_PATH'
# [program:novnc]
# command=gosu '$USER' bash -c "websockify --web=/usr/lib/novnc 8085 localhost:5901"
# EOF

# colcon
BASHRC_PATH=$HOME/.bashrc
grep -F "source /opt/ros/$ROS_DISTRO/setup.bash" $BASHRC_PATH || echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> $BASHRC_PATH
grep -F "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" $BASHRC_PATH || echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> $BASHRC_PATH
chown $USER:$USER $BASHRC_PATH

# Fix rosdep permission
mkdir -p $HOME/.ros
cp -r /root/.ros/rosdep $HOME/.ros/rosdep
chown -R $USER:$USER $HOME/.ros


# chown -R $USER:$USER $HOME/Desktop

# clearup
PASSWORD=
VNC_PASSWORD=


SESSION=init

# Check if the session already exists
tmux has-session -t $SESSION 2>/dev/null

if [ $? != 0 ]; then
  # If the session doesn't exist, set up a new tmux session
  tmux -2 new-session -d -s $SESSION
  tmux rename-window -t $SESSION:0 'config'  # Window 0 is renamed to 'config'
  tmux new-window -t $SESSION:1 -n 'rosbridge'  # Window 1 named 'docker'
  tmux new-window -t $SESSION:2 -n 'cmdexe'  # Window 2 named 'cmdexe'
  tmux new-window -t $SESSION:3 -n 'robot_bringup'  # Window 3 named 'robot_bringup'
  tmux new-window -t $SESSION:4 -n 'autostart'  # Window 3 named 'robot_bringup'
fi

# Log files for command output
CMD_EXE_LOG="/tmp/cmdexe.log"
ROBOT_BRINGUP_LOG="/tmp/robot_bringup.log"
AUTOSTART_LOG="/tmp/autostart.log"


# Commands to be executed in window 2 ('cmdexe')
tmux send-keys -t $SESSION:1 "cd \$MARRTINOROBOT2_WS" C-m
tmux send-keys -t $SESSION:1 "./rosbridge.sh > $CMD_EXE_LOG 2>&1 &" C-m  # Log output to cmdexe.lo

# Commands to be executed in window 2 ('cmdexe')
tmux send-keys -t $SESSION:2 "cd ~/src/marrtinorobot2/marrtinorobot2_webinterface/marrtinorobot2_webinterface" C-m
tmux send-keys -t $SESSION:2 "python3 command_executor.py > $CMD_EXE_LOG 2>&1 &" C-m  # Log output to cmdexe.log

# Commands to be executed in window 3 ('robot_bringup')
tmux send-keys -t $SESSION:3 "cd ~/src/marrtinorobot2/marrtinorobot2_webinterface/marrtinorobot2_webinterface" C-m
tmux send-keys -t $SESSION:3 "python3 robot_bringup.py > $ROBOT_BRINGUP_LOG 2>&1 &" C-m  # Log output to robot_bringup.log

# Commands to be executed in window 4 ('robot_bringup')
tmux send-keys -t $SESSION:4 "cd ~/src/marrtinorobot2/bringup" C-m
tmux send-keys -t $SESSION:4 "python3 autostart.py > $AUTOSTART_LOG 2>&1 &" C-m  # Log output to robot_bringup.log

echo "============================================================================================"
echo "NOTE 1: --security-opt seccomp=unconfined flag is required to launch Ubuntu Jammy based image."
echo -e 'See \e]8;;https://github.com/Tiryoh/docker-ros2-desktop-vnc/pull/56\e\\https://github.com/Tiryoh/docker-ros2-desktop-vnc/pull/56\e]8;;\e\\'
echo "============================================================================================"

# exec /bin/tini -- supervisord -n -c /etc/supervisor/supervisord.conf
