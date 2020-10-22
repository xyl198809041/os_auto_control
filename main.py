import psutil
import data
import schedule
from time import sleep
import c


# 任务函数
def check_process():
    """
检查进程
    """
    processes = {p.name(): p for p in psutil.process_iter()}
    [processes[name].kill() for name in processes if name not in data.process_white_list]


@c.try_function
def update_local_info():
    """
上传更新本机信息
    """
    c.web.GetJson('%s/update?mac=%s&key=%s&value=%s' %
                  (c.base_url, c.get_mac_address(), "ip", c.get_ip_address()))


if __name__ == '__main__':
    # 测试
    print(c.get_ip_address())
    print(c.get_mac_address())
    # end测试
    schedule.every(10).seconds.do(check_process)
    schedule.every(1).hours.do(update_local_info).run()
    while True:
        schedule.run_pending()
        sleep(1)
