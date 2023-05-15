import time
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

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
text = "    /\______/\ \n    ( O  w  O )"
text2= "    _/\____/\_ \n    ( -  o  - )"
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


while (True):
	draw2.text((0,0),text2, font=font, fill=255,)
	oled.image(image2)
	oled.show()
	time.sleep(0.5)
	#draw =  ImageDraw.Draw(clear)
	#oled.fill(0)
	oled.show()
	draw.text((0,0),text, font=font, fill=255,)
	oled.image(image)
	oled.show()
	time.sleep(2)
	#draw = ImageDraw.Draw(clear)
	#oled.fill(0)
	oled.show()	
