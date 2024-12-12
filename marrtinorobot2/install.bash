#!/bin/bash

while true; do
  clear
  echo "### MENU PRINCIPALE ###"
  echo "1) Prerequisiti"
  echo "2) ROS 2 Humble"
  echo "3) Docker"
  echo "4) Esci"
  echo "#######################"
  read -p "Seleziona un'opzione: " scelta

  case $scelta in
    1)
      bash script1.sh
      ;;
    2)
      bash script2.sh
      ;;
    3)
      bash script3.sh
      ;;
    4)
      echo "Uscita in corso..."
      exit 0
      ;;
    *)
      echo "Opzione non valida. Riprova."
      sleep 2
      ;;
  esac
done
