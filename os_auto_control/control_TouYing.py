import time
import tkinter

import serial.tools.list_ports
import serial  # 导入串口通信库
from time import sleep
import cv2
import numpy as np

import pyautogui

img_list = []

diff_num = 0
temp_screen = None
mouse_num = 0
mouse_countdown = 0
is_need_cancel = False

power_off = bytes.fromhex('50 57 52 20 4f 46 46 0d')
power_on = bytes.fromhex('50 57 52 20 4f 4e 0d')
power_state = bytes.fromhex('50 57 52 3f 0d')
LAMP = bytes.fromhex('4c 41 4d 50 3f 0d')


class Serial_control:
    touYing_defaul = None
    touYing_state = 'X'

    @classmethod
    def check(cls):
        port_list = list(serial.tools.list_ports.comports())
        print(port_list)
        for port in port_list:
            s = cls(port.device)
            is_this = False
            temp = cls.touYing_state
            try:
                s.port_open_recv()
                s.send(power_state)
                temp = s.recv()
                is_this = temp.find('R') >= 0
            except:
                try:
                    s.port_close()
                except Exception:
                    print(1)
            if is_this:
                cls.touYing_state = temp.replace('=', '')
                cls.touYing_defaul = s
                print(s)
                return s

    def __init__(self, com_num='com5'):
        self.com_mun = com_num
        self.ser = None

    def port_open_recv(self):  # 对串口的参数进行配置
        self.ser = serial.Serial()  # 创建一个串口对象
        self.ser.port = self.com_mun  # 设置串口号
        self.ser.baudrate = 9600  # 设置波特率
        self.ser.bytesize = 8  # 设置数据位数
        self.ser.stopbits = 1  # 设置停止位
        self.ser.parity = "N"
        self.ser.open()  # 打开串口
        if self.ser.isOpen():
            print(f"串口{self.com_mun}打开成功！")
        else:
            print(f"串口{self.com_mun}打开失败！")

    def port_close(self):  # 关闭串口
        self.ser.close()
        if self.ser.isOpen():
            print("串口关闭失败！")
        else:
            print("串口关闭成功！")
        self.ser = None

    def send(self, send_data: bytes):  # 发送数据到串口
        if self.ser.isOpen():
            self.ser.write(send_data)  # 将字符串转换为字节并发送
            print("发送成功！", send_data.decode('utf8'))
        else:
            print("发送失败！")

    def recv(self, outtime=5) -> str:
        s = ''
        for i in range(outtime):
            if self.ser.in_waiting:
                recv_data = self.ser.read(self.ser.in_waiting)
                s += recv_data.decode('utf-8')
                i -= 1
            else:
                time.sleep(1)
        print(s)
        return s


def do_TouYing(serial_TouYing, action=power_state, time_out=5):
    for i in range(3):
        try:
            serial_TouYing.port_open_recv()
            serial_TouYing.send(bytes.fromhex('0d'))
            serial_TouYing.recv(3)
            serial_TouYing.send(action)
            rt = serial_TouYing.recv(time_out)
            serial_TouYing.port_close()
            if action == power_state:
                Serial_control.touYing_state = str(rt).replace('=', '')
            return rt
        except Exception as e:
            print('投影控制错误:', e)


def win_to_cancel() -> bool:
    global mouse_num, mouse_countdown, is_need_cancel
    mouse_num = 0
    mouse_countdown = 30  # 倒计时秒

    def do():
        global mouse_countdown, is_need_cancel
        label.config(text=f'投影即将关机\n需要取消请移动鼠标\n剩余时间{mouse_countdown}秒', font=("微软雅黑", 30))
        mouse_countdown -= 1
        if mouse_countdown < 0:
            is_need_cancel = False
            root.destroy()
        if mouse_num < 10:
            root.after(1000, do)
        else:
            is_need_cancel = True
            root.destroy()

    def mouse(event):
        global mouse_num
        mouse_num += 1

    root = tkinter.Tk()
    root.state("zoomed")
    label = tkinter.Label(root)
    label.pack(expand=True)
    root.bind('<Motion>', mouse)
    root.attributes("-topmost", True)
    do()
    root.mainloop()
    return is_need_cancel


def check_desktop(serial_TouYing, max_diff_num=10):
    """
检测桌面情况,并完成操作
max_diff_num 设置时间(分钟)
    """
    global temp_screen, diff_num
    pyautogui.screenshot("full_img.png")
    img = cv2.imread("full_img.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if temp_screen is None:
        temp_screen = img
    else:
        diff = cv2.absdiff(img, temp_screen)
        diff = cv2.threshold(diff, 1, 1, cv2.THRESH_BINARY)[1]
        print('改变百分比:', np.sum(diff) / diff.size)
        if np.sum(diff) / diff.size > 0.001:
            diff_num = min(0, diff_num + 1)
            temp_screen = img
        else:
            diff_num += 1
        print(diff_num)
    if diff_num > max_diff_num:
        if do_TouYing(serial_TouYing, power_state).find('WR=00') == -1:
            if not win_to_cancel():
                try:
                    return do_TouYing(serial_TouYing, power_off) == ':'
                except Exception as e:
                    print(e)
            else:
                diff_num = 0 - max_diff_num * 2
        else:
            diff_num = 0 - max_diff_num
