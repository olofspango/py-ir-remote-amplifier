from flask import Flask
from flask_restful import Resource, Api, reqparse

import serial
import time

# CONSTANTS
COMMANDS = {
    "CD_POWER": "9E6106F9",
    "PURE_DIRECT":"5EA1BB44",
    "LINE1" : "5EA19867",
    "LINE2" : "5EA1837C",
    "LINE3" :   "5EA103FC",
    "COAXIAL" :   "5EA118E7",
    "OPTICAL" :   "5EA1CA34",
    "TUNER" :   "5EA16897",      #  Was: TUNER
    "PHONO" :   "5EA128D7",
    "CD" :   "5EA1A857",    #  Was: CD
    "BAND" :   "5EA1758A",
    "TUNING_DOWN": "FE8026D8",
    "TUNING_UP": "FE808678",
    "MEMORY": "5EA1F50A",
    "PRESET_DOWN": "5EA18877",
    "PRESET_UP": "5EA108F7",
    "DISK_SKIP":"9E61F20D",
    "VOLUMEUP" :   "5EA158A7",       #  Was: VOLUME_PLUS
    "VOLUMEDOWN" :   "5EA1D827",
    "BAND" :      "7E81758A",
    "STANDBY" :      "7E8154AB",
    "PLAY" :      "9E6140BF",
    "PAUSE": "9E61AA55",
    "STOP" :      "9E616A95",
    "NEXT": "9E61E01F",
    "PREV":"9E6120DF",
    "OPEN_CLOSE" :      "9E61807F",
    "MUTE": "5EA138C7",
    "FORWARD" : "9E61609F",
    "REWIND": "9E61A05F",
    "REPEAT" : "FFFFFFFF"
}
s = serial.Serial('/dev/ttyUSB0', 9600)


command = "VOLUMEUP"
print('Sending command ' + command)
try:
  s.write(bytes.fromhex("01" + COMMANDS[command]))
  time.sleep(2)
  s.write(bytes.fromhex("02" + COMMANDS[command]))
  time.sleep(2)
  s.write(bytes.fromhex("01" + COMMANDS["VOLUMEDOWN"]))
  time.sleep(2)
  s.write(bytes.fromhex("02" + COMMANDS["VOLUMEDOWN"]))

  while True:
      data = s.readline()
      if data:
          print(data)
except KeyboardInterrupt:
  s.close()
