
from menu import MenuTraverser
from tts import say
from spdt import SPDT
from lcd import LCDBottom

class VirtualFlowHandler:

    def __init__(self):
        # Menu handler
        self.menu_handler = MenuTraverser(self.update_display)

    def process_flow(self):
        self.menu_handler.prepare_menu()

        print("Use prev, next, back or enter commands to move around")
        while True:
            cmd = input()
            if cmd == "prev":
                self.menu_handler.prev()
            elif cmd == "next":
                self.menu_handler.next()
            elif cmd == "back":
                self.menu_handler.back()
            elif cmd == "enter":
                self.menu_handler.enter()
            elif cmd == "exit":
                break

    def update_display(self):
        print("Menu is now :")
        print(self.menu_handler.active_menu.stringify(1))

    def add_submenu(self, submenu):
        self.menu_handler.menu.add_submenu(submenu)

class PhysicalFlowHandler:

    def __init__(self, buttonPrev, buttonNext, buttonAction, spdt, display):
        # Keep all HW components
        self.buttonPrev = buttonPrev
        self.buttonNext = buttonNext
        self.buttonAction = buttonAction
        self.spdt = spdt
        self.display = display
        self.user_display = LCDBottom(self.display)
        # Menu handler
        self.menu_handler = MenuTraverser(self.update_display)
        self.menu_handler.state["display"] = self.user_display
        # Init
        self.setup_events()

    def setup_events(self):
        import RPi.GPIO as GPIO
        def handle_action_button_release(button, time):
            if time < 1:
                self.display.enable_backlight(True)
                self.menu_handler.enter()
        def handle_prev_hold(button, time):
            if time > 3 and time < 4:
                self.menu_handler.goto_root()
                self.display.enable_backlight(False)
        def handle_spdt_change(spdt, state):
            if state == SPDT.SPDT_ON_TOP:
                say("Sound and voice on")
            elif state == SPDT.SPDT_OFF:
                say("Sound on, voice off")
            elif state == SPDT.SPDT_ON_BOTTOM:
                say("Sound and voice off")

        GPIO.setmode(GPIO.BCM)
        self.buttonPrev.onPress(lambda _: self.menu_handler.prev())
        self.buttonPrev.onHold(handle_prev_hold)
        self.buttonNext.onPress(lambda _: self.menu_handler.next())
        self.buttonNext.onHold(handle_prev_hold)
        self.buttonAction.onRelease(handle_action_button_release)
        self.buttonAction.onHold(lambda _, __: self.menu_handler.back())
        self.spdt.onChanged(handle_spdt_change)

    def process_flow(self):
        self.menu_handler.prepare_menu()

        while True:
            cmd = input()
            if cmd == "prev":
                self.menu_handler.prev()
            elif cmd == "next":
                self.menu_handler.next()
            elif cmd == "back":
                self.menu_handler.back()
            elif cmd == "enter":
                self.menu_handler.enter()
            elif cmd == "exit":
                break
        self.teardown()

    def update_display(self):
        self.display.set_text(self.menu_handler.active_menu.title, center=True)

    def add_submenu(self, submenu):
        self.menu_handler.menu.add_submenu(submenu)

    def teardown(self):
        import RPi.GPIO as GPIO
        self.buttonPrev.terminate()
        self.buttonNext.terminate()
        self.buttonAction.terminate()
        self.display.terminate()
        GPIO.cleanup()

