#!/bin/bash

# Definizione della sessione tmux
SESSION=init

# Funzione per killare la sessione
kill_session() {
  tmux has-session -t $SESSION 2>/dev/null
  if [ $? == 0 ]; then
    tmux kill-session -t $SESSION
    echo "Sessione '$SESSION' killata con successo."
  else
    echo "Nessuna sessione '$SESSION' trovata."
  fi
  exit 0
}

# Gestione del parametro --kill
if [ "$1" == "--kill" ]; then
  kill_session
fi

# Controllo se la sessione esiste già
tmux has-session -t $SESSION 2>/dev/null

if [ $? != 0 ]; then
  # Creazione della sessione tmux
   
  tmux -2 new-session -d -s $SESSION
  tmux rename-window -t $SESSION:0 'bringup'  # Window 0 is renamed to 'config'
  tmux new-window -t $SESSION:1 -n 'rplidar'  # Window 1 named 'docker'
  tmux new-window -t $SESSION:2 -n 'websocket'  # Window 2 named 'cmdexe'
  tmux new-window -t $SESSION:3 -n 'robot_bringup'  # Window 3 named 'robot_bringup'
  tmux new-window -t $SESSION:4 -n 'autostart'  # Window 3 named 'robot_bringup'
  tmux new-window -t $SESSION:5 -n 'blockly'
  tmux new-window -t $SESSION:6 -n 'tts'
  tmux new-window -t $SESSION:7 -n 'rplidar'
  tmux new-window -t $SESSION:9 -n 'slam'
  #tmux new-window -t $SESSION:10 -n 'sample1'
  #tmux new-window -t $SESSION:11 -n 'sample2'
  #tmux new-window -t $SESSION:12 -n 'sample3'


  # Log files for command output
  CMD_EXE_LOG="/tmp/cmdexe.log"
  ROBOT_BRINGUP_LOG="/tmp/robot_bringup.log"
  AUTOSTART_LOG="/tmp/autostart.log"
  # Commands to be executed in window 1
  tmux send-keys -t $SESSION:0 "cd \$MARRTINOROBOT2_WS" C-m
  tmux send-keys -t $SESSION:0 "./bringup.sh " C-m  # 

  # Commands to be executed in window 1
  tmux send-keys -t $SESSION:1 "cd \$MARRTINOROBOT2_WS" C-m
  tmux send-keys -t $SESSION:1 "./rplidar-c1.sh " C-m  # Log output to cmdexe.lo

  # Commands to be executed in window 2 
  tmux send-keys -t $SESSION:2 "cd ~/src/marrtinorobot2/marrtinorobot2_webinterface/marrtinorobot2_webinterface" C-m
  tmux send-keys -t $SESSION:2 "python3 websocket_robot.py " C-m  # Log to websocket_robot.log

  # Commands to be executed in window 3 ('robot_bringup')
  tmux send-keys -t $SESSION:3 "cd \$MARRTINOROBOT2_WS" C-m
  #tmux send-keys -t $SESSION:3 "python3 robot_bringup.py " C-m  # Log output to robot_bringup.log

  # Commands to be executed in window 4 ('robot_bringup')
  tmux send-keys -t $SESSION:4 "cd \$MARRTINOROBOT2_WS" C-m
  # sleep 5
  tmux send-keys -t $SESSION:5 "cd \$MARRTINOROBOT2_WS" C-m
  
  tmux send-keys -t $SESSION:6 "cd \$MARRTINOROBOT2_WS" C-m
  tmux send-keys -t $SESSION:6 "./tts.sh " C-m  # Log output to cmdexe.lo

  tmux send-keys -t $SESSION:7 "cd \$MARRTINOROBOT2_WS" C-m
  #tmux send-keys -t $SESSION:7 "./rplidar-c1.sh " C-m  # Log output to cmdexe.lo

  
  tmux send-keys -t $SESSION:8 "cd ~/marrtinorobot2_ws" C-m
  tmux send-keys -t $SESSION:9 "cd ~/marrtinorobot2_ws" C-m
  #tmux send-keys -t $SESSION:10 "cd ~/marrtinorobot2_ws" C-m
  #tmux send-keys -t $SESSION:11 "cd ~/marrtinorobot2_ws" C-m
  #tmux send-keys -t $SESSION:12 "cd ~/marrtinorobot2_ws" C-m
fi

# Apertura della sessione tmux finale
tmux attach -t $SESSION
