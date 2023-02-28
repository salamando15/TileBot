#import all libraries
import pigpio
import time
import sys
import RPi.GPIO as GPIO

#pin assignment
pi=pigpio.pi();
leftmotorpin=12;
rightmotorpin=13;
Ain1=9;
Ain2=11;
Bin1=8;
Bin2=25;

#set pinMode and all pins as outputs
GPIO.setmode(GPIO.BCM);
GPIO.setup(Ain1, GPIO.OUT);
GPIO.setup(Ain2, GPIO.OUT);
GPIO.setup(Bin1, GPIO.OUT);
GPIO.setup(Bin2, GPIO.OUT);


def go():
    pi.hardware_PWM(leftmotorpin, 100, 500000);
    pi.hardware_PWM(rightmotorpin, 100, 500000);
    print('going forward!');
    time.sleep(1);
    stop();


def stop():
    print("stopping");
    #stop motors
    pi.hardware_PWM(leftmotorpin, 100, 000000); 
    pi.hardware_PWM(rightmotorpin, 100, 000000); 


def Lturn():
     print('turning left');
     pi.hardware_PWM(leftmotorpin, 100, 500000); #only left motor spins
     time.sleep(1);

def Rturn():
     print('turning right');
     pi.hardware_PWM(rightmotorpin, 100, 500000); #only right motor spins
     time.sleep(1);
     stop();

def switch_direction_forward():
     #set in1 high for both motors, in2 low for both motors 
     GPIO.output(Ain1, GPIO.HIGH);
     GPIO.output(Ain2, GPIO.LOW);
     GPIO.output(Bin1, GPIO.HIGH);
     GPIO.output(Bin2, GPIO.LOW);
     print('motors moving forward');
     #green LED lights up on polarity switch

def switch_direction_backward():
     #reverse motor polarities
     #in1 low for both motors, in2 high for both motors
     GPIO.output(Ain1, GPIO.LOW);
     GPIO.output(Ain2, GPIO.HIGH);
     GPIO.output(Bin1, GPIO.LOW);
     GPIO.output(Bin2, GPIO.HIGH);
     print('motors moving backward');
     #red LED lights up on polarity switch

def turn_in_place():
     #motor polarities alternated, 
     #one will rotate clockwise as the 
     #other rotates cpunterclockwise
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

#cleanup!
GPIO.cleanup();

    
