import os
import sys
import time

import os_auto_control.c as c
import os_auto_control.main as m
import tkinter
import tkinter.simpledialog


p = sys.executable

print(p)
time.sleep(10)
os.execl(p,*sys.argv)