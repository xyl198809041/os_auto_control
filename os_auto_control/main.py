import psutil
from os_auto_control import data, c
import schedule
from time import sleep
import os
from pack.tool import speak
import os
from time import sleep

import psutil
import schedule
from pack.tool import speak

from os_auto_control import data, c


# 初始化
def init():
    if not c.config['is_init']:
        speak('我已安装完成,开始初始化,请等待')
        os.system(r'C:\tool\DrvCeonw\DrvCeox86.exe /a')
        info = c.web_get_info()
        c.set_seewo_class(info['name'])
        speak('初始化已完成,正在重启')
        c.config['is_init'] = True
        c.config_save()
        os.system('shutdown -r -t 0')


# 任务函数
@c.try_function
def check_process():
    """
检查进程
    """
    processes = {p.name(): p for p in psutil.process_iter()}
    # 不在所有名单中,提交
    not_in_list = [name for name in processes if
                   name not in data.process_not_in_list and
                   name not in data.process_white_list and
                   name not in data.process_black_list]
    [c.web_update('processes_not_in_list', name) for name in not_in_list]
    data.process_not_in_list.extend(not_in_list)
    # 在黑名单中,直接杀了
    not_in_list = [name for name in processes if name in data.process_black_list]
    [processes[name].kill() for name in not_in_list]
    # 不在白名单中,再说
    not_in_list = [name for name in processes if name not in data.process_white_list]
    # [processes[name].kill() for name in not_in_list]


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
        'pip install https://codeload.github.com/xyl198809041/os_auto_control/zip/master --upgrade --no-cache-dir')
    if rt == 1:
        raise Exception('软件更新失败')
    c.web_update('update', '0')


if __name__ == '__main__':
    # 测试
    print(c.get_ip_address())
    print(c.get_mac_address())
    c.set_seewo_class('222')
    # end测试
    schedule.every(1).days.at('12:00').do(update_local_self).run()
    schedule.every(10).seconds.do(check_process)
    schedule.every(1).hours.do(update_local_info).run()
    while True:
        schedule.run_pending()
        sleep(1)
