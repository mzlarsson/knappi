#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi
from lcd import LCD
import time

lcd = LCD(16, 19, 25, 11, 23, 22)

lcd.set_text('Hello!')

time.sleep(2)

lcd.set_text("World!", clean=False)

time.sleep(2)

lcd.set_text("Center!", center=True)

time.sleep(2)

lcd.cursor_visible(True)
lcd.cursor_blink(True)

time.sleep(2)

lcd.clear()
lcd.cursor_position(1, 9)
lcd.set_text("Hupp", clean=False, center=False)
lcd.autoscroll(True)

time.sleep(2)
lcd.set_text("NANO", clean=False)

time.sleep(2)

lcd.clear()
lcd.autoscroll(False)

time.sleep(4)

lcd.roll("Hello World!")