import threading
import RPi.GPIO as GPIO

class SPDT(object):
    
    SPDT_OFF = 0
    SPDT_ON_LEFT = 1
    SPDT_ON_RIGHT = 2
    
    def __init__(self, id, pin_left, pin_right, bounce_time=0.3):
        self.id = id
        self.state = SPDT.SPDT_OFF
        self.pin_left = pin_left
        self.pin_right = pin_right        
        self.onChangeHandlers = []
        self.bounce_time = bounce_time
        self.bounceTimer = None
        self.buffered_events = []
        self.initGPIO()

    def initGPIO(self):
        self._init_pin(self.pin_left)
        self._init_pin(self.pin_right)
    
    def _init_pin(self, pin):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pin, GPIO.BOTH)
        GPIO.add_event_callback(pin, self.stateChanged)
        
    def getValue(self):
        return self.state
        
    def onChanged(self, handler):
        if handler is not None:
            self.onChangeHandlers.append(handler)
        
    def removeChangeHandler(self, handler):
        self.onChangeHandlers.remove(handler)
        
    def stateChanged(self, channel):
        old_state = self.state
        if channel == self.pin_left:
            self.state = SPDT.SPDT_ON_LEFT if GPIO.input(self.pin_left) else SPDT.SPDT_OFF
        elif channel == self.pin_right:
            self.state = SPDT.SPDT_ON_RIGHT if GPIO.input(self.pin_right) else SPDT.SPDT_OFF
            
        if self.state != old_state:
            self.buffered_events.append(self.state)
            if not self.bounceTimer:
                self.bounceTimer = threading.Timer(self.bounce_time, self.bounceTimerEnded)
                self.bounceTimer.start()
            
            
    def bounceTimerEnded(self):
        if all(map(lambda x: x == self.state, self.buffered_events)):
            self.bounceTimer = None
            self.buffered_events = []
            for handler in self.onChangeHandlers:
                handler(self, self.state)
        else:
            self.buffered_events = [self.state]
            self.bounceTimer = threading.Timer(self.bounce_time, self.bounceTimerEnded)
            self.bounceTimer.start()
        
    def terminate(self):
        GPIO.remove_event_detect(self.pin_left)
        GPIO.remove_event_detect(self.pin_right)
        del self.onPressHandlers[:]
        del self.onReleaseHandlers[:]