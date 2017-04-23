#!/usr/bin/python2
#
# you must install pyserial (sudo easy_install pyserial)
import serial
import time
#scale = serial.Serial('/dev/tty.usbserial-00002014', 9600, bytesize=8, stopbits=1, timeout=None)

save_file = time.strftime("weigh_data%Y%m%d%H%M%S.csv", time.localtime())
with serial.Serial() as scale:
    scale.baudrate = 9600
    scale.parity = serial.PARITY_NONE
    scale.bytesize = 8
    scale.stopbits = 1
    scale.timeout = 1
    scale.port = '/dev/ttyUSB0'
    scale.open()
    scale.reset_input_buffer()
    print "Initializing Scale - please wait"

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

    print "Scale Initialized - appending to file: " + save_file
    counter = 0;
    with open(save_file, 'w+') as f:
        while True:
            if scale.in_waiting > 3:
                grams = scale.readline()
                grams = grams.strip()
                scale_time = time.time()
                scale_time = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime())
                if grams.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-')):
                    counter += 1
                    g = grams.split()
                    scale_out = str(str(counter) + ',' + str(scale_time) + ',' + g[0] + '\n')
                    f.write(scale_out)
                    print str(counter) + ': ' + grams
            else: time.sleep(0.1)
        f.close()
    scale.close()
