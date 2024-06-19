# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 23:32:14 2024

@author: mcmah
"""
#https://pyscard.sourceforge.io/pyscard-wrapper.html#
#https://rpi4cluster.com/python-nfc-writer-reader/
#https://www.mutek.com/mutek-pcsc-readers-pcsc-lite-linux/

from smartcard.Exceptions import NoCardException
from smartcard.System import readers
from smartcard.util import toHexString
import sys

from time import sleep

count = 0
sleepTime = 0 #
Pcard = "ready"

while True:
    count = 0
    for reader in readers():
        while count <1:
            try:
                connection = reader.createConnection()
                connection.connect()
                #print(reader, toHexString(connection.getATR()))
                        # # Get card UID
                SELECT = [0xFF, 0xCA, 0x00, 0x00, 0x00]
                response, sw1, sw2 = connection.transmit(SELECT)
                uid = toHexString(response)
                if Pcard == "ready":
                    print(f"Card UID t: {uid}")
                    Pcard = "not ready"
                    sleepTime =0
                sleep(1)
                
                if sleepTime>2 and Pcard != "ready":
                    sleepTime =0
                    Pcard = "ready"
                    
                sleepTime =sleepTime+1
        
            except NoCardException:
                print(reader, 'no card inserted')
                sleep(0.5)
                
            count=+1

'''if 'win32' == sys.platform:
    print('press Enter to continue')
    sys.stdin.read(1)'''
