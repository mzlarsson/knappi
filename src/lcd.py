# Character LCD
# (only supports 16x2, since that is the only size I'm interested in xD)
import Adafruit_CharLCD as AF_LCD
from threading import Timer

"""
Default pin setup
=================
lcd_rs = 16
lcd_en = 14
lcd_d4 = 25
lcd_d5 = 11
lcd_d6 = 23
lcd_d7 = 22
lcd_backlight = 19
"""

class LCD(object):

    DIRECTION_RIGHT = 0
    DIRECTION_LEFT = 1

    def __init__(self, rs=16, en=14, d4=25, d5=11, d6=23, d7=22, bl=19):
        self.lcd = AF_LCD.Adafruit_CharLCD(rs, en, d4, d5, d6, d7, 16, 2, bl, enable_pwm=True, invert_polarity=False)
        self.rolling_text = None
        self.current_text = None
        
    def width(self):
        return 16
        
    def height(self):
        return 2
        
    def enable(self, enable):
        self.lcd.enable_display(enable)
        
    def enable_backlight(self, enable):
        self.lcd.set_backlight(1 if enable else 0)
        
    def set_text(self, text, clean=True, center=False):
        self.rolling_text = None
        if clean:
            self.clear()
        if center:
            def center_line(line):
                if len(line) < 16:
                    line = " "*int((self.width()-len(line))/2) + line
                return line
            text = "\n".join(list(map(center_line, text.split("\n"))))
            
        self.current_text = text

        print("Printing '%s'" % text)
        self.lcd.message(text)
        
    def roll(self, text, delay=0.5):
        if len(text) < 16:
            text = " "*(16-len(text)) + text
        self.rolling_text = text
        self._roll_next(delay, False)
            
    def _roll_next(self, delay, rotate=True):
        if self.rolling_text:
            if rotate:
                self.rolling_text = self.rolling_text[1:] + self.rolling_text[0]
            self.lcd.clear()
            self.lcd.message(self.rolling_text)
            Timer(delay, self._roll_next, args=(delay,True)).start()
        
    def cursor_home(self):
        self.lcd.home()
        
    def cursor_position(self, col, row):
        self.lcd.set_cursor(col, row)
        
    def cursor_visible(self, visible):
        self.lcd.show_cursor(visible)
        
    def cursor_blink(self, blink):
        self.lcd.blink(blink)
        
    def cursor_move(self, right=True):
        if self.DIRECTION_LEFT:
            self.lcd.move_left()
        else:
            self.lcd.move_right()
            
    def autoscroll(self, autoscroll):
        self.lcd.autoscroll(autoscroll)
        
    def clear(self):
        self.lcd.clear()
        
    def terminate(self):
        self.rolling_text = None
        self.clear()

class LCDBottom:

    def __init__(self, lcd):
        self.lcd = lcd
        self.current_text = None
        
    def set_text(self, text, center=False):
        upper_text = self.lcd.current_text.split("\n")[0]
        lower_text = text
        if len(text) < 16 and center:
            lower_text = " "*int((self.lcd.width()-len(text))/2) + text
            
        self.current_text = lower_text
            
        self.lcd.set_text(upper_text + "\n" + lower_text)
