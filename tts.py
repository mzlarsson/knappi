
import threading
import subprocess
import os

def say(text):
    threading.Thread(target=run_say, args=(text,)).start()
    
def run_say(text):
    subprocess.call(["espeak", text], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)