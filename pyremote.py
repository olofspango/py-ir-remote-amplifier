from flask import Flask
from flask_restful import Resource, Api, reqparse

import serial
# import time

# CONSTANTS
COMMANDS = {
    "LINE1" : "5EA19867",
    "LINE2" : "5EA1837C",
    "LINE3" :   "5EA103FC",
    "COAXIAL" :   "5EA118E7",
    "OPTICAL" :   "5EA1CA34",
    "KEY_TUNER" :   "5EA16897",      #  Was: TUNER
    "PHONO" :   "5EA128D7",
    "KEY_CD" :   "5EA1A857",    #  Was: CD
    "BAND" :   "5EA1758A",
    "KEY_VOLUMEUP" :   "5EA158A7",       #  Was: VOLUME_PLUS
    "KEY_VOLUMEDOWN" :   "5EA1D827",
    "BAND" :      "7E81758A",
    "STANDBY" :      "7E8154AB",
    "PLAY" :      "9E6140BF",
    "STOP" :      "9E616A95",
    "OPEN_CLOSE" :      "9E61807F"
}
# LINE1 = "5EA19867"
# LINE2 = "5EA1837C"
# LINE3 =   "5EA103FC"
# COAXIAL =   "5EA118E7"
# OPTICAL =   "5EA1CA34"
# KEY_TUNER =   "5EA16897"        #  Was: TUNER
# PHONO =   "5EA128D7"
# KEY_CD =   "5EA1A857"        #  Was: CD
# BAND =   "5EA1758A"
# KEY_VOLUMEUP =   "5EA158A7"        #  Was: VOLUME_PLUS
# KEY_VOLUMEDOWN =   "5EA1D827"
# BAND               =      "7E81758A"
# STANDBY            =      "7E8154AB"        #  Was: STANDBY
# PLAY               =      "9E6140BF"
# STOP               =      "9E616A95"
# OPEN_CLOSE         =      "9E61807F"

s = serial.Serial('/dev/ttyUSB0', 9600)

# time.sleep(5) # the Arduino is reset after enabling the serial connection, therefore we need some wait a second

app = Flask(__name__)
api = Api(app)

class RemoteControl(Resource):
    def get(self, command):
       if command:
           print('You send a command as well!')
       print("Gonna try to send the optical ir code")
       try:
           s.write(bytes.fromhex(COMMANDS[command]))
       except KeyboardInterrupt:
           s.close()
       return "OK"
#api.add_resource(RemoteControl,'/remote/')
api.add_resource(RemoteControl,'/remote/<command>')


if __name__ == "__main__":
  app.run(port="5002", host="0.0.0.0")
