#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import time
import logging
from PIL import Image, ImageSequence
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch

# Raspberry Pi pin configuration
RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level=logging.DEBUG)

# Initialize LCD
disp = LCD_2inch.LCD_2inch(spi=SPI.SpiDev(bus, device), spi_freq=10000000, rst=RST, dc=DC, bl=BL)
disp.Init()
disp.clear()
disp.bl_DutyCycle(50)

# Load the GIF file
gif_path = "uhhhhh.gif"  # Path to your uploaded GIF file
gif = Image.open(gif_path)

try:
    while True:
        # Loop through each frame in the GIF
        for frame in ImageSequence.Iterator(gif):
            # Resize frame to fit display dimensions, if needed
            frame = frame.resize((disp.height, disp.width), Image.LANCZOS)
            frame = frame.convert("RGB")  # Convert to RGB if necessary
            disp.ShowImage(frame)
            
            # Wait for the frame duration specified in the GIF
            time.sleep(gif.info['duration'] / 1000.0)  # Convert milliseconds to seconds

except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("Exiting on keyboard interrupt.")
    exit()
