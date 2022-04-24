from Utils import dict_result, say_something
import threading
import requests
import json
import os
import sys

def get_initial_data():
    initial_data = {
        "sessionid":"",
        "auto_danmu":True,
        "danmu_limit":10,
        "im_called":False
    }
    return initial_data

def initialize_config():
    initial_data = {
        "sessionid":"",
        "auto_danmu":True,
        "danmu_limit":10,
        "im_called":False
    }
    f = open(r"./config.json","w+")
    json.dump(initial_data,f)
    f.close()

def get_user_info():
    r = requests.get(url="https://www.yuketang.cn/api/v3/user/basic-info",headers=headers)
    rtn = dict_result(r.text)
    return (rtn["code"],rtn["data"])

def get_on_lesson():
    r = requests.get("https://www.yuketang.cn/api/v3/classroom/on-lesson",headers=headers)
    rtn = dict_result(r.text)
    return (rtn["code"],rtn["data"]["onLessonClassrooms"])

if not os.path.exists("./config.json"):
    initialize_config()
f = open(r"./config.json","r")
data_dict = json.load(f)
initial_data  = get_initial_data()
SESSIONID = data_dict.get("sessionid",None)
AUTO_DANMU = data_dict.get("auto_danmu",initial_data["auto_danmu"])
DANMU_LIMIT = data_dict.get("danmu_limit",initial_data["danmu_limit"])
IM_CALLED = data_dict.get("im_called",initial_data["im_called"])
headers = {
    "Cookie":"sessionid=%s" % SESSIONID,
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
}
code,user_info = get_user_info()
if code == 50000:
    meg = "sessionid有误，请检查config.json"
    speak_thread = threading.Thread(target=say_something,args=(meg,))
    speak_thread.start()
    speak_thread.join()
    sys.exit()
elif code == 0:
    UID = user_info["id"]
    UNAME = user_info["name"]
f.close()