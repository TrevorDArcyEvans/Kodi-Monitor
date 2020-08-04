#!/usr/bin/env python

from gpiozero import Button
from signal import pause
import subprocess

ShutdownPin = 3

def Shutdown():
  subprocess.call(['shutdown', '-h', 'now'], shell=False)

button = Button(ShutdownPin)
button.when_pressed = Shutdown

pause()
