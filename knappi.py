from pluginhandler import load_all_plugins
from menu import Menu
from button import Button
from lcd import LCD
from flowhandler import VirtualFlowHandler,PhysicalFlowHandler

def load_flow_handler():
    prevButton = Button("prevbutton", 21, 26)
    nextButton = Button("nextbutton", 14, 17)
    okButton = Button("okButton", 6, 8)
    lcd = LCD(rs=16, en=19, d4=25, d5=11, d6=23, d7=22)
    return PhysicalFlowHandler(prevButton, nextButton, okButton, lcd)

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