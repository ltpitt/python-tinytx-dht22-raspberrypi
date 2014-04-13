tinytx-dht22-raspberrypi
========================

TinyTX - DHT22 - Raspberry Pi serial reader

This is a tiny script to receive data sent from TinyTX and save it to MysqlDB

TinyTX is an Open Source wireless IoT sensor node built and shared
by great

Nathan Chantrell (http://nathan.chantrell.net/tinytx-wireless-sensor/)

Special thanks goes to him also for the read_data function

This script should be set to be executed in cron every 15 minutes.
To do so add in "crontab -e":

0,15,30,45 * * * * /usr/bin/python /your/script/path/dht22.py

Davide Nastri, 04/2014
