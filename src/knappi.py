from pluginhandler import load_all_plugins
from menu import Menu
from button import Button
from spdt import SPDT
from lcd import LCD
from flowhandler import VirtualFlowHandler,PhysicalFlowHandler

def load_flow_handler():
    prevButton = Button("prevbutton", 21, 26)
    nextButton = Button("nextbutton", 17, None)
    okButton = Button("okButton", 6, 8)
    spdt = SPDT("spdt", 4, 27)
    lcd = LCD(rs=16, en=14, d4=25, d5=11, d6=23, d7=22, bl=19)
    return PhysicalFlowHandler(prevButton, nextButton, okButton, spdt, lcd)

def main():
    flow_handler = load_flow_handler()
    plugins = load_all_plugins()
    for plugin in plugins:
        plugin_menu = Menu(plugin.get_name())
        plugin.setup(plugin_menu)
        flow_handler.add_submenu(plugin_menu)
    
    flow_handler.process_flow()
    
    for plugin in plugins:
        plugin.cleanup()

    print("Bye <3")
    
if __name__ == "__main__":
    main()
