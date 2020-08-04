#!/usr/bin/env python

import os
from time import sleep
import RPi.GPIO as GPIO

# Kodi
KodiUserName = os.environ['KODI_USER_NAME']
KodiPassword = os.environ['KODI_PASSWORD']
KodiHost = os.environ['KODI_HOST']
KodiPort = os.environ['KODI_PORT']

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

# disable warnings
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(KodiUp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(KodiBack, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(KodiLeft, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(KodiEnter, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(KodiRight, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(KodiDown, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# diagnostics
print('Settings:')
print(f'  KODI_USER_NAME = {KodiUserName}')
print(f'  KODI_PASSWORD  = {KodiPassword}')
print(f'  KODI_HOST      = {KodiHost}')
print(f'  KODI_PORT      = {KodiPort}')

while True:
    if (GPIO.input(KodiUp) == True):
        print('KodiUp')

    if (GPIO.input(KodiBack) == True):
        print('KodiBack')

    if (GPIO.input(KodiLeft) == True):
        print('KodiLeft')

    if (GPIO.input(KodiEnter) == True):
        print('KodiEnter')

    if (GPIO.input(KodiRight) == True):
        print('KodiRight')

    if (GPIO.input(KodiDown) == True):
        print('KodiDown')

    sleep(0.15);

