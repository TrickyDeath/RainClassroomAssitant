from Utils import say_something, test_network
from Classes import Lesson
from GetInfo import get_on_lesson
import requests
import threading
import time

def del_onclass(lesson_obj):
    on_lesson_list.remove(lesson_obj)

if __name__ == "__main__":
    on_lesson_list = []
    lesson_list = []
    user_dict = {}
    meg = "雨课堂监听已开启"
    threading.Thread(target=say_something,args=(meg,)).start()
    network_status = True
    while True:
        try:
            lesson_list = get_on_lesson()
        except requests.exceptions.ConnectionError:
            meg = "网络异常，监听中断"
            threading.Thread(target=say_something,args=(meg,)).start()
            network_status = False
        except Exception:
            pass

        while not network_status:
            ret = test_network()
            if ret == True:
                try:
                    lesson_list = get_on_lesson()
                except:
                    pass
                else:
                    network_status = True
                    meg = "网络已恢复，监听开始"
                    threading.Thread(target=say_something,args=(meg,)).start()
                    break
            time.sleep(5)
            
        for lesson in lesson_list:
            lessionid = lesson["lessonId"]
            lessonname = lesson["courseName"]
            lesson_obj = Lesson(lessionid,lessonname)
            if lesson_obj not in on_lesson_list:
                thread = threading.Thread(target=lesson_obj.start_lesson,args=(del_onclass,))
                thread.start()
                meg = "检测到课程%s正在上课，已加入自动提醒列表" % lessonname
                threading.Thread(target=say_something,args=(meg,)).start()
                on_lesson_list.append(lesson_obj)
        time.sleep(30)
