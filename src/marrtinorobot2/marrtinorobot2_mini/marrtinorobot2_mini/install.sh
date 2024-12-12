pip install adafruit-blinka
pip install adafruit-circuitpython-servokit
pip install spidev
pip install numpy
pip install pillow


pip install adafruit-blinka
python3 -m venv ~/emo_env
source ~/emo_env/bin/activate
pip install adafruit-circuitpython-board adafruit-circuitpython-servokit pillow spidev
 
sudo apt-get update
sudo apt-get install python3-rpi.gpio -y
sudo apt-get install python3-pil -y
sudo apt-get install python3-spidev -y
sudo apt-get install alsa-utils -y
