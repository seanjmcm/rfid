# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 23:32:14 2024

@author: mcmah
"""
#https://pyscard.sourceforge.io/pyscard-wrapper.html#
#https://rpi4cluster.com/python-nfc-writer-reader/

#https://realpython.com/python-gui-tkinter/ --> sudo apt-get install python3-tk
#https://www.reddit.com/r/Crostini/comments/lc5p7n/tkinter_not_opening_a_window_when_using_spyder_3/


#import openpyxl

from smartcard.Exceptions import NoCardException
from smartcard.System import readers
from smartcard.util import toHexString
import sys
from tkinter import *
from tkinter import ttk
from time import sleep
from datetime import datetime
from PIL import Image, ImageTk


count = 0
sleepTime = 0 #
Pcard = "ready"

import csv

#tk._test() #https://www.reddit.com/r/Crostini/comments/lc5p7n/tkinter_not_opening_a_window_when_using_spyder_3/

#def open_popup():
   


def destroy_window():
    win.destroy()
    
def write_to_logfile(uid, logTime):
    
    with open('time.csv', 'a', newline='') as csvfile:
        timewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        timewriter.writerow([uid,logTime ])



tempMessage=0

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
                    
                    logTime = datetime.now()
                    
                    write_to_logfile(uid, logTime)
                    
                    
                    win = Tk()

                    
                    #top= Toplevel(win)
                    win.geometry("550x250")
                    win.title("RFID Tag")
                    tapMess = "UID :" + str(uid) +"\n" + "Thank you for Logging In"
                    
                    #https://stackoverflow.com/questions/74535657/how-can-i-load-an-image-into-a-tkinter-window-canvas
                    image = im = Image.open("D:\mcmah\Google Drive\Learning\lit\dissertation\spo2\correct.png")
                    image = im = Image.open("C:\pilot\correct-sml.png")
                    tk_image = ImageTk.PhotoImage(image)
                    
                    Label(win, text= tapMess, font=('Helvetica 18 bold') ).place(x=130,y=40)
                    
                    Label(win, image=tk_image, compound='center' ).place(x=200,y=100)


                    win.after(3000, destroy_window)
                    win.mainloop()
                    
                    
                   
                
                if sleepTime>1 and Pcard != "ready":
                    sleepTime =0
                    Pcard = "ready"
                    sleep(.1)
                    
                    
                sleepTime =sleepTime+1
        
            except NoCardException:
                if tempMessage > 20:
                    print(reader, 'no card inserted')
                    tempMessage=0
                sleep(0.2)

                tempMessage=tempMessage+1
            
            except :
                print(reader, 'whoops!')
                sleep(0.5)
            count=+1




'''if 'win32' == sys.platform:
    print('press Enter to continue')
    sys.stdin.read(1)'''