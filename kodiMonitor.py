#!/usr/bin/env python

import os
import RPi.GPIO as GPIO

# Kodi
KodiUserName = os.environ['KODI_USER_NAME']
KodiPassword = os.environ['KODI_PASSWORD']
KodiHost = os.environ['KODI_HOST']
KodiPort = os.environ['KODI_PORT']

# button config
BounceTime = 200 # ms

# input buttons
KodiUp = 14
KodiBack = 18
KodiLeft = 4

# The only thing that is special about GPIO27 on Pin 13 is that it was GPIO21 on Rev 1 boards
#   https://www.raspberrypi.org/forums/viewtopic.php?t=36486
#
# $ cat /sys/firmware/devicetree/base/model 
# Raspberry Pi Model B Rev 1
KodiEnter = 21

KodiRight = 17
KodiDown = 15

# callbacks
def OnKodiUp(channel):
  print("OnKodiUp")

def OnKodiBack(channel):
  print("OnKodiBack")

def OnKodiLeft(channel):
  print("OnKodiLeft")

def OnKodiEnter(channel):
  print("OnKodiEnter")

def OnKodiRight(channel):
  print("OnKodiRight")

def OnKodiDown(channel):
  print("OnKodiDown")

# disable warnings
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(KodiUp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(KodiBack, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(KodiLeft, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(KodiEnter, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(KodiRight, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(KodiDown, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(KodiUp, GPIO.RISING, callback=OnKodiUp, bouncetime=BounceTime)
GPIO.add_event_detect(KodiBack, GPIO.RISING, callback=OnKodiBack, bouncetime=BounceTime)
GPIO.add_event_detect(KodiLeft, GPIO.RISING, callback=OnKodiLeft, bouncetime=BounceTime)
GPIO.add_event_detect(KodiEnter, GPIO.RISING, callback=OnKodiEnter, bouncetime=BounceTime)
GPIO.add_event_detect(KodiRight, GPIO.RISING, callback=OnKodiRight, bouncetime=BounceTime)
GPIO.add_event_detect(KodiDown, GPIO.RISING, callback=OnKodiDown, bouncetime=BounceTime)

# diagnostics
print('Settings:')
print(f'  KODI_USER_NAME = {KodiUserName}')
print(f'  KODI_PASSWORD  = {KodiPassword}')
print(f'  KODI_HOST      = {KodiHost}')
print(f'  KODI_PORT      = {KodiPort}')

try:
  while True:
    pass

finally:
  GPIO.cleanup()
