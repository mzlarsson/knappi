
import pymumble_py3 as pymumble
from pymumble_py3.callbacks import *

import pyaudio
from time import sleep
import threading

class MumbleHandler:

    def __init__(self, nick, server="localhost", pwd="humbug"):
        self.playback_handlers = []
        self.sound_activated = False
    
        self.mumble = pymumble.Mumble(server, nick, password=pwd, reconnect=True)
        self.mumble.callbacks.set_callback(PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, self._on_text_message_received)
        self.mumble.callbacks.set_callback(PYMUMBLE_CLBK_CONNECTED, self._on_connected)
        self.mumble.callbacks.set_callback(PYMUMBLE_CLBK_DISCONNECTED, self._on_disconnected)
        self.mumble.callbacks.set_callback(PYMUMBLE_CLBK_USERCREATED, self._on_user_added)
        self.mumble.callbacks.set_callback(PYMUMBLE_CLBK_USERUPDATED, self._on_user_changed)
        self.mumble.callbacks.set_callback(PYMUMBLE_CLBK_USERREMOVED, self._on_user_removed)
        self.mumble.set_receive_sound(1)  # we want to receive sound
        self.mumble.start()
        self.mumble.is_ready()            # wait for connection
        
        # Connected!
        self.mumble.users.myself.mute()   # we don't want to send sound
                
    def _enable_sound_for_user_if_needed(self, user):
        if self.sound_activated:
            channel_id = self.mumble.users.myself["channel_id"]
            if user != self.mumble.users.myself and user["channel_id"] == channel_id:
                new_handler = PlaybackHandler(user)
                new_handler.start_playback()
                self.playback_handlers.append(new_handler)
                
    def _disable_sound_for_user_if_needed(self, user):
        handler_to_remove = None
        for handler in self.playback_handlers:
            if handler.user["name"] == user["name"]:
                handler_to_remove = handler
                break
                
        if handler_to_remove:
            handler_to_remove.stop_playback()
            self.playback_handlers.remove(handler_to_remove)
        
    def _on_user_added(self, user):
        self._enable_sound_for_user_if_needed(user)
        
    def _on_user_removed(self, user, msg):
        self._disable_sound_for_user_if_needed(user)
        
    def _on_user_changed(self, user, actions):
        if actions.get("self_mute") is not None:
            if actions["self_mute"]:
                print("%s is self-muted" % (user["name"]))
            else:
                print("%s is no longer self-muted" % (user["name"]))
        elif actions.get("channel_id") is not None:
            channel = self.mumble.channels[actions["channel_id"]]
            print("%s joined %s" % (user["name"], channel["name"]))
            
            if self.sound_activated:
                if actions["channel_id"] == self.mumble.users.myself["channel_id"]:
                    self._enable_sound_for_user_if_needed(user)
                else:
                    self._disable_sound_for_user_if_needed(user)
        else:
            print(actions)

    def _on_text_message_received(self, msg):
        # sending the received sound back to server
        user = self.mumble.users[msg.actor]["name"]
        message = msg.message.strip() 
        print("%s: %s" % (user, message))
        
    def _on_connected(self):
        print("Connected to the server")

    def _on_disconnected(self):
        print("Disconnected from the server")


    def disable_sound(self):
        for handler in self.playback_handlers:
            handler.stop_playback()
            
        self.playback_handlers = []
        self.sound_activated = False
        
    def enable_sound(self):    
        self.disable_sound()   # Reset old handlers
        
        self.sound_activated = True        
        for user in self.mumble.users.values():
            self._enable_sound_for_user_if_needed(user)
    
    def join_channel(self, channel_name):
        channel = self.mumble.channels.find_by_name(channel_name)
        if channel:
            channel.move_in()
            
    def print_state(self):
        channel_id = self.mumble.users.myself["channel_id"]
        channel = self.mumble.channels[channel_id]
        
        userinfos = []
        for user in self.mumble.users.values():
            if user["channel_id"] == channel_id:
                userinfo = user["name"]
                if user.get("self_mute"):
                    userinfo += " [self-muted]"
                userinfos.append(userinfo)
                
        print("| ==========================================")
        print("| Currently in channel %s" % channel["name"])
        for userinfo in userinfos:
            print("| \t%s" % userinfo)
        print("| ==========================================")
        
class PlaybackHandler:

    def __init__(self, mumble_user):
        self.user = mumble_user
        self.stop = True
        self.muted = False
        self.run_thread = None
        
    def start_playback(self):
        print("Starting playback for user %s" % self.user["name"])
        self.run_thread = threading.Thread(target=self.run_playback)
        self.run_thread.start()
    
    def run_playback(self):
        self.p_audio = pyaudio.PyAudio()
        self.stream = self.p_audio.open(input=False,
                                        output=True,
                                        channels=1,
                                        format=pyaudio.paInt16,
                                        rate=pymumble.constants.PYMUMBLE_SAMPLERATE,
                                        frames_per_buffer=1024)
                                        
        self.stop = False
        while not self.stop:
            while not self.stop and not self.user.sound.is_sound():
                sleep(0.1)
                
            while not self.stop and self.user.sound.is_sound():
                data = self.user.sound.get_sound(1024).pcm
                if not self.muted:
                    self.stream.write(data)
            
        print("Stopped feeding sound from %s" % self.user["name"])
        
    def stop_playback(self):
        self.stop = True