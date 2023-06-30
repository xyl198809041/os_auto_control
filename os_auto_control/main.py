import os
import tkinter
import tkinter.simpledialog
from time import sleep
import psutil
import schedule
from pack.tool import speak as tool_speck
from os_auto_control import data, c
from os_auto_control import control_TouYing


def speak(text):
    try:
        tool_speck(text)
    except Exception as e:
        print(e)


# 初始化
def init():
    if not c.config['is_init']:
        speak('系统已安装完成,开始配置,请等待')
        info = c.web_get_info()
        if info['data'] is None:
            def run_input():
                while True:
                    input_pcname = tkinter.simpledialog.askstring(title='配置', prompt='请输入计算机名,例如:101')
                    if input_pcname != '':
                        c.web_set_info(pc_name=input_pcname)
                        print(input_pcname)
                        root.destroy()
                        root.quit()
                        break

            root = tkinter.Tk()
            root.withdraw()
            root.after(1, run_input)
            root.mainloop()
            info = c.web_get_info()

        try:
            os.system(r'C:\tool\DrvCeonw\DrvCeox86.exe /a')
            c.wait_process_running('DrvCeox86.exe')
            c.set_seewo_class(info['data']['pc_name'])
            speak('配置已完成,正在重启')
            c.config['is_init'] = True
            c.config_save()
            os.system('shutdown -r -t 0')
        except Exception as e:
            print(e)


# 任务函数
@c.try_function
def shutdown():
    """
关机
    """
    os.system('shutdown -s -f -t 0')


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
                         not c.check_file_in_white_Copyright(processes[name].exe())]
    # 在黑名单中,直接杀了,并剔除
    black_list = [name for name in not_in_white_list if name in data.process_black_list]
    black_list.extend([name for name in not_in_white_list if
                       c.check_file_in_black_Copyright(processes[name].exe())])
    [processes[name].kill() for name in black_list]
    # if len(black_list) != 0:
    # speak('发现可疑软件在运行,系统已经将其封杀,如有疑问可以咨询许姚龙')
    c.web_update_processes_list('processes_black_list', black_list)
    print('黑名单,杀掉进程:', black_list)
    not_in_white_list = [name for name in not_in_white_list if name not in data.process_black_list]
    # 不在名单中的,再说

    # 不在所有名单中,提交
    not_in_white_list = [name for name in not_in_white_list if name not in data.process_not_in_list]
    print('灰名单,提交数据:', not_in_white_list)
    c.web_update_processes_list('processes_not_in_list', not_in_white_list)
    print(not_in_white_list)
    data.process_not_in_list.extend(not_in_white_list)


@c.try_function
def update_local_info():
    """
上传更新本机信息
    """
    c.web_login()


@c.try_function
def update_local_self():
    """
软件更新,重启后生效
    """
    if c.web_get_v():
        rt = os.system(
            'pip install https://codeload.github.com/xyl198809041/py_tool/zip/master --upgrade --no-cache-dir')
        rt = os.system(
            'pip install https://codeload.github.com/xyl198809041/os_auto_control/zip/master --upgrade --no-cache-dir')
        if rt == 1:
            raise Exception('软件更新失败')
        c.web_update_msg('正常', 'update')


def run():
    # 测试
    print(data.v)
    print(c.get_ip_address())
    print(c.get_mac_address())
    pass
    # end测试
    init()
    schedule.every(1).minutes.do(update_local_self).run()
    schedule.every(5).seconds.do(check_process)
    schedule.every(1).minutes.do(update_local_info).run()
    schedule.every(1).seconds.do(control_TouYing.check_desktop,
                                 serial_TouYing=control_TouYing.Serial_control.check())
    if c.config['auto_shutdown']:
        schedule.every(1).days.at('21:00').do(shutdown)
    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    # 测试
    run()
