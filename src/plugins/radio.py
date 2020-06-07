
import os
from os.path import isfile, join
from menu import Menu

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def get_plugin():
    return Radio("resources")

class Radio:

    def __init__(self, path):
        self.path = path
        self.songs = [f for f in os.listdir(path) if isfile(join(path, f)) and self.is_audio_file(f)]
        pygame.mixer.init()
        
    def get_name(self):
        return "Radio"
        
    def get_prio(self):
        return 900
        
    def setup(self, parent_menu):
        play_item = Menu("Play")
        parent_menu.add_submenu(play_item)
        stop_item = Menu("Stop")
        stop_item.register_action(self.stop_song)
        parent_menu.add_submenu(stop_item)
    
        for song in self.songs:
            item = Menu(".".join(song.split(".")[:-1]))
            item.register_action(lambda state, song=song: self.play_song(song, state))
            play_item.add_submenu(item)
        
    def is_audio_file(self, file):
        return file.endswith(".mp3") or file.endswith(".wav")
        
    def play_song(self, song, state):
        print("Playing %s" % song)
        self.stop_song(state)
        
        if state.get("display"):
            state["display"].set_text("Playing!", center=True)

        radio_state = self.get_radio_state(state)
        radio_state["current_song"] = song
        pygame.mixer.music.load(join(self.path, song))
        pygame.mixer.music.play()
        
    def stop_song(self, state):
        radio_state = self.get_radio_state(state)
        if radio_state.get("current_song"):
            pygame.mixer.music.stop()
            radio_state["current_song"] = None
        pygame.mixer.quit()
        pygame.mixer.init()

    def get_radio_state(self, state):
        if not state.get("radio"):
            state["radio"] = {}
        return state["radio"]

    def cleanup(self):
        pass
