#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys 
import time
import logging
import random
import spidev as SPI
from PIL import Image, ImageDraw
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

# Set display dimensions
width = disp.height
height = disp.width

# Eye position and size
eye_radius = 35
eye_y = height // 2 - 40
left_eye_x = width // 4
right_eye_x = 3 * width // 4

# Helper function to draw eyes
def draw_eyes(draw, left_eye_offset=0, right_eye_offset=0, eye_fill="WHITE", eye_tilt=0, eyes_closed=False, eye_shape="round"):
    if eyes_closed:
        # Closed eyes as lines
        draw.line((left_eye_x - eye_radius + left_eye_offset, eye_y, left_eye_x + eye_radius + left_eye_offset, eye_y), fill=eye_fill, width=3)
        draw.line((right_eye_x - eye_radius + right_eye_offset, eye_y, right_eye_x + eye_radius + right_eye_offset, eye_y), fill=eye_fill, width=3)
    else:
        if eye_shape == "round":
            # Open round eyes
            draw.ellipse((left_eye_x - eye_radius + left_eye_offset, eye_y - eye_radius, left_eye_x + eye_radius + left_eye_offset, eye_y + eye_radius), fill=eye_fill)
            draw.ellipse((right_eye_x - eye_radius + right_eye_offset, eye_y - eye_radius, right_eye_x + eye_radius + right_eye_offset, eye_y + eye_radius), fill=eye_fill)
        elif eye_shape == "tilted":
            # Tilted eyes for sad expression
            draw.pieslice((left_eye_x - eye_radius + left_eye_offset, eye_y - eye_radius + eye_tilt, left_eye_x + eye_radius + left_eye_offset, eye_y + eye_radius + eye_tilt), start=20, end=160, fill=eye_fill)
            draw.pieslice((right_eye_x - eye_radius + right_eye_offset, eye_y - eye_radius + eye_tilt, right_eye_x + eye_radius + right_eye_offset, eye_y + eye_radius + eye_tilt), start=20, end=160, fill=eye_fill)

# Emotion-specific functions
def draw_normal_face():
    for offset in range(-30, 31, 5):  # Move eyes to the right
        image = Image.new("RGB", (width, height), "BLACK")
        draw = ImageDraw.Draw(image)
        
        # Randomize blinking
        blink = random.choice([True, False]) and offset == 0

        # Draw moving eyes with random blinking
        draw_eyes(draw, left_eye_offset=offset, right_eye_offset=offset, eyes_closed=blink)
        
        # Show image
        disp.ShowImage(image)

    for offset in range(30, -31, -5):  # Move eyes back to the left
        image = Image.new("RGB", (width, height), "BLACK")
        draw = ImageDraw.Draw(image)
        
        # Randomize blinking
        blink = random.choice([True, False]) and offset == 0

        # Draw moving eyes with random blinking
        draw_eyes(draw, left_eye_offset=offset, right_eye_offset=offset, eyes_closed=blink)
        
        # Show image
        disp.ShowImage(image)

def draw_happy_face():
    image = Image.new("RGB", (width, height), "BLACK")
    draw = ImageDraw.Draw(image)
    draw_eyes(draw)
    mouth_coords = (left_eye_x - 20, eye_y + 60, right_eye_x + 20, eye_y + 80)
    draw.arc(mouth_coords, start=0, end=180, fill="WHITE", width=3)
    disp.ShowImage(image)

def draw_sad_face():
    # Transition from round eyes to tilted eyes
    for tilt in range(0, 15, 5):
        image = Image.new("RGB", (width, height), "BLACK")
        draw = ImageDraw.Draw(image)
        draw_eyes(draw, eye_tilt=tilt, eye_shape="tilted")
        mouth_coords = (left_eye_x - 20, eye_y + 80, right_eye_x + 20, eye_y + 100)
        draw.arc(mouth_coords, start=180, end=0, fill="WHITE", width=3)  # Downturned mouth
        disp.ShowImage(image)
        time.sleep(0.05)
        
    # Final sad face with fully tilted eyes
    image = Image.new("RGB", (width, height), "BLACK")
    draw = ImageDraw.Draw(image)
    draw_eyes(draw, eye_tilt=15, eye_shape="tilted")
    draw.arc(mouth_coords, start=180, end=0, fill="WHITE", width=3)
    disp.ShowImage(image)

def draw_curiosity_face():
    image = Image.new("RGB", (width, height), "BLACK")
    draw = ImageDraw.Draw(image)
    draw_eyes(draw, left_eye_offset=3, right_eye_offset=-3)  # Slight inward tilt
    mouth_coords = (left_eye_x - 10, eye_y + 70, right_eye_x + 10, eye_y + 80)
    draw.arc(mouth_coords, start=0, end=180, fill="WHITE", width=3)
    disp.ShowImage(image)

def draw_angry_face():
    image = Image.new("RGB", (width, height), "BLACK")
    draw = ImageDraw.Draw(image)
    draw_eyes(draw, eye_tilt=15)  # Tilted, half-closed eyes for anger
    mouth_coords = (left_eye_x - 20, eye_y + 90, right_eye_x + 20, eye_y + 110)
    draw.line((mouth_coords[0], mouth_coords[1], mouth_coords[2], mouth_coords[3]), fill="WHITE", width=3)  # Straight line for angry mouth
    disp.ShowImage(image)

try:
    while True:
        # Display each emotion with a short delay
        draw_normal_face()
        time.sleep(0.5)

        draw_happy_face()
        time.sleep(0.5)

        draw_sad_face()
        time.sleep(0.5)

        draw_curiosity_face()
        time.sleep(0.5)

        # Transition from normal to angry
        draw_angry_face()
        time.sleep(1)  # Hold angry expression

except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("Exiting on keyboard interrupt.")
    exit()
