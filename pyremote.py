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
    "REPEAT" : "FFFFFFFF",
    "SONY_POWER" : "00000A90",
    "SONY_VOLUMEUP" : "00000490",
    "SONY_VOLUMEDOWN" : "00000C90",
    "SONY_ACTIONMENU" :"00006923",
    "SONY_OK" : "00000A70",
    "SONY_INPUT" : "00000A50",
    "SONY_KEY_1" : "00000010",
    "SONY_KEY_2" : "00000810",
    "SONY_KEY_3" : "00000410",
    "SONY_KEY_4" : "00000c10",
    "SONY_KEY_5" : "00000210",
    "SONY_KEY_6" : "00000a10",
    "SONY_KEY_7" : "00000610",
    "SONY_KEY_8" : "00000e10",
    "SONY_KEY_9" : "00000110",
    "SONY_KEY_0" : "00000910",
    "SONY_BACK" : "000062E9",
    "SONY_HOME" : "00000070",
    "SONY_VOLUME_UP" : "00000490",
    "SONY_VOLUME_DOWN" : "00000C90",
    "SONY_PROGRAM_UP" : "00000090",
    "SONY_PROGRAM_DOWN" : "00000890",
    "SONY_MUTE" : "00000290",
    "SONY_PLAY" : "00002CE9",
    "SONY_PAUSE" : "00004CE9",
    "SONY_NEXT" : "00005EE9",
    "SONY_PREVIOUS" : "00001EE9",
    "SONY_STOP" : "00000CE9"
}

SONY_NUMBER_OF_BITS = {
    "SONY_POWER": 12,
    "SONY_VOLUMEDOWN": 12,
    "SONY_VOLUMEUP" : 12,
    "SONY_ACTIONMENU" : 15,
    "SONY_OK": 12,
    "SONY_INPUT" : 12,
    "SONY_KEY_1" : 12,
    "SONY_KEY_2" : 12,
    "SONY_KEY_3" : 12,
    "SONY_KEY_4" : 12,
    "SONY_KEY_5" : 12,
    "SONY_KEY_6" : 12,
    "SONY_KEY_7" : 12,
    "SONY_KEY_8" : 12,
    "SONY_KEY_9" : 12,
    "SONY_KEY_0" : 12,
    "SONY_BACK" : 15,
    "SONY_HOME" : 12,
    "SONY_VOLUME_UP" : 12,
    "SONY_VOLUME_DOWN" : 12,
    "SONY_PROGRAM_UP" : 12,
    "SONY_PROGRAM_DOWN" : 12,
    "SONY_MUTE" : 12,
    "SONY_PLAY" : 15,
    "SONY_PAUSE" : 15,
    "SONY_NEXT" : 15,
    "SONY_PREVIOUS" : 15,
    "SONY_STOP" : 15,

}

s = serial.Serial('/dev/ttyUSB0', 9600)
app = Flask(__name__)
api = Api(app)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

class RemoteControl(Resource):
    def get(self, command, repeat):
        if(repeat == "start"):
            print("starting!")
            s.write(bytes.fromhex("01" + COMMANDS[command]))
        try:
            if(repeat == "start"):
               commandCode = "01"
            elif (repeat == "stop"):
               commandCode = "02"
            elif (command.startswith("SONY")):
                commandType = 3
                numberOfBits = SONY_NUMBER_OF_BITS[command]
                commandCode = (( hex((numberOfBits << 3) + commandType) ) + "" ).replace("0x", "")
            else:
               commandCode = "00"
            print('Sending command ' + command + " with repeatcode " +  commandCode)
            s.write(bytes.fromhex(commandCode + COMMANDS[command]))
            # time.sleep(0.040)

        except KeyboardInterrupt:
           s.close()
        except Exception as e:
            print(e)
            return "Failed. Something went wrong."
        return "OK"
api.add_resource(RemoteControl,'/remote/<command>/<repeat>')


if __name__ == "__main__":
  app.run(port="5002", host="0.0.0.0")
