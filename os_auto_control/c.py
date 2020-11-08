import json
import socket
import time
import uuid
import pack.pyChrome as chrome
import configparser
import psutil
import win32api

from os_auto_control import data


def config_save():
    with open(r'c:\tool\config.json', 'w') as f:
        f.write(json.dumps(__config))


def web_update(key: str, value: str, mac: str = ''):
    """
上传更新本机信息
    """
    if mac == '':
        mac = get_mac_address()
    rt = web.GetJson('%s/update?mac=%s&key=%s&value=%s' %
                     (base_url, mac, key, value))
    if rt['code'] == 200:
        print('更新' + key + '成功')
    else:
        print(rt['msg'])


def web_msg(msg: str, type: str):
    """
上报消息
    :param msg:
    :param type:
    """
    web.GetJson('%s/msg?mac=%s&type=%s&msg=%s' % (base_url, get_mac_address(), type, msg))


def web_get_info():
    rt = web.GetJson('%s/get_info?mac=%s' % (base_url, get_mac_address()))
    if rt['code'] != 200:
        raise Exception('获取主机信息错误')
    return rt


def try_function(func):
    """
设置错误上传服务器
    :param func:
    :return:
    """

    def new_func():
        try:
            func()
        except Exception as e:
            print(str(e))
            web_msg(str(e), 'system_error')
    return new_func


# 自定义函数
def get_ip_address():
    """
获取ip
    :return:
    """
    return socket.gethostbyname(socket.gethostname())


def get_mac_address():
    """
获取mac
    :return:
    """
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)]).upper()


def set_seewo_class(id: str):
    path = r'C:\Users\class\AppData\Roaming\Seewo\SeewoLink\config.ini'
    config = configparser.ConfigParser()
    config.read(path)
    config.set('GENERAL', 'DeviceName', id)
    with open(path, 'w') as f:
        config.write(f)


def wait_process_running(process: str):
    """
等待进程运行结束
    :param process:
    """
    while True:
        process_list = [p.name() for p in psutil.process_iter()]
        if process in process_list:
            time.sleep(10)
        else:
            return


def chece_file_in_white_Copyright(file: str):
    """
获取文件的版本信息
    :param file:
    :return:
    """
    translation = win32api.GetFileVersionInfo(file, '\\VarFileInfo\\Translation')[0]
    c = win32api.GetFileVersionInfo(file,
                                    u'\\StringFileInfo\\%04X%04X\\%s' %
                                    (translation[0], translation[1], 'LegalCopyright'))
    for item in data.Copyright_white_list:
        if item in c:
            return True
    return False


# 参数
web = chrome.WebBrowser(False)
base_url = 'http://local.api.hzsgz.com/os_server'
__config = json.load(open(r'c:\tool\config.json'))
if get_mac_address() not in __config:
    __config[get_mac_address()] = {
        'is_init': False
    }
config = __config[get_mac_address()]
