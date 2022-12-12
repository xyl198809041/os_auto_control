import time

import os_auto_control.c as c
import os_auto_control.main as m
import tkinter
import tkinter.simpledialog


time.sleep(10)
a = c.web_get_info()
print(a)
