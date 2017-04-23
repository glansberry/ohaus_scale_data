#!/usr/bin/python2
#
# you must install pyserial (sudo easy_install pyserial)
#
# Scout pro manual with commands here: http://dmx.ohaus.com/WorkArea/downloadasset.aspx?id=3600
# Scout SPX manusl http://dmx.ohaus.com/WorkArea/showcontent.aspx?id=4294974227

import serial
import time
import sys

if len(sys.argv) < 2:
    print 'missing port'
    exit()

port = sys.argv[1]
save_file = time.strftime("weigh_data%Y%m%d%H%M%S.csv", time.localtime())
with serial.Serial() as scale:
    scale.baudrate = 9600
    scale.parity = serial.PARITY_NONE
    scale.bytesize = 8
    scale.stopbits = 1
    scale.timeout = 1
    scale.port = port
    scale.open()
    scale.reset_input_buffer()
    print "Initializing Scale - please wait"

    scale.write(b'1U\r\n')  #spx set to grams
    time.sleep(0.5)
    scale.write(b'0M\r\n')  #scout pro set to grams
    time.sleep(0.5)
    print scale.readline()
    scale.write(b'SLP\r\n')  #spx autoprint on nonzero stability
    time.sleep(0.5)
    scale.write(b'SA\r\n')  #scout pro autoprint on nonzero stability
    time.sleep(0.5)
    print scale.readline()
    scale.reset_input_buffer()

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
