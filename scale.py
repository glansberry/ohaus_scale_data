#!/usr/bin/python2
#
# you must install pyserial (sudo easy_install pyserial)
import serial
import time
#scale = serial.Serial('/dev/tty.usbserial-00002014', 9600, bytesize=8, stopbits=1, timeout=None)
with serial.Serial() as scale:
    scale.baudrate = 9600
    scale.parity = serial.PARITY_NONE
    scale.bytesize = 8
    scale.stopbits = 1
    scale.timeout = 10
    scale.port = '/dev/ttyUSB0'
    scale.open()

    time.sleep(0.1)
    scale.write(b'0P\r\n')  #auto print off
    time.sleep(0.5)
    print scale.readline()
    scale.write(b'1U\r\n')  #set to grams
    time.sleep(0.5)
    print scale.readline()
    scale.write(b'SLP\r\n')  #autoprint on nonzero stability
    time.sleep(0.5)
    print scale.readline()

    with open('weigh_data.csv', 'w+') as f:
        while True:
            grams = scale.readline()
            grams = grams.lstrip()
            scale_time = time.time()
            if grams.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-')):
                g = grams.split()
                scale_out = str(str(scale_time) + ',' + g[0] + '\n')
                print scale_out
                f.write(scale_out)
            f.close()
    scale.close()
