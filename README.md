# RainClassroomAssitant
基于Python的雨课堂小助手。
## 介绍
疫情期间，网课成为了当前重要的教学方式。这种方式在疫情期间为诸位都提供了极大的便利。但是，不免有些线上水课，这些水课老师不仅仅讲的内容枯燥无聊，照着PPT读，还要整出一系列的活来提升听课率，例如：课堂中途偷袭式发题、点名，将弹幕回答问题记录作为考察平时成绩的依据等。为了解决线上“水课”不能安心划水的问题，雨课堂小助手应运而生。
## 已实现功能
 - 自动签到
 - 自动答题（仅限于上课过程中发布的选择题、多选题、填空题）
 - 自动发弹幕（一定时间内收到一定数量的弹幕后，自动跟风发送相同内容的弹幕）
 - 点名、收到题目语音提醒
 - 多线程支持（此脚本支持在有多个正在上课课程的情况下使用）
## 待做功能
- [ ] 自动预习
## 使用方法
### 获取sessionid
1. 登录雨课堂网页版
2. 点击F12，打开网页调试器，找到存储（Storage），并找到sessionid，圈的部分就是你sessionid的值，如下图：
![网页调试器](/help_pic/sessionid.png)
### 使用程序
1. 下载release的[RainClassroomAssistant.exe](https://github.com/TrickyDeath/RainClassroomAssitant/releases/tag/v0.0.1)，并点击运行，
2. 首次运行会生成一个config.json在同目录下，需要打开config.json设置你的sessionid，例如你的sessionid为123456，则如下填写
'''
{"sessionid": "123456","auto_danmu": true,"danmu_limit": 10,"im_called": false}
'''
你可以自行修改一些配置，config.json中：
'''
auto_danmu为自动发送弹幕开关，true为开，false为关
danmu_limit为自动发送弹幕的阈值，在60秒内收到danmu_limit次同样内容的弹幕后，将会自动发送该条弹幕
im_called为点名语音提醒配置，true为仅自己被点到时才会语音提醒，false为只要老师点名就会语音提醒
'''
3. 之后只需要运行RainClassroomAssistant.exe，即可开始监听
注：
只要你不点击退出登录，sessionid很长时间才会过期，如果sessionid失效，重新[获取sessionid](#获取sessionid)即可
当然也可以直接下载源代码，并安装requirement.txt中的第三方库，直接使用Python运行