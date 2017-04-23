# ohaus_scale_data
captures data from ohaus scale

you will need to install pyserial for this to work.

Should work with both the scout pro, and scout spx

The script initializes the scale to auto print grams when not zero

to run it, run scale.py port, where port is something like /dev/ttyUSB0 or wherever the scale shows up on your system

it will save to a file called weight_datayearmonthdayhourminutesecond.csv

