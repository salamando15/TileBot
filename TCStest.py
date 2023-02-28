
#!/usr/bin/python
import smbus
import time
import RPi.GPIO as GPIO
import sys

bus = smbus.SMBus(1) ## i2c device 1 - GPIO pins 2 and 3
color_ADD = 0x29  ## sensor address

### Configuration Registers
ENABLE = 0x00
ATIME = 0x01   ## ADC integration time reset value -> 0XFF
WTIME = 0x03 ## wait time can range from 2.78 ms to 8.54 sec

CONTROL = 0x0F ## Gain control
CONFIG1 = 0x0D  ##configuration 1 register responsible for LED current, prox/color gain control
ID = 0x12  ## device ID
STATUS = 0x13  ## status register

## Interrupts Registers
AILTL = 0x04  ## ALS interrupt low thres low byte
AILTH = 0x05 ## ALS interrupt low thres highbyte
AIHTL = 0x06 ## ALS interrupt high thres low byte
AIHTH = 0x07## ALS interrupt high thres high byte
PERS = 0x0C  ## Persistence Filters interrupt

## Color/ALS Registers
CDATAL = 0x14 ## Clear Channel low byte data
CDATAH = 0x15 ##Clear Channel low byte data
RDATAL = 0x16  ##Red Color Channel low byte data
RDATAH = 0x17 ##Red Color Channel high byte data
GDATAL = 0x18 ## Green  Color Channel low byte data
GDATAH = 0x19 ##Green Color Channel high byte data
BDATAL = 0x1A ##Blue Color Channel low byte data
BDATAH = 0x1B ##Blue Color Channel high byte data

## basic read and write functions
## read function that returns value success attempt
## write operation with parameters: device address, register address, value to write
#       bus.write_byte_data(device, )
## read operation with 2 parameters: device addres, register address
#d      data = bus.read_byte_data(device, register
def read(reg):
    #if(!write(reg)) return
    val = bus.read_byte_data(color_ADD, reg)
    time.sleep(0.5)
    return val
## write function: smbus function has parameters device address, register address, value to write
## returns
def write(reg, val):
    ## command 
    temp = 5 << 5
    test = reg | temp
    bus.write_byte_data(color_ADD, test, val)
    time.sleep(0.5)
    val = bus.read_byte_data(color_ADD, reg)
    return val
## start up connection
def begin():

    GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD
    GPIO.setup(17, GPIO.OUT) # set a port/pin as an output
    GPIO.setup(27,GPIO.OUT)  ## GPIO Pin 27 as the input to the LED
    GPIO.output(17, 1)       # set port/pin value to 1/GPIO.HIGH/True
    GPIO.output(27, 1)        # et port/pin value to 0/GPIO.LOW/True

    #write(GPULSE,0x8F)  ## set pulse length  to 16 us(bits 7-6) and number of pulses to 16(bits 5-0
    #write(PPULSE,0x8F)
    enablePower()
    time.sleep(0.5)## Datasheet recommends
    print("Turning on Power ", read(ENABLE))
    check = read(ID)
    if (check != 0x44):
         return False
    print("Starting Program : Raspberry Pi connecting to ADPS9960 with ID ", check)
    enableWait()
    print("Turning ON Wait Feature ", read(ENABLE))
    time.sleep(0.5)
    write(WTIME, 0xD5) ## set wait time to 204 ms
    print("Setting wait time to 204 ms : ", read(WTIME))
     ## ADC integration time parameters
    write(ATIME,0xD5) ## 42 integration cycle --> coutn up to 66804
    print("Setting ADC time to 42 integration cycles with 101 ms integration time: ", read(ATIME))
     ## ADC Gain parameters
    write(CONTROL,0x02) ## Gain of 16x
    print("Setting Gain of 16")
    time.sleep(0.5)


## end program
def end():
    write(ENABLE,0x00)

## enable/disable power
def enablePower():
    check = read(ENABLE)
    test = 0b00000001
    if ((check & test)!=0):
        return True
    val = (check | test)
    return write(ENABLE, val)

def disablePower():
    check = read(ENABLE)
    test = 0b00000001
    if ((check & test)==0):
        return True
    val = (check & 0b11111110)
    return write(ENABLE, val)

## Enable/Disable Wait Registers
def enableWait():
    check = read(ENABLE)
    test = 0b00001000
    if ((check & test)!=0):
        return True
    val = (check | test)
    return write(ENABLE, val)

def disableWait():
    check = read(ENABLE)
    test = 0b00001000
    if ((check & test)==0):
        return True
    val = (check & 0b11110111)
    return write(ENABLE, val)


## Enable/Disable Color sensor
def enableColor():
    print("Turning on Color Sensor")
    check = read(ENABLE)
    test = 0b00000010
    if ((check & test)!=0):
        return True
    val = (check | test)
    return write(ENABLE, val)

def disableColor():
    check = read(ENABLE)
    test = 0b00000010
    if ((check & test)==0):
        return True
    val = (check & 0b11111101)
    return write(ENABLE, val)

### Check for color sensor status and reading color values

def ColorAvailable():
    enableColor()
    time.sleep(0.003)
    check = read(STATUS)
    if (check & 0b00000001):
        return 1
    else:
        return 0

def readColors():
    colors = []
    print("Extracting Color Values")

    clearData = read(CDATAH)
    clearData = clearData << 8
    clearData |= read(CDATAL)

    redData = read(RDATAH)
    print("High Read Data: ", redData)
    redData = redData << 8
    print("High Read Data Shifted: ", redData)
    redData |= read(RDATAL)
    print("High Read Data Bitwise with Low Byte ", redData)

    greenData = read(GDATAH)
    greenData = greenData << 8
    greenData |= read(GDATAL)

    blueData = read(BDATAH)
    blueData = blueData << 8
    blueData |= read(BDATAL)

    colors.append(redData)
    colors.append(greenData)
    colors.append(blueData)
    colors.append(clearData)
    print(colors)
    disableColor()
    return colors

def colorTemp(r, g, b):
    # Converts the raw R/G/B values to color temperature in degrees Kelvin"""

    #  1. Map RGB values to their XYZ counterparts.
    #   Based on 6500K fluorescent, 3000K fluorescent
    #    and 60W incandescent values for a wide range.
    #    Note: Y = Illuminance or lux
    x = (-0.14282 * r) + (1.54924 * g) + (-0.95641 * b)
    y = (-0.32466 * r) + (1.57837 * g) + (-0.73191 * b)
    z = (-0.68202 * r) + (0.77073 * g) + (0.56332 * b)

    #  2. Calculate the chromaticity co-ordinates
    xchrome = x / (x + y + z)
    ychrome = y / (x + y + z)

    #  3. Use   to determine the CCT
    n = (xchrome - 0.3320) / (0.1858 - ychrome)

    #  4. Calculate the final CCT
    cct = (449.0 * pow(n, 3)) + (3525.0 * pow(n, 2)) + (6823.3 * n) + 5520.33

    #    Return the results in degrees Kelvin
    return cct

## Set Functions ##
def ambientLevel(r, g, b):

    #   This only uses RGB ... how can we integrate clear or calculate lux
    #   based exclusively on clear since this might be more reliable?
    illuminance = (-0.32466 * r) + (1.57837 * g) + (-0.73191 * b)

    return illuminance
def setIntTime(x): ## set integration time

    ## Example: for a 100 ms integration time the device needs to be converted
    val = 256-round(x/0.0024)
    return write(ATIME, val)


begin()
lastUpdate = 0
while True:
    if ColorAvailable():
        extract = readColors()
        red = extract[0]
        green = extract[1]
        blue = extract[2]
        clear = extract[3]
        print("Red :", red )
        print("Green :", green )
        print("Blue :", blue)
        print("Clear :", clear)
        ## update every four seconds
        milli = int(time.time()*1000)
        if(milli - lastUpdate > 4000):
            lastUpdate = milli
            kelvin = colorTemp(red, green, blue)
            brightness = ambientLevel(red, green, blue)
            print("Color temperature: ", kelvin)
            print("Ambient Light Level: ", brightness)
            print("Last Updated : ", lastUpdate)
        time.sleep(3)
