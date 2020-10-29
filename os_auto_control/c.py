import json
import socket
import uuid
import pack.pyChrome as chrome
import configparser


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
    if rt['Code'] != 200:
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
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def set_seewo_class(id: str):
    path = r'C:\Users\class\AppData\Roaming\Seewo\SeewoLink\config.ini'
    config = configparser.ConfigParser()
    config.read(path)
    config.set('GENERAL', 'DeviceName', id)
    with open(path, 'w') as f:
        config.write(f)


# 参数
web = chrome.WebBrowser(False)
base_url = 'http://local.api.hzsgz.com/os_server'
__config = json.load(open(r'c:\tool\config.json'))
if get_mac_address() not in __config:
    __config[get_mac_address()] = {
        'is_init': False
    }
config = __config[get_mac_address()]
