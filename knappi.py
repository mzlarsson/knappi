from pluginhandler import load_all_plugins
from menu import Menu
from flowhandler import VirtualFlowHandler

def load_flow_handler():
    return VirtualFlowHandler()

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