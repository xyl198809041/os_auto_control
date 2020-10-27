import psutil
from os_auto_control import data, c
import schedule
from time import sleep
import os


# 任务函数
@c.try_function
def check_process():
    """
检查进程
    """
    processes = {p.name(): p for p in psutil.process_iter()}
    not_in_list = [name for name in processes if name not in data.process_white_list]
    [processes[name].kill() for name in not_in_list]


@c.try_function
def update_local_info():
    """
上传更新本机信息
    """
    rt = c.web.GetJson('%s/update?mac=%s&key=%s&value=%s' %
                       (c.base_url, c.get_mac_address(), "ip", c.get_ip_address()))
    if rt['code'] == 200:
        print('更新电脑信息完成')
    else:
        print(rt['msg'])


@c.try_function
def update_local_self():
    """
软件更新,重启后生效
    """
    rt = os.system(
        'pip install https://codeload.github.com/xyl198809041/os_auto_control/zip/master --upgrade --no-cache-dir')
    if rt == 1:
        raise Exception('软件更新失败')
    print('软件更新成功')


if __name__ == '__main__':
    # 测试
    print(c.get_ip_address())
    print(c.get_mac_address())
    update_local_self()
    # end测试
    schedule.every(10).seconds.do(check_process)
    schedule.every(1).hours.do(update_local_info).run()
    while True:
        schedule.run_pending()
        sleep(1)
