#!/usr/bin/env python

import os
import sys
import json
import urllib.request
import base64
import time
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
KodiSelect = 21

KodiRight = 17
KodiDown = 15

# Makes a POST call to Kodi RPC API and returns the response
#
# GET calls used to work:
#
#   https://forum.kodi.tv/showthread.php?tid=324598
#
# A major change for Leia onwards is that JSON-RPC no longer accepts many of the commands via HTTP.
# This is a measure taken for improved security, but no doubt will inconvenience a number of JSON consumers.
# Although Kodi still accepts HTTP GET requests to JSON it limits all non-POST requests to ReadData permissions only.
# So when trying to call a modifying JSON-RPC method like Player.PlayPause the following error will be returned:
# {
# "jsonrpc": "2.0",
# "error": {
#   "code": -32099,
#   "message": "Bad client permission."
#   },
# "id": 1
# }
# To make any data modifications you will need to use HTTP POST.
# See https://github.com/xbmc/xbmc/pull/12281 for more details.
def SendPostToKodi(host, port, username, password, method):
  # build the URL for Kodi
  url = 'http://%s:%s/jsonrpc' %(host, port)
    
  # build json data structure to be sent
  values = {}
  values["jsonrpc"] = "2.0"
  values["method"] = method
  values["id"] = "1"

  headers = {"Content-Type":"application/json",}

  # format data
  data = json.dumps(values)
  data = str(data)
  data = data.encode("utf-8")

  # 'data' field will make the method "POST"
  req = urllib.request.Request(url, headers=headers, data=data)

  # add base64 encoded Basic Auth header
  base64string = base64.encodestring(('%s:%s' % (username,password)).encode()).decode().strip()
  req.add_header("Authorization", "Basic %s" % base64string)

  # wrap RPC call to Kodi in a try: block to allow for graceful error handling
  try:
    response = urllib.request.urlopen(req)
    response = response.read()
    response = json.loads(response.decode('utf-8'))

    # A lot of the Kodi responses include the value "result", which lets you know how your call went
    # This logic fork grabs the value of "result" if one is present, and then returns that.
    # Note, if no "result" is included in the response from Kodi, the JSON response is returned instead.
    # You can then print out the whole thing, or pull info you want for further processing or additional calls.
    if 'result' in response:
      response = response['result']

    # explicitly catch HTTP errors and connection errors
  except urllib.error.HTTPError as e:
    response = 'ERROR: ' + str(e.reason)

  return response

def Input(key):
  return SendPostToKodi(KodiHost, KodiPort, KodiUserName, KodiPassword, key)

# callbacks
def OnKodiUp(channel):
  print("OnKodiUp")

def OnKodiBack(channel):
  print("OnKodiBack")

def OnKodiLeft(channel):
  print("OnKodiLeft")

def OnKodiSelect(channel):
  print("OnKodiSelect")

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
GPIO.setup(KodiSelect, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(KodiRight, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(KodiDown, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(KodiUp, GPIO.RISING, callback=OnKodiUp, bouncetime=BounceTime)
GPIO.add_event_detect(KodiBack, GPIO.RISING, callback=OnKodiBack, bouncetime=BounceTime)
GPIO.add_event_detect(KodiLeft, GPIO.RISING, callback=OnKodiLeft, bouncetime=BounceTime)
GPIO.add_event_detect(KodiSelect, GPIO.RISING, callback=OnKodiSelect, bouncetime=BounceTime)
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
