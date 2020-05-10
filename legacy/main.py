
import RPi.GPIO as GPIO

from property import Property
from button import Button
from led import LED, MultiLED
from mumblehandler import MumbleHandler

from time import sleep

def main():

    print("Starting mumble client...")
    mumble_client = MumbleHandler("Knappi")
    mumble_client.join_channel("BoyfriendStatus")
    print("Client started!")
    
    sleep(1)  # Make sure everything went OK

    GPIO.setmode(GPIO.BCM)
    
    state = Property(0)
    sound_enabled = Property(0)
    
    def handleMultiPress(button, presses):
        print("multipress %d" % presses)
        if presses == 1:
            # Show info
            state.setValue(1)
            sleep(2)
            state.setValue(0)
        elif presses == 2:
            # Send request about stopping
            state.setValue(2)
        elif presses == 3:
            # Send URGENT request about stopping
            state.setValue(1)
            
    def handleHold(button, duration):
        if duration >= 3 and duration < 4:
            if sound_enabled.getValue():
                mumble_client.disable_sound()
                sound_enabled.setValue(0)
                state.setValue(0)
            else:
                mumble_client.enable_sound()
                sound_enabled.setValue(1)

    button = Button("mybutton", 17, None, 1)
    button.onMultiPress(handleMultiPress)
    button.onHold(handleHold)

    led1 = LED("led1", 27)
    led2 = LED("led2", 22)
    multi_led = MultiLED([led1, led2])
    
    def updateLEDState(value):
        if sound_enabled.getValue():
            multi_led.set_state(3)
        else:
            multi_led.set_state(state.getValue())
            
    state.listen(updateLEDState)
    sound_enabled.listen(updateLEDState)
    
    print("Button initiated and event handlers registered")
    print("Waiting for button press...")
    
    cmd = ""
    while cmd != "exit":
        cmd = input()
        if cmd == "state":
            mumble_client.print_state()
        
    mumble_client.disable_sound()
    button.terminate()
    GPIO.cleanup()

if __name__ == "__main__":
    main()