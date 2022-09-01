import time
import requests
import threading
from Scripts.Utils import get_on_lesson, test_network
from Scripts.Classes import Lesson

def monitor(main_ui):
    # 监听器函数

    def del_onclass(lesson_obj):
        # 作为回调函数传入start_lesson
        on_lesson_list.remove(lesson_obj)

    # 已经签到完成加入监听列表的课程
    on_lesson_list = []
    # 检测到的未加入监听列表的课程
    lesson_list = []
    network_status = True
    sessionid = main_ui.config["sessionid"]
    while True:
        # 获取课程列表
        try:
            lesson_list = get_on_lesson(sessionid)
            # lesson_list_old = get_on_lesson_old()
        except requests.exceptions.ConnectionError:
            meg = "网络异常，监听中断"
            main_ui.add_message_signal.emit(meg,8)
            network_status = False
        except Exception:
            pass
        # 网络异常处理
        while not network_status:
            ret = test_network()
            if ret == True:
                try:
                    lesson_list = get_on_lesson(sessionid)
                    # lesson_list_old = get_on_lesson_old()
                except:
                    pass
                else:
                    network_status = True
                    meg = "网络已恢复，监听开始"
                    main_ui.add_message_signal.emit(meg,8)
                    break
            # 可结束线程的计时器
            timer = 0
            while timer <= 5:
                time.sleep(1)
                timer += 1
                if not main_ui.is_active:
                    # 由于on_lesson_list在多线程操作之下，此处必须使用列表复制，以保证列表完整性
                    for lesson in on_lesson_list.copy():
                        lesson.wsapp.close()
                    return
        # 课程列表
        for lesson in lesson_list:
            lessionid = lesson["lessonId"]
            lessonname = lesson["courseName"]
            classroomid = lesson["classroomId"]
            lesson_obj = Lesson(lessionid,lessonname,classroomid,main_ui)
            if lesson_obj not in on_lesson_list:
                thread = threading.Thread(target=lesson_obj.start_lesson,args=(del_onclass,),daemon=True)
                thread.start()
                meg = "检测到课程%s正在上课，已加入监听列表" % lessonname
                main_ui.add_message_signal.emit(meg,7)
                on_lesson_list.append(lesson_obj)
        
        # for lesson in lesson_list_old:
        #     lessionid = lesson["lesson_id"]
        #     lessonname = lesson["classroom"]["name"]
        #     classroomid = lesson["classroomId"]

        # 可结束线程的计时器
        timer = 0
        while timer <= 30:
            time.sleep(1)
            timer += 1
            if not main_ui.is_active:
                # 由于on_lesson_list在多线程操作之下，此处必须使用列表复制，以保证列表完整性
                for lesson in on_lesson_list.copy():
                    lesson.wsapp.close()
                return