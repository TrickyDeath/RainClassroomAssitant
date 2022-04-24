from Utils import say_something, dict_result
from GetInfo import SESSIONID,AUTO_DANMU,DANMU_LIMIT,IM_CALLED,UID,UNAME
import requests
import threading
import random
import time
import websocket
import json

wss_url = "wss://www.yuketang.cn/wsapp/"
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
        self.handshark = {"op":"hello","userid":UID,"role":"student","auth":self.auth,"lessonid":self.lessonid}
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
                if UNAME == data["name"]:
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
    
    def start_lesson(self, callback):
        self.auth = self.checkin_class()
        wsapp = websocket.WebSocketApp(url=wss_url,header=self.headers,on_open=self.on_open,on_message=self.on_message)
        wsapp.run_forever()
        meg = "%s监听结束" % self.lessonname
        threading.Thread(target=say_something,args=(meg,)).start()
        return callback(self)
    
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

class Danmu:
    def __init__(self, content):
        self.content = content
        self.time = time.time()

    def __eq__(self, other):
        return (self.content == other.content) and (self.time == other.time)

class User:
    def __init__(self, uid):
        self.uid = uid
        self.time = time.time()
    
    def get_userinfo(self):
        r = requests.get()