#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
import re
import yaml

# Funzione per trovare un dispositivo webcam per nome
def find_webcam_by_name(device_name):
    try:
        result = subprocess.run(['v4l2-ctl', '--list-devices'], capture_output=True, text=True)
        video_devices = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running v4l2-ctl: {e}")
        return None

    # Regex per trovare il dispositivo
    pattern = re.compile(rf'{re.escape(device_name)}:.*?(/dev/video\d+)', re.DOTALL)
    match = pattern.search(video_devices)

    # Controllo e ritorno del dispositivo
    if match:
        video_device_path = match.group(1)
        print(f"Found Webcam Information:\n{video_devices}")
        print(f"Associated {video_device_path}")
        return video_device_path
    else:
        print(f"Webcam with device name '{device_name}' not found.")
        return None

# Funzione per leggere il file YAML
def readconfig(yamlfile):
    try:
        with open(yamlfile, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"YAML file {yamlfile} not found!")
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML file: {exc}")
        sys.exit(1)

# Funzione per eseguire comandi di sistema con netcat
def systemcmd(cmdkey, port):
    cmd = f"echo '{cmdkey}' | netcat -w 1 localhost {port}"
    print("  " + cmd)
    os.system(cmd)
    time.sleep(3)

# Funzione per ottenere una chiave dal file YAML
def getconfig(section, key):
    try:
        return config[section][key]
    except KeyError:
        return None

# Funzione principale per l'avvio automatico di dispositivi e funzioni
def autostart(config, dostart):
    print("Auto start:")

    # Simulatore (usando comandi ROS 2 se applicabile)
    # if getconfig('simulator', 'stage'):
        # mapname = getconfig('simulator', 'mapname')
        # robottype = getconfig('simulator', 'robottype')
        # nrobots = getconfig('simulator', 'nrobots')
        # simtimeval = 'true' if dostart else 'false'
        
        # # ROS 2: Usa ros2 param set
        # cmd = f'ros2 param set /use_sim_time {simtimeval}'
        # subprocess.run(cmd, shell=True)
        
        # # Avvia o arresta lo stage
        # stage_cmd = f"{mapname};{robottype};{nrobots}" if dostart else "@stagekill"
        # systemcmd(stage_cmd, 9235)

    # Avvio dei dispositivi (robot, joystick, camera, laser)
    if getconfig('devices', 'robot'):
        systemcmd('@robot' if dostart else '@robotkill', 9236)

    joystick = getconfig('devices', 'joystick')
    if joystick == '2wd':
        systemcmd('@joystick' if dostart else '@joystickkill', 9240)
    elif joystick == 'keyboard':
        systemcmd('@keyboard' if dostart else '@joystickkill', 9240)
    elif joystick == '4wd':
        systemcmd('@joystick4wd' if dostart else '@joystickkill', 9240)

    cam = getconfig('devices', 'camera')
    if cam in ['usbcam', 'astra', 'xtion']:
        systemcmd(f'@{cam}' if dostart else '@camerakill', 9237)
    else:
        device_name_to_find = "USB 2.0 Camera"
        device_name = find_webcam_by_name(device_name_to_find)
        if device_name:
            systemcmd(f'@camera_{device_name}' if dostart else '@camerakill', 9237)

    las = getconfig('devices', 'laser')
    if las in ['hokuyo', 'rplidar', 'ld06']:
        systemcmd(f'@{las}' if dostart else '@laserkill', 9238)

    # Funzioni ROS (localizzazione, navigazione, mapping)
    if getconfig('functions', 'localization'):
        systemcmd('@loc' if dostart else '@lockill', 9238)

    navigation = getconfig('functions', 'navigation')
    if navigation == 'gbn':
        systemcmd('@gbn' if dostart else '@gbnkill', 9238)
    elif navigation == 'move_base':
        systemcmd('@movebase' if dostart else '@movebasekill', 9238)
    elif navigation == 'move_base_gbn':
        systemcmd('@movebasegbn' if dostart else '@movebasekill', 9238)

    if getconfig('functions', 'navigation_rviz'):
        systemcmd('@rviz' if dostart else '@rvizkill', 9238)

    if getconfig('functions', 'mapping') == 'gmapping':
        systemcmd('@gmapping' if dostart else '@gmappingkill', 9241)
    elif getconfig('functions', 'mapping') == 'srrg_mapper':
        systemcmd('@srrgmapper' if dostart else '@srrgmapperkill', 9241)

    # Funzioni aggiuntive
    if getconfig('functions', 'videoserver'):
        systemcmd('@videoserver' if dostart else '@videoserverkill', 9237)

    if getconfig('functions', 'rosbridge'):
        systemcmd('@rosbridge' if dostart else '@rosbridgekill', 9237)

    if getconfig('functions', 'apriltags'):
        systemcmd('@apriltags' if dostart else '@apriltagskill', 9237)

    if getconfig('functions', 'pantilt'):
        systemcmd('@pantilt_start' if dostart else '@pantilt_kill', 9249)


# Avvio script principale
if __name__ == '__main__':
    autostartfile = "autostart.yaml"
    yamlfile = os.getenv('MARRTINO_APPS_HOME', '') + "/" + autostartfile
    dostart = True

    if len(sys.argv) > 1 and sys.argv[1] == '--kill':
        dostart = False
    if len(sys.argv) > 2 and sys.argv[2] == '--kill':
        dostart = False
    if len(sys.argv) > 1 and sys.argv[1][0] != '-':
        yamlfile = sys.argv[1]

    if not os.path.isfile(yamlfile):
        yamlfile = os.path.expanduser("~") + "/" + autostartfile

    if not os.path.isfile(yamlfile):
        print(f"File {autostartfile} not found!")
        sys.exit(1)

    config = readconfig(yamlfile)
    autostart(config, dostart)
