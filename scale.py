#!/usr/bin/python2
#
# you must install pyserial (sudo easy_install pyserial)
#
# Scout pro manual with commands here: http://dmx.ohaus.com/WorkArea/downloadasset.aspx?id=3600
# Scout SPX manusl http://dmx.ohaus.com/WorkArea/showcontent.aspx?id=4294974227

import serial
import time
import sys
import optparse
import os
import random

def important(counter, period):
    randomphrase = ["I'm tired, are you?", "that looks delicious", "wait, who are you again?",
        "my name is scale, what's yours?", "this is so fun", "want to come over my place when we're done?",
        "kwantos boatayas tienes me ameego"]
    #if say does not work, try espeak
    if counter % period == 0:
            command = 'say ' + '\"' + random.choice(randomphrase) + '\"'
            os.system(command)

parser = optparse.OptionParser()
parser.add_option('-m', '--min-weight', help='below this weight, bell will sound')
parser.add_option('-o', '--output-file', help='file to write output')
parser.add_option('-p', '--serial-port', help='serial port to use')
(options, args) = parser.parse_args()

if options.output_file is None:
    save_file = time.strftime("weigh_data%Y%m%d%H%M%S.csv", time.localtime())
else:
    save_file = options.output_file
print"saving to file: " + save_file

if options.serial_port is None:
     parser.print_help()
     exit(-1)
else:
    port = options.serial_port

if options.min_weight:
    minweight = float(options.min_weight)
    if minweight > 1000 or minweight < 500:
        print 'warning: min-weight is out of range: ' + str(minweight)
else:
    minweight = 0;

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
                    g = float(grams.split()[0])
                    scale_out = str(str(counter) + ',' + str(scale_time) + ',' + str(g) + '\n')
                    f.write(scale_out)
                    if g < minweight:
                        print "\a\033[31m" + str(counter) + ': *LOW*' + str(g) + 'g' + "\033[0m"
                        phrase = "Low Weight Of " + str(g) + " Grams"
                        command = 'say ' + '\"' + phrase + '\"'
                        os.system(command)
                    else:
                        print str(counter) + ': ' + str(g) + 'g'
                    important(counter, 100)

            else: time.sleep(0.1)
        f.close()
    scale.close()

