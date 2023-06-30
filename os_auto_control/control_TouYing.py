import time

import serial.tools.list_ports
import serial  # 导入串口通信库
from time import sleep
import cv2
import numpy as np

import pyautogui

img_list = []

diff_num = 0
temp = None

power_off = bytes.fromhex('50 57 52 20 4f 46 46 0d')
power_on = bytes.fromhex('50 57 52 20 4f 4e 0d')
power_state = bytes.fromhex('50 57 52 3f 0d')


class Serial_control:
    touYing_defaul = None

    @classmethod
    def check(cls):
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            s = cls(port.device)
            is_this = False
            try:
                s.port_open_recv()
                s.send(power_state)
                temp = s.recv()
                is_this = s.recv() == ':\r'
            finally:
                s.port_close()
                if is_this:
                    cls.touYing_defaul = s
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
            print("串口打开成功！")
        else:
            print("串口打开失败！")

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


Serial_control.check()


def do_TouYing(action=power_state, time_out=5):
    Serial_control.touYing_defaul.port_open_recv()
    Serial_control.touYing_defaul.send(action)
    rt = Serial_control.touYing_defaul.recv(time_out)
    Serial_control.touYing_defaul.port_close()
    return rt


def check_desktop(max_diff_num=10):
    """
检测桌面情况,并完成操作
    """
    global temp, diff_num
    pyautogui.screenshot("full_img.png")
    img = cv2.imread("full_img.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if temp is None:
        temp = img
    else:
        diff = cv2.absdiff(img, temp)
        diff = cv2.threshold(diff, 1, 1, cv2.THRESH_BINARY)[1]
        print('改变百分比:', np.sum(diff) / diff.size)
        if np.sum(diff) / diff.size > 0.001:
            diff_num = 0
            temp = img
        else:
            diff_num += 1
        print(diff_num)
    if diff_num > max_diff_num:
        if do_TouYing(power_state) != ':WR=00':
            try:
                return do_TouYing(power_off) == ':'
            except Exception as e:
                print(e)
                return False
        else:
            diff_num = 0 - max_diff_num
