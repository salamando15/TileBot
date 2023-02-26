
#!/usr/bin/python
import smbus
import time
import RPI.GPIO as GPIO

bus = smbus.SMBus(1) ## i2c device 1 - GPIO pins 2 and 3
color_ADD = 0x39  ## sensor address

## REGISTER ADRESSES: 8 bit addresses ##
## RAM : 0x00 - 0x7F
## Registers : 0x80 - 0xFF

### Configuration Registers
ENABLE = 0x80
ATIME = 0x81   ## ADC integration time reset value -> 0XFF
WTIME = 0x83 ## wait time can range from 2.78 ms to 8.54 sec

CONTROL = 0x8F ## Gain control
CONFIG1 = 0x8D  ##configuration 1 register responsible for LED current, prox/color gain control
CONFIG2 = 0x90 ## configuration 2 register responsible for prox sat/clear sat interrupts, and LED Boost
CONFIG3 = 0x9F ## configuration 3 register
ID = 0x92  ## device ID
STATUS = 0x93  ## status register

## Interrupts Registers
AILTL = 0x84  ## ALS interrupt low thres low byte
AILTH = 0x85 ## ALS interrupt low thres highbyte
AIHTL = 0x86 ## ALS interrupt high thres low byte
AIHTH = 0x87## ALS interrupt high thres high byte
PILT = 0x89  ## Proximity interrupt low threshold
PIHT = 0x8B ## Proximity interrupt high threshold
PERS = 0x8C  ## Persistence Filters interrupt
IFORCE = 0xE4  ## force interrupt
PICLEAR = 0xE5  ## prox interrupt clear
CICLEAR = 0xE6  ## ALS clear channel interrupt clear

## Proximity Registers
PPULSE = 0x8E  ## Proximity pulse count and length
PDATA = 0x9C ## proximity data register
POFFSET_UR = 0x9D  ## prox offset for up and right photodiodes
POFFSET_DL = 0x9E  ## prox offset for down and left photodiodes

## Color/ALS Registers
CDATAL = 0x94 ## Clear Channel low byte data
CDATAH = 0x95 ##Clear Channel low byte data
RDATAL 0x96  ##Red Color Channel low byte data
RDATAH = 0x97 ##Red Color Channel high byte data
GDATAL = 0x98 ## Green  Color Channel low byte data
GDATAH = 0x99 ##Green Color Channel high byte data
BDATAL = 0x9A ##Blue Color Channel low byte data
BDATAH = 0x9B ##Blue Color Channel high byte data

## Gesture Registers
GPENTH = 0xA0 ## gesture prox enter thres
GEXTH = 0xA1 ## gesture prox exit thres
GCONF1 = 0xA2 ## gesture configuration 1
GCONF2 = 0xA3 ## gesture configuration 2
GOFFSET_U = 0xA4  ## gesture up offset
GOFFSET_D = 0xA5 ## gesture down offset
GPULSE = 0xA6 ## gesture pulse count and length
GOFFSET_L = 0xA7 ## gesture left offset
GOFFSET_R = 0xA9 ## gesture right offset
GCONF3 = 0xAA ## gesture configuration 3
GCONF4 = 0xAB ## gesture configuration 4
GFLVL = 0xAE ## Gesture FIFO level
GSTATUS = 0xAF  ## gesture status
AICLEAR = 0xE7  ## All non gesture interrupt clear
GFIFO_U = 0xFC  ## gesture FIFO UP value
GFIFO_D = 0xFD  ## gesture FIFO DOWN value
GFIFO_L = 0xFE  ## gesture FIFO LEFT value
GFIFO_R = 0xFF  ## gesture FIFO RIGHT value


## ENABLE Register
# MSB is reserved --> 0
# Bit 6 enables gesture sensor
# Bit 5 enables proximity sensor
# Bit 4 enables ALS interrupts
# Bit 3 enables wait timer
# Bit 2 enables proximity detection
# Bit 1 enables Color/ALS function
# Bit 0 enables oscillator to run device (1 for ON, 0 for low power sleep mode)

## Color/ALS function
# bit 2 of ENABLE fn enables ALS
## bit 6 oF CONFIG2 turns on CLEAR DIODE SATURATION INTERRUPT
## bit 7 of status register CLEARS DIODE SATURATION

## Config address -->
commandA = 0b00011011 ## wait enable, ALS and interupts ON

## basic read and write functions
## read function that returns value success attempt
## write operation with parameters: device address, register address, value to write
#       bus.write_byte_data(device, )
## read operation with 2 parameters: device addres, register address
#d      data = bus.read_byte_data(device, register
def read(reg):
    #if(!write(reg)) return
    val = bus.read_byte_data(color_ADD, reg)
    return val
## write function: smbus function has parameters device address, register address, value to write
## returns
def write(val):
    bus.write_byte()
def write(reg, val):
    bus.write_byte_data(color_ADD, reg, val)
    val = bus.read_byte_data(color_ADD, reg)
    return val
## start up connection
def begin():
    check = read(ID)
    if (check != 0xAB) return false
    write(WTIME, 0xFF) ## set wait time to 2.78 ms
    write(GPULSE,0x8F)  ## set pulse length  to 16 us(bits 7-6) and number of pulses to 16(bits 5-0
    write(PPULSE,0x8F)
    enablePower()
    enableWait()
     ## ADC integration time parameters
     write(ATIME,256-(10/2.78))
     ## ADC Gain parameters
     write(CONTROL,0x02)

     time.sleep(3)
     ## turnPowerON
     enablePower()

     GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD
     GPIO.setup(17, GPIO.output) # set a port/pin as an output
     GPIO.output(17, 1)       # set port/pin value to 1/GPIO.HIGH/True
     #GPIO.output(17, 0)        # et port/pin value to 0/GPIO.LOW/True

## end program
def end():
    write(ENABLE,0x00)

## enable/disable power
def enablePower():
    check = read(ENABLE)
    test = 0b00000001
    if ((check & test)!=0) return true
    val = (check |= test)
    return write(ENABLE, val)

def disablePower():
    check = read(ENABLE)
    test = 0b00000001
    if ((check & test)==0) return true
    val = (check &= 0b11111110)
    return write(ENABLE, val)

## Enable/Disable Wait Registers
def enableWait():
    check = read(ENABLE)
    test = 0b00001000
    if ((check & test)!=0) return true
    val = (check |= test)
    return write(ENABLE, val)
}
def disableWait():
    check = read(ENABLE)
    test = 0b00001000
    if ((check & test)==0) return true
    val = (check &= 0b11110111)
    return write(ENABLE, val)
}
## Enable/Disable Gesture Sensor
def enableGesture():
    check = read(ENABLE)
    test = 0b01000000
    if ((check & test)!=0) return true
    val = (check |= test)
    return write(ENABLE, val)

def disableGesture():
    check = read(ENABLE)
    test = 0b01000000
    if ((check & test)==0) return true
    val = (check &= 0b10111111)
    return write(ENABLE, val)

## Enable/Disable Proximity Sensor
def enableProx():
    check = read(ENABLE)
    test = 0b00000100
    if ((check & test)!=0) return true
    val = (check |= test)
    return write(ENABLE, val)

def disableProx():
    check = read(ENABLE)
    test = 0b00000100
    if ((check & test)==0) return true
    val = (check &= 0b11111011)
    return write(ENABLE, val)

## Enable/Disable Color sensor
def enableColor():
    check = read(ENABLE)
    test = 0b00000010
    if ((check & test)!=0) return true
    val = (check |= test)
    return write(ENABLE, val)

def disableColor():
    check = read(ENABLE)
    test = 0b00000010
    if ((check & test)==0) return true
    val = (check &= 0b11111101)
    return write(ENABLE, val)


### Check for color sensor status and reading color values

def ColorAvailable():
    enableColor()
    check = read(STATUS)
    if (check & 0b00000001):
        return 1
    else:
        return 0

def readColors():
    colors = []
    color.append(read(CDATAL))
    color.append(read(CDATAL))
    color.append(read(CDATAH))
    color.append(read(CDATAH))

    disableColor()
    return colors

## proximity sensor check and read
def proxAvailable():
    enableProx()
    check = read(STATUS)
    test = 0b00000010
    if (check & test):
        return 1
    else:
        return 0

def readProx():
    check = read(PDATA)
    disableProx()
    val = (255-check)
    return val


begin()
enableColor()
lastUpdate = 0
while True:
    if ColorAvailable():
        extract = readColors()
        print("Red :", extract[0])
        print("Green :", extract[1])
        print("Blue :", extract[2])
        print("Clear :", extract[3])

        ## update every second
    milli = int(time.time()*1000)
    if(milli - lastUpdate > 1000):
        lastUpdate = milli
        print("Last Updated : ", lastUpdate)
