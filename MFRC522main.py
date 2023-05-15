#!/usr/bin/env python3
# -*- coding: utf8 -*-

from mfrc522_i2c import MFRC522
import signal

continue_reading = True


# Capture SIGINT for cleanup when script is aborted
def end_read(signal, frame):
    global continue_reading
    print('Ctrl+C captured, ending read')
    continue_reading = False
# Function to generate random set of data for test purposes
def random_data(size=16):
    """ Create random data """
    data = []
    for i in range(size):
        data.append(random.randint(0, 255))
    return (data)


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Reader is located at Bus 1, adress 0x28
i2cBus = 1
i2cAddress = 0x28

# Create an object of the class MFRC522
MFRC522Reader = MFRC522(i2cBus, i2cAddress)

#version = MFRC522Reader.getReaderVersion()
#print(f'MFRC522 Software Version: {version}')

while continue_reading:
    # Scan for cards
    (status, backData, tagType) = MFRC522Reader.scan()
    if status == MFRC522Reader.MIFARE_OK:
        ## print card detected type
        print(f'Card detected, Type: {tagType}')

        # Get UID of the card using identify function
        (status, uid, backBits) = MFRC522Reader.identify()
        #
        if status == MFRC522Reader.MIFARE_OK:
            print(f'Card identified, '
                  f'UID: {uid[0]:02x}:{uid[1]:02x}:{uid[2]:02x}:{uid[3]:02x}')

            # reading UID by using select function
            (status, backData, backBits) = MFRC522Reader.select(uid)
            if status == MFRC522Reader.MIFARE_OK:
                print('Card selected')

                # TODO: Determine 1K or 4K

                # Authenticate
                mode = MFRC522Reader.MIFARE_AUTHKEY1

                blockAddr = 8
                (status, backData, backBits) = MFRC522Reader.authenticate(
                    mode,
                    blockAddr,
                    MFRC522Reader.MIFARE_KEY,
                    uid)
                if (status == MFRC522Reader.MIFARE_OK):
                    print('Card authenticated')

                    # Read data from OLD card
                    (status, backData, backBits) = MFRC522Reader.read(
                        blockAddr)
                    if (status == MFRC522Reader.MIFARE_OK):
                        print(f'Block {blockAddr:02} ', end='')
                        for i in range(0, 16):
                            print(f'{backData[i]:02x} ', end='')
                        print("Read Operation Completed")

                        #continue_reading = False
                        
                        # Write Operation: New Data to Card
                        data = random_data()
                        (status, backData, backBits) = MFRC522Reader.write(
                            blockAddr,
                            data)
                        if (status == MFRC522Reader.MIFARE_OK):
                            print(f'Block {blockAddr:02} ', end='')
                            for i in range(0, 16):
                                print(f'{data[i]:02x} ', end='')
                            print('Write operation Completed')

                            # Read new data from card
                            (status, backData, backBits) = MFRC522Reader.read(
                                blockAddr)
                            if (status == MFRC522Reader.MIFARE_OK):
                                print(f'Block {blockAddr:02} ', end='')
                                for i in range(0, 16):
                                    print(f'{backData[i]:02x} ', end='')
                                print('Read Operation Completed')

                                continue_reading = False
                            else:
                                print('Error while reading new data')
                        else:
                            print('Error while writing new data')
                    else:
                        print('Error while reading old data')

                    # Deauthenticate
                    MFRC522Reader.deauthenticate()
                    print('Card deauthenticated')
                else:
                    print('Authentication error')
