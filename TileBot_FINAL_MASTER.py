import picamera
import picamera.array
import pigpio
import time
import sys
import RPi.GPIO as GPIO
import numpy as np
from PIL import Image
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import adafruit_tcs34725
from mfrc522 import SimpleMFRC522


'''
-------------------------------------------------------------MASTER BUTTON SETUP
'''

GPIO.setmode(GPIO.BCM)
pin = 17 # BCM17
GPIO.setup(pin, GPIO.IN)


'''
-------------------------------------------------------------MOVEMENT FUNCTIONS SETUP
'''

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

'''
-------------------------------------------------------------CAMERA FUNCTION SETUP
'''

def GridPicture():
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


    print(colorList)


    GPIO.cleanup();

'''
-------------------------------------------------------------COLOR SENSOR FUNCTION SETUP
'''

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_tcs34725.TCS34725(i2c)

def readColor():
    # Raw data from the sensor in a 4-tuple of red, green, blue, clear light component values
    # print(sensor.color_raw)

    color = sensor.color
    color_rgb = sensor.color_rgb_bytes
    print(
        "RGB color as 8 bits per channel int: #{0:02X} or as 3-tuple: {1}".format(
            color, color_rgb
        )

    )
    color_idx = ['red', 'blue', 'white']
    color_values = [
    [255,       0,      0],
    [0, 0,      255],
          [0,0,       0]
    ]


    color_rgb = list(color_rgb)
    r = color_rgb[0]
    g = color_rgb[2]
    b = color_rgb[3]

    if(r > b ) and (r > g):
        color = "red"
    elif (b > r ) and (b > g):
        color = "blue"
    else:
        color = "white"

    print("COLOR RBG")
    print(color_rgb)
    print(color)
    if color == 'red':
        destinationFINAL='Hospital';



    # Read the color temperature and lux of the sensor too.
    temp = sensor.color_temperature
    lux = sensor.lux
    print("Temperature: {0}K Lux: {1}\n".format(temp, lux))
    # Delay for a second and repeat.
    time.sleep(1.0)

'''
-------------------------------------------------------------------RFID FUNCTION SETUP
'''
def write():
        print("Place and leave your tag on top of the reader to scan it ")
        text = input("Enter new data to write to the tag, then click Enter: ")
        reader.write(text)
        print("Uploading ...")
        time.sleep(2)
        print("Success! Please remove your tag. ")
        time.sleep(2)
def scan():
        print("Please hold a tag near the reader")
        print("Reading tag in 3 seconds...")
        ID, TXT= reader.read()
        #print("HEXID: %s\nID: %s\nText: %s \n" % (ID,TXT))
        destinationOBJECTIVE = TXT;

def resetIDs():
    print("Please have all cards on you ready to be reset")
    ID, TXT = scan()
    time.sleep(1)
    reader.write("")
    time.sleep(1)

## Create a dictionary that saves the RFID cards that come in the package
## Each card has a unique ID
hosp = {978625901994:"Hospital"}
school = {637887556276:"School"}
zoo = {151558501832:"Zoo"}
mall = {429122065461:"Mall"}
supermarket = {632930121064:"Seatown"}
keys = {hosp, school, zoo, mall, supermarket}
yes_choices = ['yes', 'y']
no_choices = ['no', 'n']
reader = SimpleMFRC522()

def check():
    try:
        while True:
            id, text = scan()
            time.sleep(2)
            if (text==""):
                print("The card scanned --> HEXID: %s\nID: %s\nText: %s \n" % (hex(id),id,text))
                keys.update({id:text})
                print(keys)
                continue
            else:
                print("The card scanned --> HEXID: %s\nID: %s\nText: %s \n" % (hex(id),id,text))
                change = input("Would you like to add/rewrite this card? Please enter yes or no: ")
                if change.lower() in yes_choices:
                    write()
                    continue
                elif change.lower() in no_choices:
                    print("Please remove the card from the reader")
                    continue
                else:
                    print('Please type yes or no')
                    continue

    except KeyboardInterrupt:
            GPIO.cleanup()


'''
-------------------------------------------------------------OLED FUNCTION SETUP
'''

OLED_WIDTH = 128
OLED_HEIGHT = 32
OLED_ADDRESS = 0x3c

# Initialize I2C library busio
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, 
     i2c, addr=OLED_ADDRESS)


# Graphics stuff - create a canvas to draw/write on
image2 = Image.new("1", (oled.width, oled.height))
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw2 = ImageDraw.Draw(image2)
font = ImageFont.load_default()

# Draw a rectangle with no fill, ten pixels thick
draw.rectangle((0, 0, oled.width-1, oled.height-1), 
     outline=10, fill=0)
draw2.rectangle((0,0, oled.width-1, oled.height-1), outline=10, fill=0)
# Draw some text
text = "    success!!! \n    :)"
text2= "    try again!! \n    :("
(font_width, font_height) = font.getsize(text)
draw.text( # position text in center
     (0, 0),  
    text,
    font=font,
    fill=255,
)

# Display image
oled.image(image)
oled.show()


def taskFailOLED():
	draw2.text((0,0),text2, font=font, fill=255,)
	oled.image(image2)
	oled.show()
	time.sleep(0.5)
	#draw =  ImageDraw.Draw(clear)
	#oled.fill(0)
	oled.show()

def taskSuccessOLED():
	draw.text((0,0),text, font=font, fill=255,)
	oled.image(image)
	oled.show()
	time.sleep(2)
	#draw = ImageDraw.Draw(clear)
	#oled.fill(0)
	oled.show()

'''
-------------------------------------------------------------FINAL FUNCTION CALL
'''
try:
  GPIO.wait_for_edge(pin, GPIO.RISING)
  scan();
  GridPicture();
  movement(colorList);
  readColor();
  if destinationOBJECTIVE==destinationFINAL:
      taskSuccessOLED();
  else:
      taskFailOLED();

      
      
      
  
  sys.exit()

