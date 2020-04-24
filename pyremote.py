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
app = Flask(__name__)
api = Api(app)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

repeating = False

@app.route('/repeatOn')
def startRepeat():
    global repeating
    print("Started repeating")
    repeating = True
    repeater()
    return "Started Repeating"

@app.route('/repeatOff')
def stopRepeat():
    global repeating
    repeating = False
    return "Stopped Repeating"

def repeater():
    global repeating
    while(repeating):
        s.write(bytes.fromhex("01ffffffff"))
        time.sleep(0.200)
        print("FFFFFFFF")

class RemoteControl(Resource):
    def get(self, command):
        try:
            # repeatCount = 1
            # if(command.startswith("VOLUME")):
            #     repeatCount = 1 # Had this set to 3 before, but fixed so that if you hold the button IR sends repeat command
            # for i in range(0, repeatCount):
            print('Sending command ' + command)
            s.write(bytes.fromhex("00" + COMMANDS[command]))
            # time.sleep(0.040)

        except KeyboardInterrupt:
           s.close()
        except:
            return "Failed. Something went wrong."
        return "OK"
#api.add_resource(RemoteControl,'/remote/')
api.add_resource(RemoteControl,'/remote/<command>')


if __name__ == "__main__":
  app.run(port="5002", host="0.0.0.0")
