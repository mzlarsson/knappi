
import threading

class MenuTraverser:

    def __init__(self, on_menu_traversal):
        # Local states
        self.menu = Menu("Welcome")
        self.menu.parent = self.menu
        self.active_menu = None
        self.state = {}
        self.on_menu_traversal = on_menu_traversal
        
    def prepare_menu(self):
        if not self.active_menu:
            if self.menu.child:
                self.active_menu = self.menu.child
            else:
                self.active_menu = self.menu
            self.on_menu_traversal()
                
    def goto_root(self):
        self.active_menu = self.menu
        self.on_menu_traversal()
        
    def prev(self):
        print("Move from %s to %s" % (self.active_menu.title, self.active_menu.prev.title))
        self.active_menu = self.active_menu.prev
        self.on_menu_traversal()
        
    def next(self):
        self.active_menu = self.active_menu.next
        self.on_menu_traversal()
        
    def back(self):
        if self.active_menu.in_action:
            self.active_menu.in_action = False
        else:
            self.active_menu = self.active_menu.parent
            self.active_menu.reset()
            self.on_menu_traversal()
        
    def enter(self):
        if self.active_menu.is_navigation_only():
            if self.active_menu.child:
                self.active_menu = self.active_menu.child
                self.on_menu_traversal()
        else:
            self.active_menu.in_action = True
            self.active_menu.do_action(self.state)
            
    def is_in_action(self):
        return self.active_menu is not None and self.active_menu.in_action
        
        
class Menu:

    def __init__(self, title):
        self.title = title
        self.prev = self
        self.next = self
        self.is_first = True
        self.is_last = True
        self.child = None
        self.parent = None
        self.action = None
        self.in_action = False
        
    def reset(self):
        if self.child:
            while not self.child.is_first:
                self.child = self.child.prev
            
    def add_submenu(self, submenu):
        submenu.parent = self
        if not self.child:
            self.child = submenu
        else:
            last = self.child
            while not last.is_last:
                last = last.next
            last.is_last = False
            submenu.is_last = True
            submenu.next = last.next
            submenu.prev = last
            submenu.next.prev = submenu
            last.next = submenu
            
    def is_navigation_only(self):
        return self.action is None
        
    def register_action(self, action):
        self.action = action
        
    def do_action(self, state):
        threading.Thread(target=self.action, args=(state,)).start()
        
    def stringify(self, tab=0, render_siblings=True):
        text = "%s[%s]%s\n" % ('\t'*tab, self.title, ' (active)' if self.in_action else '')
        
        if self.child:
            text += self.child.stringify(tab+1)

        if render_siblings:
            next_menu = self.next
            while next_menu != self:
                text += next_menu.stringify(tab, False)
                next_menu = next_menu.next
        return text
                