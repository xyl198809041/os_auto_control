import os
from time import sleep

import psutil
import schedule
from pack.tool import speak

from os_auto_control import data, c


# 初始化
def init():
    if not c.config['is_init']:
        speak('我已安装完成,开始配置,请等待')
        os.system(r'C:\tool\DrvCeonw\DrvCeox86.exe /a')
        c.wait_process_running('DrvCeox86.exe')
        info = c.web_get_info()
        c.set_seewo_class(info['data']['name'])
        speak('配置已完成,正在重启')
        c.config['is_init'] = True
        c.config_save()
        os.system('shutdown -r -t 0')


# 任务函数
@c.try_function
def check_process():
    """
检查进程
    """
    # 白名单剔除
    processes = {p.name(): p for p in psutil.process_iter()}
    psutil.Process().exe()
    not_in_white_list = [name for name in processes if name not in data.process_white_list]
    not_in_white_list = [name for name in not_in_white_list if
                         not c.chece_file_in_white_Copyright(processes[name].exe())]
    # 在黑名单中,直接杀了,并剔除
    black_list = [name for name in not_in_white_list if name in data.process_black_list]
    [processes[name].kill() for name in black_list]
    print('黑名单,杀掉进程:', black_list)
    not_in_white_list = [name for name in not_in_white_list if name not in data.process_black_list]
    # 不在名单中的,再说

    # 不在所有名单中,提交
    not_in_white_list = [name for name in not_in_white_list if name not in data.process_not_in_list]
    print('灰名单,提交数据:', not_in_white_list)
    [c.web_update('processes_not_in_list', name) for name in not_in_white_list]
    data.process_not_in_list.extend(not_in_white_list)


@c.try_function
def update_local_info():
    """
上传更新本机信息
    """
    c.web_update('ip', c.get_ip_address())


@c.try_function
def update_local_self():
    """
软件更新,重启后生效
    """
    rt = os.system(
        'pip install https://codeload.github.com/xyl198809041/py_tool/zip/master --upgrade --no-cache-dir')
    rt = os.system(
        'pip install https://codeload.github.com/xyl198809041/os_auto_control/zip/master --upgrade --no-cache-dir')
    if rt == 1:
        raise Exception('软件更新失败')
    c.web_update('update', '0')


def run():
    # 测试
    print(c.get_ip_address())
    print(c.get_mac_address())
    # end测试
    init()
    schedule.every(1).days.at('12:00').do(update_local_self).run()
    schedule.every(10).seconds.do(check_process)
    schedule.every(1).hours.do(update_local_info).run()
    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    # 测试
    run()
