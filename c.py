import socket
import uuid
import pack.pyChrome as chrome

# 参数
web = chrome.WebBrowser(False)
base_url = 'http://local.api.hzsgz.com/os_server'


def try_function(func):
    def new_func():
        try:
            func()
        except Exception as e:
            update_error(str(e), 'system_error')
    return new_func


def update_error(msg: str, type: str):
    web.GetJson('%s/msg?mac=%s&type=%s&msg=%s' % (base_url, get_mac_address(), type, msg))


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
