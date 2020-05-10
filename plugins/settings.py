
def get_plugin():
    return Settings()

class Settings:

    def __init__(self):
        pass
        
    def get_name(self):
        return "Settings"
        
    def get_prio(self):
        return 1
        
    def setup(self, parent_menu):
        pass

    def cleanup(self):
        pass