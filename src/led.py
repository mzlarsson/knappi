import RPi.GPIO as GPIO
import threading

class LED(object):
    
    def __init__(self, id, pin):
        self.id = id
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def is_active(self):
        return GPIO.input(self.pin) == 1
        
    def set_state(self, on):
        if on:
            GPIO.output(self.pin, 1)
        else:
            GPIO.output(self.pin, 0)
            
            
class MultiLED(object):
    
    STATE_NO_LIGHT = 0
    STATE_BLINK = 1
    STATE_ROUND_ROBIN = 2
    STATE_FULL_LIGHT = 3
    
    def __init__(self, leds):
        self.leds = leds
        self.speed = 2
        self.state = None
        self.rr_led = 0
        self.timer = None
        self.set_state(self.STATE_NO_LIGHT) # Reset LEDs
        
    def get_state(self):
        return self.state
        
    def set_state(self, new_state):
        if self.state == new_state:
            return

        if self.timer:
            self.timer.cancel()
            self.rr_led = 0
        
        print("New MultiLED state : %d" % new_state)
        self.state = new_state
        if new_state == self.STATE_FULL_LIGHT:
            for led in self.leds:
                led.set_state(1)
        else:
            # Reset all lights
            for led in self.leds:
                led.set_state(0)
            # Start periodical updates
            if self.state != self.STATE_NO_LIGHT:
                self.update()
            
    def update(self):
        self.timer = threading.Timer(1/self.speed, self.update)
        self.timer.start()
        
        if self.state == self.STATE_BLINK:
            toggled_state = not self.leds[0].is_active()
            for led in self.leds:
                led.set_state(toggled_state)
        elif self.state == self.STATE_ROUND_ROBIN:
            self.leds[self.rr_led].set_state(0)
            self.rr_led = (self.rr_led+1)%len(self.leds)
            self.leds[self.rr_led].set_state(1)
        