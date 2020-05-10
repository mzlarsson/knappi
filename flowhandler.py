
from menu import MenuTraverser

class VirtualFlowHandler:

    def __init__(self):
        # Menu handler
        self.menu_handler = MenuTraverser(self.update_display)
        
    def process_flow(self):
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

    def __init__(self, buttonPrev, buttonNext, buttonAction, display):
        # Keep all HW components
        self.buttonPrev = buttonPrev
        self.buttonNext = buttonNext
        self.buttonAction = buttonAction
        self.display = display
        # Menu handler
        self.menu_handler = MenuTraverse(self.update_display)
        # Init
        setup_events()
        
    def setup_events(self):
        import RPi.GPIO as GPIO
        def handle_action_button(button, time):
            if time < 1:
                self.menu_handler.enter()
            else:
                self.menu_handler.back()
    
        GPIO.setmode(GPIO.BCM)
        self.buttonPrev.onPress(lambda _: self.menu_handler.prev())
        self.buttonNext.onPress(lambda _: self.menu_handler.next())
        self.buttonAction.onRelease(handle_action_button)
        
    def process_flow(self):
        while True:
            cmd = input()
            if cmd == "exit":
                break
        teardown()
        
    def update_display(self):
        print("Menu is now " + self.menu_handler.active_menu.title)
        
    def add_submenu(self, submenu):
        self.menu_handler.menu.add_submenu(submenu)
        
    def teardown(self):
        import RPi.GPIO as GPIO
        self.buttonPrev.terminate()
        self.buttonNext.terminate()
        self.buttonAction.terminate()
        self.display.terminate()
        GPIO.cleanup()
        