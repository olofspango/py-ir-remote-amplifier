import serial
import time

s = serial.Serial('/dev/ttyUSB0', 9600) # change name, if needed
# s.open()
time.sleep(5) # the Arduino is reset after enabling the serial connectio, therefore we have to wait some seconds

while True:
  try:
    s.write(bytes.fromhex('5EA19867'))
    time.sleep(5)
  except KeyboardInterrupt:
    s.close()
