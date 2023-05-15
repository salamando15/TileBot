import pigpio
import time
import sys
import RPi.GPIO as GPIO
import numpy as np

#import pandas as pd
from PIL import Image
#import matplotlib.pyplot as plt


pi=pigpio.pi();
leftmotorpin=12;
rightmotorpin=13;
Ain1=9;
Ain2=11;
Bin1=8;
Bin2=25;

GPIO.setmode(GPIO.BCM);
GPIO.setup(Ain1, GPIO.OUT);
GPIO.setup(Ain2, GPIO.OUT);
GPIO.setup(Bin1, GPIO.OUT);
GPIO.setup(Bin2, GPIO.OUT);

def go():
    pi.hardware_PWM(leftmotorpin, 100, 500000);
    pi.hardware_PWM(rightmotorpin, 100, 500000);
    print('going in motor direction!');
    time.sleep(3);
    stop();


def stop():
    print("stopping");
    pi.hardware_PWM(leftmotorpin, 100, 000000);
    pi.hardware_PWM(rightmotorpin, 100, 000000);


def Lturn():
     print('turning left');
     pi.hardware_PWM(leftmotorpin, 100, 500000);
     time.sleep(1);

def Rturn():
     print('turning right');
     pi.hardware_PWM(rightmotorpin, 100, 500000);
     time.sleep(1);
     stop();

def switch_direction_forward():
     GPIO.output(Ain1, GPIO.HIGH);
     GPIO.output(Ain2, GPIO.LOW);
     GPIO.output(Bin1, GPIO.HIGH);
     GPIO.output(Bin2, GPIO.LOW);
     print('motors moving forward');

def switch_direction_backward():
     GPIO.output(Ain1, GPIO.LOW);
     GPIO.output(Ain2, GPIO.HIGH);
     GPIO.output(Bin1, GPIO.LOW);
     GPIO.output(Bin2, GPIO.HIGH);
     print('motors moving backward');

def turn_in_place():
     GPIO.output(Ain1, GPIO.LOW);
     GPIO.output(Ain2, GPIO.HIGH);
     GPIO.output(Bin1, GPIO.HIGH);
     GPIO.output(Bin2, GPIO.LOW);
     pi.hardware_PWM(leftmotorpin, 100, 500000);
     pi.hardware_PWM(rightmotorpin, 100, 500000);
     print('turning in place!');
     time.sleep(3);
     stop();


def movement(tile_colors):
    for instruction in tile_colors:
        print('instruction color:', instruction);
        if instruction == 'red':
            switch_direction_forward();
            go();
        elif instruction == 'green':
            switch_direction_forward();
            Lturn();
        elif instruction == 'blue':
            switch_direction_forward();
            Rturn();
        elif instruction == 'yellow':
            switch_direction_backward();
            go();
        time.sleep(2);
        




img_pil = Image.open( 'camera_output.jpg' )

img = np.array(img_pil)

tile_positions = [
    {'top': 5, 'bottom': 15, 'left': 5,  'right': 15},
    {'top': 0, 'bottom': 20, 'left': 20, 'right': 40},
    {'top': 0, 'bottom': 20, 'left': 40, 'right': 60},
    {'top': 0, 'bottom': 20, 'left': 60, 'right': 80}
]


color_idx = ['red', 'blue', 'green', 'yellow']
color_values = [
    [255,	0,	0],
    [0,	0,	255],
	  [0,255,	0],
    [255,	255,	0]
]
N = len(color_values)
color_values = np.array(color_values)

colorList = []
for t_idx, t in enumerate(tile_positions):
  tile_rgb = img[ t['top']: t['bottom'], t['left']:t['right']  ]
  tile_m = np.mean(tile_rgb, axis=(0,1))

  rgb_array = np.tile(tile_m, (N,1))

  result_array = color_values - rgb_array

  distance_array = np.linalg.norm(result_array, axis=1)

  min_index = np.argmin(distance_array)



  print(t_idx, tile_rgb.shape, tile_m)
  print(color_idx[min_index])

  colorList.append(color_idx[min_index])
  #colorList.append(recognize_color(tile_m[0],tile_m[1],tile_m[2]))

  # next, use https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html to compute Euclidian dist to an array of colors
  # color array is N rows by 3 columns (R, G, B), the result should have N rows

  # once you have a distance array with N rows, use https://numpy.org/doc/stable/reference/generated/numpy.argmin.html 
  # this will return the index of the minimum distance

print(colorList)


movement(colorList);




GPIO.cleanup();
