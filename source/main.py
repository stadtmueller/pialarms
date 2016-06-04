
# This file is part of PiAlarms.
#
#   PiAlarms is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   PiAlarms is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with PiAlarms.  If not, see <http://www.gnu.org/licenses/>.

#----------------------------------------------------------------------

#! /usr/bin/env python
# -*- coding: utf8 -*-
# FILENAME: main.py

import threading
import Timer
import Mail
import RPi.GPIO as GPIO
import picamera
import os

m = Mail.Email()
# Conifgure this line with receiever address, email login name and password
m.setLoginData( "rec", "ema", "psw" )

stop = threading.Event()
tMain = Timer.Timer( 145, 145, stop )
t = Timer.Timer( 30, 30, stop )

sensorPin = 7
spotlightPin = 38
loopCount = 0
pictureCount = 0

fileName = "/home/pi/PiCamera/Fotos/SILENT%i.jpg"
smsFile = "/home/pi/message.txt"

cam = picamera.PiCamera()
# cam.led = False # Only with GPIO.setmode( GPIO.BCM ) possible
GPIO.setwarnings( False )
GPIO.setmode( GPIO.BOARD )
GPIO.setup( sensorPin, GPIO.IN )
GPIO.setup( spotlightPin, GPIO.OUT )

# Namefind-algorythm
def name( files, nameTemp ):
  i = 0
  files.sort()
  if not len( files ) == 0:
    while i < len( files ):
      if not file == ( nameTemp % i ):
        s = ( nameTemp % ( i + 1 ) )
      if file == ( nameTemp % i ):
        print "No Match"
      i += 1
  else:
    s = ( nameTemp % 0 )
  return s

# Sensor-buffer
def waitForSensor():
  while GPIO.input( 7 ) == GPIO.HIGH:
    pass

# Function to call after timer was trminated
def cleanAndExit():
  GPIO.cleanup()
  cam.close()
  stop.set()
  os.system( "sudo shutdown -h now" )

# Moving message.txt to /var/spool for sms-script
def sendSMS():
  os.system( "cp /home/pi/message.txt /var/spool/sms/outgoing" )
  print( "Copied File" )

def sendMail( m, filename ):
  m.setFilename( filename )
  m.send()

#--------------------------------
#--------------------------------


try:
  tMain.start()
  t.start()

  waitForSensor()

  while True:
    if GPIO.input( sensorPin ):
      files = os.listdir( "/home/pi/PiCamera/Fotos" )
      t.reset()
      print( "-- TRIGGERED: Taking picture..." )
      GPIO.output( spotlightPin, GPIO.HIGH )
      storeTo = name( files, fileName )
      cam.capture( name( files, fileName ) )
      GPIO.output( spotlightPin, GPIO.LOW )
      print( "-- TRIGGERED: Sending SMS..." )
      sendMail()
      pictureCount += 1 
      waitForSensor()
    else:
      print "Sensor inactiv -- " + str( loopCount )
      loopCount += 1
    time.sleep( 0.50 )
except KeyboardInterrupt:
  GPIO.cleanup()
  cam.close()
  stop.set()
  exit()
