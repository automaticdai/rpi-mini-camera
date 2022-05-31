#!/usr/bin/python

import time
from datetime import datetime

import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageOps
from PIL import ImageFilter


from picamera import PiCamera

# Input pins:
L_pin = 27 
R_pin = 23 
C_pin = 4 
U_pin = 17 
D_pin = 22 

A_pin = 5 
B_pin = 6 


GPIO.setmode(GPIO.BCM) 

GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# create a new camera object
camera = PiCamera()
camera.resolution = (128, 64)

while True:
  # capture image
  camera.capture('preview.jpg')
  
  # Load image based on OLED display height.  Note that image is converted to 1 bit color.
  image = Image.open('preview.jpg')
  image = image.filter(ImageFilter.SHARPEN)
  image = image.convert('1')
  # Alternatively load a different format image, resize it, and convert to 1 bit color.
  #image = Image.open('happycat.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
  
  # Display image.
  disp.image(image)
  disp.display()
  
  # wait for capture key
  if GPIO.input(C_pin):
    pass
  else:
    # show a black image
    image = Image.open('black.jpg').convert('1')
    disp.image(image)
    disp.display()
    
    # boost resolution and capture a picture
    camera.resolution = (1280, 720)
    filename_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    camera.capture(filename_str + '.jpg')
    
    # reverse back to LCD resolution 
    camera.resolution = (128, 64)
    time.sleep(0.1)
