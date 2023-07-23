from os_auto_control import c
from os_auto_control.control_TouYing import *


def job_open_TouYing():
    """
打开投影机
    :return:
    """
    if Serial_control.touYing_defaul is None:
        return Serial_control.touYing_state
    else:
        return do_TouYing(Serial_control.touYing_defaul, action=power_on)
