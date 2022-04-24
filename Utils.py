import threading
import pyttsx3
import json
import urllib3

lock = threading.Lock()

def say_something(text):
    print(text)
    lock.acquire()
    pyttsx3.speak(text)
    lock.release()
    
def dict_result(text):
    return dict(json.loads(text))

def test_network():
    try:
        http = urllib3.PoolManager()
        http.request('GET', 'https://baidu.com')
        return True
    except:
        return False