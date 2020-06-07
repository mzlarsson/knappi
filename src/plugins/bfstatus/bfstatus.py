
from menu import Menu
from plugins.bfstatus.mumblehandler import MumbleHandler
from time import sleep

def get_plugin():
    return BoyfriendStatus()

class BoyfriendStatus:

    def __init__(self):
        self.mumble_client = None
        
    def get_name(self):
        return "BFStatus"
        
    def get_prio(self):
        return 1000
        
    def setup(self, parent_menu):
        print("Starting mumble client...")
        self.mumble_client = MumbleHandler("Knappi")
        self.mumble_client.join_channel("BoyfriendStatus")
        print("Client started!")
        
        sleep(1)  # Make sure everything went OK
        
        mi_mute = Menu("Mute voice")
        mi_mute.register_action(self.mute_voice)
        parent_menu.add_submenu(mi_mute)
        
        mi_unmute = Menu("Unmute voice")
        mi_unmute.register_action(self.unmute_voice)
        parent_menu.add_submenu(mi_unmute)
        
        mi_cg = Menu("Current game")
        mi_cg.register_action(self.dummy_print)
        parent_menu.add_submenu(mi_cg)
        
    def mute_voice(self, state):
        self.mumble_client.disable_sound()
        state["bfstatus_voice"] = False
        
    def unmute_voice(self, state):
        self.mumble_client.enable_sound()
        state["bfstatus_voice"] = True

    def dummy_print(self, state):
        print("This is a dummy print %s" % state)
        state["justaprop"] = "justavalue"

    def cleanup(self):
        self.mumble_client.disable_sound()
