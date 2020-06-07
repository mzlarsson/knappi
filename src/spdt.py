import threading
import RPi.GPIO as GPIO

class SPDT(object):

    SPDT_ON_BOTTOM = 0
    SPDT_OFF = 1
    SPDT_ON_TOP = 2

    def __init__(self, id, pin_top, pin_bot, bounce_time=0.3):
        self.id = id
        self.state = None
        self.pin_top = pin_top
        self.pin_bot = pin_bot
        self.onChangeHandlers = []
        self.bounce_time = bounce_time
        self.bounceTimer = None
        self.buffered_events = []
        self.initGPIO()

    def initGPIO(self):
        self._init_pin(self.pin_top)
        self._init_pin(self.pin_bot)
        
        if GPIO.input(self.pin_top):
            self.state = self.SPDT_ON_TOP
        elif GPIO.input(self.pin_bot):
            self.state = self.SPDT_ON_BOTTOM
        else:
            self.state = self.SPDT_OFF

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
        if channel == self.pin_top:
            self.state = SPDT.SPDT_ON_TOP if GPIO.input(self.pin_top) else SPDT.SPDT_OFF
        elif channel == self.pin_bot:
            self.state = SPDT.SPDT_ON_BOTTOM if GPIO.input(self.pin_bot) else SPDT.SPDT_OFF

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
        GPIO.remove_event_detect(self.pin_top)
        GPIO.remove_event_detect(self.pin_bot)
        del self.onPressHandlers[:]
        del self.onReleaseHandlers[:]
