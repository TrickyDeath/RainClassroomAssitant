import threading
import pyttsx3
import json
import urllib3
import requests
import random
import os
import sys

lock = threading.Lock()

def say_something(text):
    # 带线程锁的语音函数
    lock.acquire()
    pyttsx3.speak(text)
    lock.release()
    
def dict_result(text):
    # json string 转 dict object
    return dict(json.loads(text))

def test_network():
    # 网络状态测试
    try:
        http = urllib3.PoolManager()
        http.request('GET', 'https://baidu.com')
        return True
    except:
        return False

def calculate_waittime(limit, type, custom_time):
    # 计算答题等待时间
    '''
    type
    1: 随机
    2: 自定义
    '''
    def default_calculate(limit):
        # 默认的随机答题等待时间算法
        if limit == -1:
            wait_time = random.randint(5,20)
        else:
            if limit > 15:
                wait_time = random.randint(5,limit-10)
            else:
                wait_time = 0
        return wait_time

    if type == 1:
        wait_time = default_calculate(limit)
    elif type == 2:
        # 如果自定义等待时间超过当前题目的剩余时间，则采用默认算法
        if custom_time > limit:
            wait_time = default_calculate(limit)
        else:
            wait_time = custom_time
    return wait_time

def get_initial_data():
    # 默认配置信息
    initial_data = \
    {
        "sessionid":"",
        "auto_danmu":True,
        "danmu_config":{
            "danmu_limit":5
        },
        "audio_on":True,
        "audio_config":{
            "audio_type":{
                "send_danmu":False,
                "others_danmu":False,
                "receive_problem":True,
                "answer_result":True,
                "im_called":True,
                "others_called":True,
                "course_info":True,
                "network_info":True
            }
        },
        "auto_answer":True,
        "answer_config":{
            "answer_delay":{
                "type":1,
                "custom":{
                    "time":0
                }
            }
        }
    }
    return initial_data

def get_config_path():
    # 获取配置文件路径
    config_route = get_config_dir() + "\\config.json"
    return config_route

def get_config_dir():
    # 获取配置文件所在文件夹
    appdata_route = os.environ['APPDATA']
    dir_route = appdata_route + "\\RainClassroomAssistant"
    return dir_route

def get_user_info(sessionid):
    # 获取用户信息
    headers = {
        "Cookie":"sessionid=%s" % sessionid,
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    }
    r = requests.get(url="https://www.yuketang.cn/api/v3/user/basic-info",headers=headers,proxies={"http": None,"https":None})
    rtn = dict_result(r.text)
    return (rtn["code"],rtn["data"])

def get_on_lesson(sessionid):
    # 获取用户当前正在上课列表
    headers = {
        "Cookie":"sessionid=%s" % sessionid,
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    }
    r = requests.get("https://www.yuketang.cn/api/v3/classroom/on-lesson",headers=headers,proxies={"http": None,"https":None})
    rtn = dict_result(r.text)
    return rtn["data"]["onLessonClassrooms"]

def get_on_lesson_old(sessionid):
    # 获取用户当前正在上课的列表（旧版）
    headers = {
        "Cookie":"sessionid=%s" % sessionid,
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    }
    r = requests.get("https://www.yuketang.cn/v/course_meta/on_lesson_courses",headers=headers,proxies={"http": None,"https":None})
    rtn = dict_result(r.text)
    return rtn["on_lessons"]

def resource_path(relative_path):
    # 解决打包exe的图片路径问题
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)