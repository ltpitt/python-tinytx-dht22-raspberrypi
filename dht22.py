# TinyTX - DHT22 - Raspberry Pi serial reader
#
# This is a tiny script to receive data sent from TinyTX and save it to MysqlDB
#
# TinyTX is an Open Source wireless IoT sensor node built and shared by great
# Nathan Chantrell (http://nathan.chantrell.net/tinytx-wireless-sensor/)
# Special thanks goes to him also for the read_data function
#
# This script should be set to be executed in cron every 15 minutes.
# To do so add in "crontab -e":
#
# 0,15,30,45 * * * * /usr/bin/python /your/script/path/dht22.py
#
# Davide Nastri, 04/2014

import serial
import string
from time import sleep
import MySQLdb
import MySQLdb as Database
from warnings import filterwarnings
filterwarnings('ignore', category = Database.Warning)
import smtplib
from email.mime.text import MIMEText

# Specify your serial port path (/dev/ttyAMA0 is default for Raspberry Pi)
serialport = serial.Serial("/dev/ttyAMA0", 9600, timeout=0)

# This function reads data from serial port and prints received values in human readable format
def read_data(rx):

    data = rx.lstrip().split(" ")

    a = int(data[1])
    b = int(data[2])
    c = int(data[3])
    d = int(data[4])
    e = int(data[5])
    f = int(data[6])

    node_id = str(int(data[0]) & 0x1f)
    humidity = str((a+b*256)/100.0)
    voltage = str(c+d*256)
    temperature = str((e+f*256)/100.0)
    print "node:", node_id
    print "humidity:", humidity, "%"
    print "temperature:", temperature, "C"
    print "voltage:", voltage, "mV"
    if int(voltage) < 3100:
        low_battery_email_notification(voltage)
    insert_data(humidity, temperature)


# This function inserts received data into mysql database - Adjust parameters for your server
def insert_data(humidity, temperature):
    mydb = MySQLdb.connect(host='', # Enter your Mysql Server ip
        user='', # Enter your mysql username
        passwd='', # Enter your mysql password
        db='dht22')
    cursor = mydb.cursor()
    cursor.execute ('INSERT INTO dht22 (temperature, humidity)' \
          'VALUES(%s, %s)', (
          temperature, humidity))
    mydb.commit()
    cursor.close()
    exit()

# This function sends notifications to email
def low_battery_email_notification(battery_level):
    message = "Battery in your TinyTX is running low.\r\nActual reading shows: "+str(battery_level)+" Millivolts"
    subject = "TinyTX notification"
    s = smtplib.SMTP('smtp.gmail.com')
    s.set_debuglevel(1)
    sender = '' # Fill with your information
    password = '' # Same as above
    recipients = [''] # Again
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    s.ehlo()
    s.starttls()
    s.ehlo
    s.login(sender, password)
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()

try_number = 0

while True:

    data = serialport.read(9999)
    if len(data) > 0:
        print "Got data: "+data
        read_data(data)
    sleep(1)
    try_number += 1
    print 'Waiting data... '+str(try_number)
    if try_number == 500:
        exit()

ser.close()
