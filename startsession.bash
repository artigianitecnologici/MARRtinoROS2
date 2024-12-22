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
  tmux -2 new-session -d -s $SESSION -n 'config'

  # Creazione delle finestre
  tmux new-window -t $SESSION:1 -n 'bringup'
  tmux new-window -t $SESSION:2 -n 'cam'
  tmux new-window -t $SESSION:3 -n 'slam'
  tmux new-window -t $SESSION:4 -n 'explorer'
  tmux new-window -t $SESSION:5 -n 'navigation'
  tmux new-window -t $SESSION:6 -n 'sample'
  tmux new-window -t $SESSION:7 -n 'sample2'
  tmux new-window -t $SESSION:8 -n 'sample3'

  # Comandi per ogni finestra
  tmux send-keys -t $SESSION:0 "cd ~/marrtinorobot2_ws && ./bringup.sh" C-m
  tmux send-keys -t $SESSION:1 "cd ~/marrtinorobot2_ws" C-m
  tmux send-keys -t $SESSION:2 "cd ~/marrtinorobot2_ws" C-m
  tmux send-keys -t $SESSION:3 "cd ~/marrtinorobot2_ws" C-m
  tmux send-keys -t $SESSION:4 "cd ~/marrtinorobot2_ws" C-m
  tmux send-keys -t $SESSION:5 "cd ~/marrtinorobot2_ws" C-m
  tmux send-keys -t $SESSION:6 "cd ~/marrtinorobot2_ws" C-m
  tmux send-keys -t $SESSION:7 "cd ~/marrtinorobot2_ws" C-m
  tmux send-keys -t $SESSION:8 "cd ~/marrtinorobot2_ws" C-m
fi

# Apertura della sessione tmux finale
tmux attach -t $SESSION
