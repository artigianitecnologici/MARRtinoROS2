#!/bin/bash

# Avvia un display virtuale
Xvfb :99 -screen 0 1280x720x16 &

# Avvia un semplice window manager (opzionale)
fluxbox &

# Avvia il server VNC
x11vnc -display :99 -nopw -forever -rfbport 5900 &

# Avvia noVNC
websockify --web=/opt/novnc --wrap-mode=ignore 6080 localhost:5900
