#!/bin/bash

# Definizione della sessione tmux
SESSION=init

# Controllo se la sessione esiste già
tmux has-session -t $SESSION 

if [ $? != 0 ]; then
  # Creazione della sessione tmux
  tmux -2 new-session -d -s $SESSION
  tmux rename-window -t $SESSION:0 'config'
  tmux new-window -t $SESSION:1 -n 'bringup'
  tmux new-window -t $SESSION:2 -n 'cam'
  tmux new-window -t $SESSION:3 -n 'slam'
  tmux new-window -t $SESSION:4 -n 'explorer'
  tmux new-window -t $SESSION:5 -n 'navigation'
  tmux new-window -t $SESSION:6 -n 'sample'
  tmux new-window -t $SESSION:7 -n 'sample2'
  tmux new-window -t $SESSION:8 -n 'sample3'


  # Comandi per ogni finestra
  tmux send-keys -t $SESSION:0 "cd ~/marrtinorobot2_ws" C-m
  tmux send-keys -t $SESSION:0 "./bringup.sh" C-m
  tmux send-keys -t $SESSION:1 "cd ~/marrtinorobot2_ws" C-m
  tmux send-keys -t $SESSION:2 "cd ~/marrtinorobot2_ws" C-m
  tmux send-keys -t $SESSION:3 "cd ~/marrtinorobot2_ws" C-m
  tmux send-keys -t $SESSION:4 "cd ~/marrtinorobot2_ws" C-m
  # tmux send-keys -t $SESSION:0 "python wsconfig.py" C-m
  
#   tmux send-keys -t $SESSION:1 "cd " C-m
#   sleep 5  # Attesa per assicurarsi che roscore sia attivo

#   tmux send-keys -t $SESSION:3 "cd \$MARRTINO_APPS_HOME/blockly" C-m
#   tmux send-keys -t $SESSION:3 "python websocket_robot.py" C-m
# fi

# Monitoraggio del file quitrequest
# while [ ! -f "/tmp/quitrequest" ]; do
#   sleep 5
# done

# Apertura della sessione tmux finale per monitoraggio
tmux attach -t $SESSION
