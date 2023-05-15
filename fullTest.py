import picamera
import picamera.array
import pigpio
import time
import sys
import RPi.GPIO as GPIO
import numpy as np
from PIL import Image


pi=pigpio.pi();
leftmotorpin=12;
rightmotorpin=13;
Ain1=5;
Ain2=6; 
Bin1=16;
Bin2=26;

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
        
with picamera.PiCamera() as camera:
    camera.resolution = (100, 100)
    time.sleep(2)
    image = np.empty((128, 112, 3), dtype=np.uint8)
    camera.capture(image, 'rgb')
    camera.capture('camera_output.jpg')
    image = image[:100, :100]

img_pil = Image.open('camera_output.jpg')
img = np.array(img_pil)

tile_positions = [
    {'top': 15, 'bottom': 25, 'left': 15,  'right': 20},
    {'top': 15, 'bottom': 35, 'left': 30, 'right': 40},
    {'top': 15, 'bottom': 25, 'left': 45, 'right': 55},
    {'top': 15, 'bottom': 25, 'left': 60, 'right': 70}
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
  print(result_array)
  print('result array')

  distance_array = np.linalg.norm(result_array, axis=1)
  print(distance_array)
  print('distance_array')
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
