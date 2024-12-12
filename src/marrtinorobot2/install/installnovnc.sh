#!/bin/bash

# Installazione noVNC e configurazione come servizio su Ubuntu 22.04
# Esegui questo script come utente root o con sudo

echo "Aggiornamento del sistema e installazione dei pacchetti necessari..."

# Aggiorna il sistema e installa i pacchetti richiesti
apt-get update && apt-get install -y \
    tigervnc-standalone-server tigervnc-common \
    supervisor wget curl git python3-pip build-essential \
    bash-completion dos2unix && \
    apt-get autoclean && apt-get autoremove

echo "Scaricamento di noVNC..."

# Scarica noVNC
git clone https://github.com/AtsushiSaito/noVNC.git -b add_clipboard_support /usr/lib/novnc

echo "Installazione di websockify..."

# Installa websockify
pip install git+https://github.com/novnc/websockify.git@v0.10.0

# Crea un collegamento simbolico per l'accesso facilitato
ln -s /usr/lib/novnc/vnc.html /usr/lib/novnc/index.html

echo "Configurazione del servizio systemd per noVNC..."

# Crea il file di servizio systemd
cat <<EOF > /etc/systemd/system/novnc.service
[Unit]
Description=noVNC server
After=network.target

[Service]
Type=simple
ExecStart=/usr/lib/novnc/utils/novnc_proxy --vnc localhost:5901
Restart=always
User=$(whoami)
Group=$(whoami)

[Install]
WantedBy=multi-user.target
EOF

# Ricarica systemd e abilita il servizio
systemctl daemon-reload
systemctl enable novnc
systemctl start novnc

echo "Installazione e configurazione completate!"
echo "Il servizio noVNC è stato avviato e sarà disponibile all'avvio del sistema."
echo "Accedi a noVNC tramite il browser su http://<IP_DEL_TUO_SERVER>:6080"
