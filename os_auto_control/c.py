import json
import os.path
import socket
import time
import uuid
from enum import Enum

import pack.pyChrome as chrome
import configparser
import psutil
import schedule
import win32api
from typing import List

from os_auto_control import data


def config_save():
    with open(r'c:\tool\config.json', 'w') as f:
        f.write(json.dumps(__config))


def web_login(tou_Ying_state):
    mac = get_mac_address()
    rt = web.GetJson(base_url + f'update_login?mac={mac}&ip={get_ip_address()}&v={data.v}&touYing={tou_Ying_state}')
    if rt['code'] == 200:
        print('login 成功')
    else:
        print(rt['msg'])


def web_update_processes_list(list_type: str, list_data: List[str]):
    mac = get_mac_address()
    rt = web.GetJson(
        f'{base_url}update_processes_list?mac={mac}&list_type={list_type}&list_data={json.dumps(list_data)}')
    if rt['code'] == 200:
        print('update_processes_list 成功')
    else:
        print(rt['msg'])


def web_update_msg(msg: str, msg_type: str):
    mac = get_mac_address()
    rt = web.GetJson(
        f'{base_url}update_msg?mac={mac}&msg_type={msg_type}&msg={msg}')
    if rt['code'] == 200:
        print('msg update 成功')
    else:
        print(rt['msg'])


def web_get_info():
    mac = get_mac_address()
    rt = web.GetJson(
        f'{base_url}get_info?mac={mac}')
    if rt['code'] == 200:
        return rt
    else:
        raise Exception('获取主机信息错误')


def web_set_info(pc_name=''):
    if pc_name == '':
        pc_name = input()
    mac = get_mac_address()
    rt = web.GetJson(f'{base_url}regedit?mac={mac}&pc_name={pc_name}')


def web_get_v():
    """
获取版本号
    :return:
    """
    rt = web.GetJson(f'{base_url}v')
    try:
        if rt['msg'] > data.server_v:
            data.server_v = rt['msg']
            return True
        else:
            return False
    except:
        return False


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
            print(func.__name__)
            try:
                web_update_msg(str(e), 'system_error')
            except:
                print('错误无法上传')

    return new_func


# old

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
    try:
        path = r'C:\Users\class\AppData\Roaming\Seewo\SeewoLink\config.ini'
        config = configparser.ConfigParser()
        config.read(path)
        config.set('GENERAL', 'DeviceName', id)
        with open(path, 'w') as f:
            config.write(f)
    except Exception as e:
        raise Exception('希沃初始化配置失败')


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


def check_file_in_white_Copyright(file: str):
    """
获取文件的版本信息
    :param file:
    :return:
    """
    # print(file)
    try:
        translation = win32api.GetFileVersionInfo(file, '\\VarFileInfo\\Translation')[0]
        c = win32api.GetFileVersionInfo(file,
                                        u'\\StringFileInfo\\%04X%04X\\%s' %
                                        (translation[0], translation[1], 'ProductName'))
        for item in data.Copyright_white_list:
            if item in c:
                return True
        return False
    except:
        return False


def check_file_in_black_Copyright(file: str):
    """
获取文件的版本信息
    :param file:
    :return:
    """
    # print(file)
    try:
        translation = win32api.GetFileVersionInfo(file, '\\VarFileInfo\\Translation')[0]
        c = win32api.GetFileVersionInfo(file,
                                        u'\\StringFileInfo\\%04X%04X\\%s' %
                                        (translation[0], translation[1], 'ProductName'))
        for item in data.Copyright_back_list:
            if item in c:
                return True
        return False
    except:
        return False


def run_job_by_web():
    rt = web.GetJson(base_url + f'get_job_by_mac?mac={get_mac_address()}')
    job_list = rt['data']
    for job in job_list:
        local_job = schedule.get_jobs(job['job_name'])
        if len(local_job) > 0:
            update_job_done_info(job=job, done_type=Done_type.running)
            local_job[0].job_func()
            update_job_done_info(job=job, done_type=Done_type.done)
    print('run_job_by_web', '成功')


class Done_type(Enum):
    done = '5'
    error = '-1'
    running = '1'
    wait = '0'
    delete = '-5'


def update_job_done_info(job, done_type: Done_type, msg=''):
    """
任务完成后上传记录
    :param job: 任务内容
    :param done_type: 完成情况
    :param msg: 信息
    """
    rt = web.GetJson(
        base_url +
        f'update_job_done?mac={get_mac_address()}&job_id={job["_id"]}&done_type={done_type.value}&msg={msg}')
    if rt['code'] == 200:
        print('上传任务执行记录成功', job)
    else:
        print('上传任务执行记录成功', job)


# 参数
web = chrome.WebBrowser(False)
base_url = 'https://local.api.hzsgz.com:8443/os_server/'
# base_url = 'http://localhost:93/os_server/'
if not os.path.exists(r'c:\tool'):
    os.mkdir(r'c:\tool')
if not os.path.exists(r'c:\tool\config.json'):
    open(r'c:\tool\config.json', 'w+').write('{}')
__config = json.load(open(r'c:\tool\config.json'))
if get_mac_address() not in __config:
    __config[get_mac_address()] = {
        'is_init': False,
        'auto_shutdown': True
    }
config = __config[get_mac_address()]
if 'auto_shutdown' not in config:
    config['auto_shutdown'] = True

config_save()
