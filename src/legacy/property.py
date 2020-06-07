

class Property(object):

    def __init__(self, default_value):
        self.value = default_value
        self.change_listeners = []
        
    def getValue(self):
        return self.value
        
    def setValue(self, new_value):
        self.value = new_value
        
        for listener in self.change_listeners:
            listener(new_value)
            
    def listen(self, listener):
        self.change_listeners.append(listener)
        
    def unlisten(self, listener):
        try:
            self.change_listeners.remove(listener)
        except ValueError:
            print("Warning: Failed to unlisten to property, no such listener found")
        