## Read Code

#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import sys

## A total of 10 cards will be used
## Card for Hospital, School, Park, shopping center, /pier/resort/beach area, stadium, amusement park, a choice of food chain, supermarket,
## a choice of land(mountains, lake, rural/farms, street, bridge, monument)
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
        return ID,TXT

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
