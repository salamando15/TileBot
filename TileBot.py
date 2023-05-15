def info():  
    '''Prints a basic library description'''
    print("Software library for the TileBot project.")
    
#Camera Functions
def cameraCapture():
    pass
def readTiles():
    pass
def updateTileState():
    pass

#Color Sensor Functions

## turn on color sensor
def active():
    pass
## set integration time 
def integration_time(self, val: float):
    pass
## get gain value that is preset 
def gain(self):
    pass
## change gain value 
def gain(self, val: int):
    pass
## read raw contents of red,green,blue, clear channels with values 0 to 65535
def color_raw(self):
    pass
## read RGB color detected by sensor that returns an integer with 8 bits per channel --> 0xFF0000 or 0x00FF00 or 0x0000FF
def color():
    pass
## read RGB colors detected by sensor with values 0-255
def color_rgb_bytes(self):

## Temperature and Luminance reading functions
def _temperature_and_lux_dn40(self) -> Tuple[float, float]:
    pass
def lux(self):
    pass
## The color temperature in Kelvin 
def color_temperature(self):
    pass


#Robot Movement Functions
def go():
    pass;

def stop():
    pass;

def Lturn():
     pass;

def Rturn():
     pass;

def switch_direction_forward():
     pass;

def switch_direction_backward():
    pass;

def turn_in_place():
     pass;
