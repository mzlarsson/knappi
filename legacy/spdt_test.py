
from spdt import SPDT
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

spdt = SPDT("my_spdt", 26, 19)
spdt.onChanged(lambda x, state: print("State: %d" % state))


while(True):
    cmd = input()
    if cmd == "exit":
        break
        
print("Bye!")