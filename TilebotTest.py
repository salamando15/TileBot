import pigpio
import time
import sys

pi=gpio.pi();
pins={'left':12, 'right':13};

def forward():
    pi.hardware_PWM(pins['left'], 50, 55*10000);
    pi.hardware_PWM(pins['right'], 50, 55*10000);
    print('going forward!');
    

    
