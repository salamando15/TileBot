import pigpio
import time
import sys
import RPi.GPIO as GPIO


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
    print('going forward!');
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
"""
TESTER CODE
switch_direction_forward();
time.sleep(1);
go();
turn_in_place();
time.sleep(1);
switch_direction_backward();
time.sleep(1);
go();
"""

GPIO.cleanup();

    
