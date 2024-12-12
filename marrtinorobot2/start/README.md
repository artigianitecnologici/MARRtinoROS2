# Autostart 
sudo apt-get install python3-yaml v4l2-utils netcat


To start devices and functionalities at boot automatically

1. Copy `autostart.yaml` file from template

        cd $MARRTINOROBOT2_HOME
        cp start/autostart_template.yaml ./autostart.yaml

2. Edit `autostart.yaml` and choose the configuration you want to run

3. Start (or restart) docker

        cd $MARRTINOROBOT2_HOME/docker
        ./start_docker.bash

This autostart will work also at robot boot.


## Manual start

Edit a start file `mystart.yaml`

Manual start

        cd $MARRTINOROBOT2_HOME/start
        python autostart.py mystart.yaml

Manual quit

        cd $MARRTINOROBOT2_HOME/start
        python autostart.py mystart.yaml --kill




