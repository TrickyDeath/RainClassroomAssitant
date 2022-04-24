import websocket
import json
import requests
import random
import pyttsx3
import threading
import time
import urllib3

# 你的雨课堂sessionid
SESSIONID = ""
# 是否开启自动弹幕发送
AUTO_DANMU = True
# 自动弹幕发送阈值（当同一条弹幕被接收到DANMU_LIMIT次时，将自动发送该弹幕）
DANMU_LIMIT = 10
# 点名只有点到你时才有语音提醒（否则只要有点名都会有语音提醒）
IM_CALLED = False

def dict_result(text):
    return dict(json.loads(text))

def get_user_info():
    r = requests.get(url="https://www.yuketang.cn/api/v3/user/basic-info",headers=headers)
    return dict_result(r.text)["data"]

def say_something(text):
    print(text)
    lock.acquire()
    pyttsx3.speak(text)
    lock.release()

def get_on_lesson():
    r = requests.get("https://www.yuketang.cn/api/v3/classroom/on-lesson",headers=headers)
    return dict_result(r.text)["data"]["onLessonClassrooms"]

class Lesson:
    def __init__(self,lessonid,lessonname):
        self.lessonid = lessonid
        self.lessonname = lessonname
        self.headers = {
            "Cookie":"sessionid=%s" % SESSIONID,
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
        }
        self.receive_danmu = {}
        self.sent_damu = []
        self.danmu_list = []
        self.danmu_dict = {}
        self.problems_ls = []
        self.unlocked_problem = []
    
    def _get_ppt(self,presentationid):
        r = requests.get(url="https://www.yuketang.cn/api/v3/lesson/presentation/fetch?presentation_id=%s" % (presentationid),headers=self.headers)
        return dict_result(r.text)["data"]

    def get_problems(self,presentationid):
        data = self._get_ppt(presentationid)
        return [problem["problem"] for problem in data["slides"] if "problem" in problem.keys()]

    def answer_questions(self,problemid,problemtype,answer,limit):
        if answer and problemtype != 3:
            if limit == -1:
                wait_time = random.randint(5,20)
            else:
                if limit > 15:
                    wait_time = random.randint(5,limit-10)
                else:
                    wait_time = 0
            if wait_time != 0:
                meg = "%s检测到问题，将在%s秒后自动回答，答案为%s" % (self.lessonname,wait_time,answer)
                threading.Thread(target=say_something,args=(meg,)).start()
                time.sleep(wait_time)
            else:
                meg = "%s检测到问题，剩余时间小于15秒，将立即自动回答，答案为%s" % (self.lessonname,wait_time,answer)
                threading.Thread(target=say_something,args=(meg,)).start()
            data = {"problemId":problemid,"problemType":problemtype,"dt":int(time.time()),"result":answer}
            r = requests.post(url="https://www.yuketang.cn/api/v3/lesson/problem/answer",headers=self.headers,data=json.dumps(data))
            return_dict = dict_result(r.text)
            if return_dict["code"] == 0:
                meg = "%s自动回答成功" % self.lessonname
                threading.Thread(target=say_something,args=(meg,)).start()
                return True
            else:
                meg = "%s自动回答失败，原因：%s" % (self.lessonname,return_dict["msg"].replace("_"," "))
                threading.Thread(target=say_something,args=(meg,)).start()
                return False
        else:
            meg = "%s的问题没有找到答案，请在%s秒内前往雨课堂回答" % (self.lessonname,limit)
            threading.Thread(target=say_something,args=(meg,)).start()
            return False
    
    def on_open(self, wsapp):
        self.handshark = {"op":"hello","userid":uid,"role":"student","auth":self.auth,"lessonid":self.lessonid}
        wsapp.send(json.dumps(self.handshark))

    def checkin_class(self):
        r = requests.post(url="https://www.yuketang.cn/api/v3/lesson/checkin",headers=self.headers,data=json.dumps({"source":5,"lessonId":self.lessonid}))
        set_auth = r.headers.get("Set-Auth",None)
        times = 1
        while not set_auth and times <= 3:
            set_auth = r.headers.get("Set-Auth",None)
            times += 1
            time.sleep(1)
        self.headers["Authorization"] = "Bearer %s" % set_auth
        return dict_result(r.text)["data"]["lessonToken"]

    def on_message(self, wsapp, message):
        data = dict_result(message)
        op = data["op"]
        if op == "hello":
            presentations = list(set([slide["pres"] for slide in data["timeline"] if slide["type"]=="slide"]))
            current_presentation = data["presentation"]
            if current_presentation not in presentations:
                presentations.append(current_presentation)
            for presentationid in presentations:
                self.problems_ls.extend(self.get_problems(presentationid))
            self.unlocked_problem = data["unlockedproblem"]
            for promblemid in self.unlocked_problem:
                self._current_problem(wsapp, promblemid)
        elif op == "unlockproblem":
            self.start_answer(data["problem"]["sid"],data["problem"]["limit"])
        elif op == "lessonfinished":
            meg = "%s下课了" % self.lessonname
            threading.Thread(target=say_something,args=(meg,)).start()
            wsapp.close()
        elif op == "presentationupdated":
            self.problems_ls.extend(self.get_problems(data["presentation"]))
        elif op == "presentationcreated":
            self.problems_ls.extend(self.get_problems(data["presentation"]))
        elif op == "newdanmu" and AUTO_DANMU:
            # try:
            #     self.danmu_dict[data["danmu"].lower()].append(time.time())
            # except KeyError:
            #     self.danmu_dict[data["danmu"].lower()] = [time.time()]
            
            # for content in self.danmu_dict.keys():
            #     for j in self.danmu_dict[content].values():
            #         if time.time() - j > 60:
            #             self.danmu_dict[content].remove(j)
            #     count = len(self.danmu_dict[content])
            #     if content not in self.sent_damu:
            #         if count >= DANMU_LIMIT:
            #             self.send_danmu(content)
            #             self.sent_damu.append(Danmu)
            #     else:
            # print("%()" % user_dict[])
            danmu_obj = Danmu(data["danmu"].lower())
            self.danmu_list.append(danmu_obj)
            for i in self.sent_damu:
                if time.time() - i.time > 60:
                    self.sent_damu.remove(i)
            sent_content_ls = [j.content for j in self.sent_damu]
            for i in self.danmu_list:
                if time.time() - i.time > 60:
                    self.danmu_list.remove(i)
                else:
                    if i.content in list(self.danmu_dict.keys()):
                        self.danmu_dict[i.content] += 1
                    else:
                        self.danmu_dict[i.content] = 1
                    if i.content in sent_content_ls:
                        self.danmu_dict[i.content] = 1
            for i in self.sent_damu:
                if time.time() - i.time > 60:
                    self.sent_damu.remove(i)
            for content in self.danmu_dict.keys():
                if self.danmu_dict[content] >= DANMU_LIMIT and content not in sent_content_ls:
                    self.send_danmu(content)
                    self.sent_damu.append(Danmu(content))
        elif op == "callpaused":
            meg = "%s点名了，点到了：%s" % (self.lessonname, data["name"])
            if IM_CALLED:
                if uname == data["name"]:
                    threading.Thread(target=say_something,args=(meg,)).start()
                else:
                    print(meg)
            else:
                threading.Thread(target=say_something,args=(meg,)).start()
        elif op == "probleminfo":
            if data["limit"] != -1:
                time_left = int(data["limit"]-(int(data["now"]) - int(data["dt"]))/1000)
            else:
                time_left = data["limit"]
            if time_left > 0 or time_left == -1:
                self.start_answer(data["problemid"],time_left)
    
    def start_answer(self, promblemid, limit):
        for promble in self.problems_ls:
            if promble["problemId"] == promblemid:
                threading.Thread(target=self.answer_questions,args=(promble["problemId"],promble["problemType"],promble.get("answers",[]),limit)).start()
                break
        else:
            meg = "%s的问题没有找到答案，请在%s秒内前往雨课堂回答" % (self.lessonname,limit)
            threading.Thread(target=say_something,args=(meg,)).start()

    def _current_problem(self, wsapp, promblemid):
        query_problem = {"op":"probleminfo","lessonid":self.lessonid,"problemid":promblemid,"msgid":1}
        wsapp.send(json.dumps(query_problem))
    
    def start_lesson(self):
        self.auth = self.checkin_class()
        wsapp = websocket.WebSocketApp(url=wss_url,header=self.headers,on_open=self.on_open,on_message=self.on_message)
        wsapp.run_forever()
        meg = "%s监听结束" % self.lessonname
        threading.Thread(target=say_something,args=(meg,)).start()
        on_lesson_list.remove(self)
    
    def send_danmu(self,content):
        url = "https://www.yuketang.cn/api/v3/lesson/danmu/send"
        data = {
            "extra": "",
            "fromStart": "50",
            "lessonId": self.lessonid,
            "message": content,
            "requiredCensor": False,
            "showStatus": True,
            "target": "",
            "userName": "",
            "wordCloud": True
        }
        r = requests.post(url=url,headers=self.headers,data=json.dumps(data))
        if dict_result(r.text)["code"] == 0:
            print("%s弹幕发送成功！内容：%s" % (self.lessonname,content))
        else:
            print("%s弹幕发送失败！内容：%s" % (self.lessonname,content))
    
    def __eq__(self, other):
        return self.lessonid == other.lessonid

class User:
    def __init__(self, uid):
        self.uid = uid
        self.time = time.time()
    
    def get_userinfo(self):
        r = requests.get()
    
class Danmu:
    def __init__(self, content):
        self.content = content
        self.time = time.time()

    def __eq__(self, other):
        return (self.content == other.content) and (self.time == other.time)
    
def test_network():
    try:
        http = urllib3.PoolManager()
        http.request('GET', 'https://baidu.com')
        return True
    except:
        return False

if __name__ == "__main__":
    wss_url = "wss://www.yuketang.cn/wsapp/"
    headers = {
        "Cookie":"sessionid=%s" % SESSIONID,
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    }
    lock = threading.Lock()
    problems_ls = []
    on_lesson_list = []
    lesson_list = []
    user_dict = {}
    user_info = get_user_info()
    uid = user_info["id"]
    uname = user_info["name"]
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
                thread = threading.Thread(target=lesson_obj.start_lesson)
                thread.start()
                meg = "检测到课程%s正在上课，已加入自动提醒列表" % lessonname
                threading.Thread(target=say_something,args=(meg,)).start()
                on_lesson_list.append(lesson_obj)
        time.sleep(30)
