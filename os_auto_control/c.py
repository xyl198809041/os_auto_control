import socket
import uuid
import pack.pyChrome as chrome

# 参数
web = chrome.WebBrowser(False)
base_url = 'http://local.api.hzsgz.com/os_server'


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


def try_function(func):
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
