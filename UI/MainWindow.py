# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from UI.Login import Login_Ui
from UI.Config import Config_Ui
from Scripts.Utils import *
from Scripts.Monitor import monitor
import os
import json
import datetime
import threading
    
class MainWindow_Ui(QtCore.QObject):
    # 需要建立信号槽，解决无法在线程中修改UI值问题
    add_message_signal = QtCore.pyqtSignal(str,int)
    add_course_signal = QtCore.pyqtSignal(list,int)
    del_course_signal = QtCore.pyqtSignal(int)

    def setupUi(self, MainWindow):
        # 对象变量初始化
        self.table_index = []
        self.is_active = False

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 700)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path("UI\\Image\\favicon.ico")))
        self.Window = QtWidgets.QWidget(MainWindow)
        self.Window.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Window.setObjectName("Window")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.Window)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Menu = QtWidgets.QWidget(self.Window)
        self.Menu.setStyleSheet("background-color: rgb(17, 17, 17);")
        self.Menu.setObjectName("Menu")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.Menu)
        self.horizontalLayout_3.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.Menu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(32, 32))
        self.label.setStyleSheet("border-radius:10px;\n"
"")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(resource_path("UI\\Image\\NoRainClassroom.jpg")))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.Menu)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 16pt \"黑体\";")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.active_btn = QtWidgets.QPushButton(self.Menu)
        self.active_btn.setMaximumSize(QtCore.QSize(100, 400))
        self.active_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.active_btn.setAutoFillBackground(False)
        self.active_btn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.active_btn.setObjectName("active_btn")
        self.horizontalLayout_3.addWidget(self.active_btn)
        self.login_btn = QtWidgets.QPushButton(self.Menu)
        self.login_btn.setMaximumSize(QtCore.QSize(100, 400))
        self.login_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.login_btn.setAutoFillBackground(False)
        self.login_btn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.login_btn.setObjectName("login_btn")
        self.horizontalLayout_3.addWidget(self.login_btn)
        self.config_btn = QtWidgets.QPushButton(self.Menu)
        self.config_btn.setMaximumSize(QtCore.QSize(100, 400))
        self.config_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.config_btn.setAutoFillBackground(False)
        self.config_btn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.config_btn.setObjectName("config_btn")
        self.horizontalLayout_3.addWidget(self.config_btn)
        self.horizontalLayout_3.setStretch(2, 1)
        self.horizontalLayout_3.setStretch(3, 1)
        self.horizontalLayout_3.setStretch(4, 1)
        self.horizontalLayout_3.setStretch(5, 1)
        self.verticalLayout.addWidget(self.Menu)
        self.Table = QtWidgets.QGroupBox(self.Window)
        self.Table.setStyleSheet("color: rgb(209, 209, 209);\n"
"font: 10pt \"微软雅黑\";\n"
"color: rgb(0, 0, 0);")
        self.Table.setObjectName("Table")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.Table)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tableWidget = QtWidgets.QTableWidget(self.Table)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setStyleSheet("font: 9pt \"微软雅黑\";")
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.verticalLayout_3.addWidget(self.tableWidget)
        self.verticalLayout.addWidget(self.Table)
        self.Output = QtWidgets.QGroupBox(self.Window)
        self.Output.setStyleSheet("color: rgb(209, 209, 209);\n"
"font: 10pt \"微软雅黑\";\n"
"color: rgb(0, 0, 0);")
        self.Output.setObjectName("Output")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Output)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.output_textarea = QtWidgets.QTextBrowser(self.Output)
        self.output_textarea.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(255, 255, 255);\n"
"font: 9pt \"微软雅黑\";")
        self.output_textarea.setObjectName("output_textarea")
        self.verticalLayout_2.addWidget(self.output_textarea)
        self.verticalLayout.addWidget(self.Output)
        MainWindow.setCentralWidget(self.Window)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 按钮事件绑定
        self.config_btn.clicked.connect(self.show_config)
        self.login_btn.clicked.connect(self.show_login)
        self.active_btn.clicked.connect(self.active_clicked)

        # 绑定信号槽
        self.add_message_signal.connect(self.add_message)
        self.add_course_signal.connect(self.add_course)
        self.del_course_signal.connect(self.del_course)

        # 配置文件检查
        dir_route = get_config_dir()
        config_route = get_config_path()
        self.config = self.check_config(dir_route, config_route)

        self.add_message_signal.emit("当前版本：v0.0.4",0)
        self.add_message_signal.emit("初始化完成",0)

        # 登录状态检查
        status, user_info = self.check_login()
        if status:
            self.login_btn.setText("重新登录")
            self.add_message_signal.emit("登录成功，当前登录用户："+user_info["name"],0)
        else:
            self.show_login()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "摸鱼课堂"))
        self.label_2.setText(_translate("MainWindow", "摸鱼课堂"))
        self.active_btn.setText(_translate("MainWindow", "启用"))
        self.login_btn.setText(_translate("MainWindow", "登录"))
        self.config_btn.setText(_translate("MainWindow", "配置"))
        self.Table.setTitle(_translate("MainWindow", "监听列表"))
        self.Output.setTitle(_translate("MainWindow", "信息"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "课程名"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "课程标题"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "教师"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "上课时间"))
        self.Output.setTitle(_translate("MainWindow", "信息"))

    def add_course(self, row, row_count):
        # 添加课程
        # 注意：在非UI运行线程中调用该方法请对add_course_signal发送信号
        self.tableWidget.insertRow(row_count)
        # 装填当前行各列数据
        for i in range(len(row)):
            content = QtWidgets.QTableWidgetItem(str(row[i]))
            self.tableWidget.setItem(row_count,i,content)

        # 存储各行PersistentModelIndex，便于后续删除操作
        model_index = self.tableWidget.indexFromItem(content)
        per_model_index = QtCore.QPersistentModelIndex(model_index)
        self.table_index.append((row_count,per_model_index))

    def del_course(self, index):
        # 删除课程
        # 注意：在非UI运行线程中调用该方法请对del_course_signal发送信号
        for row_count,per_model_index in self.table_index:
            # 搜索传入index所对应的QPersistentModelIndex，并进行删除
            # QPersistentModelIndex对象的索引在删除过程中不会被已删除元素影响
            if row_count == index:
                self.tableWidget.removeRow(per_model_index.row())
                self.table_index.remove((row_count,per_model_index))

    def show_config(self):
        # 展示配置对话框
        dialog = QtWidgets.QDialog()
        config_ui = Config_Ui()
        config_ui.setupUi(dialog)
        # 加载配置文件
        config_ui.load_config(self.config)
        # 这里需要刷新一次自定义延迟部分的Widget
        config_ui.enable_delay_custom()
        if dialog.exec_():
            config_route = get_config_path()
            with open(config_route,"r") as f:
                self.config = json.load(f)

    def show_login(self, _bool=False, rtn_message=""):
        # 展示登录对话框
        # rtn_message用于展示上次扫码登录失败的信息
        dialog = QtWidgets.QDialog()
        login_ui = Login_Ui()
        login_ui.setupUi(dialog)
        # 加载配置文件，主要用于加载sessionid
        login_ui.load_config(self.config)

        # 将最下方登录返回值栏设置rtn_message
        login_ui.login_return.setText(rtn_message)

        # 登录成功返回1，其他情况返回0
        success = dialog.exec_()
        if success:
            config_route = get_config_path()
            with open(config_route,"r") as f:
                self.config =  json.load(f)
        # 删除涉及登录的线程
        login_ui.close_all()
        # 再次检测登录状态
        status, user_info = self.check_login()
        if status and success:
            self.add_message_signal.emit("登录成功，当前登录用户："+user_info["name"],0)
            self.login_btn.setText("重新登录")
        if not status:
            self.show_login(rtn_message="登录失败，请重新登录")
        
    def check_config(self, dir_route, config_route):
        # 检查配置文件
        # 检查目录是否存在
        if not os.path.exists(dir_route):
            os.makedirs(dir_route)
        # 检查配置文件存在性及可用性
        if not os.path.exists(config_route):
            initial_data = get_initial_data()
            f = open(config_route,"w+")
            json.dump(initial_data,f)
            f.close()
            self.add_message_signal.emit("没有检测到配置文件，已自动创建",0)
            return initial_data
        else:
            try:
                with open(config_route,"r") as f:
                    data = json.load(f)
                    self.add_message_signal.emit("配置文件已读取",0)
                    return data
            except:
                with open(config_route,"w+") as f:
                    initial_data = get_initial_data()
                    json.dump(initial_data,f)
                    self.add_message_signal.emit("配置文件读取失败，已重新生成",0)
                    return initial_data

    def check_login(self):
        # 检查登录状态
        code, user_info = get_user_info(self.config["sessionid"])
        if code == 50000:
            return False,user_info
        elif code == 0:
            return True,user_info
            
    def add_message(self, message, type=0):
        # 新增输出信息，并尝试语音播报
        time = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        self.output_textarea.append(time + message)
        if not type == 0:
            self.audio(message,type)

    def active_clicked(self):
        # 启动按钮被点击
        if self.is_active:
            self.deactive()
        else:
            self.active()

    def active(self):
        # 启动
        self.monitor_t = threading.Thread(target=monitor,args=(self,),daemon=True)
        self.monitor_t.start()
        self.is_active = True
        self.active_btn.setText("停止监听")
        self.add_message_signal.emit("启动成功",0)
    
    def deactive(self):
        # 停止
        self.active_btn.setText("停止中...")
        self.active_btn.setEnabled(False)
        # 强制刷新UI
        QtWidgets.qApp.processEvents()
        self.is_active = False
        self.monitor_t.join()
        self.active_btn.setEnabled(True)
        self.active_btn.setText("启动")
        self.add_message_signal.emit("停止成功",0)

    def audio(self, message, type):
        '''
        type
        0: 默认，未分类音频
        1: 自动发送弹幕成功
        2: 他人弹幕发送
        3: 收到题目
        4: 自动答题情况
        5: 自己被点名
        6: 他人被点名
        7: 课程相关
        8: 网络断开/重连
        '''
        # 尝试播放语音提示
        audio_on = self.config["audio_on"]
        if audio_on:
            audio_type = self.config["audio_config"]["audio_type"]
            if \
            (type == 1 and audio_type["send_danmu"]) or \
            (type == 2 and audio_type["others_danmu"]) or \
            (type == 3 and audio_type["receive_problem"]) or \
            (type == 4 and audio_type["answer_result"]) or \
            (type == 5 and audio_type["im_called"]) or \
            (type == 6 and audio_type["others_called"]) or \
            (type == 7 and audio_type["course_info"]) or \
            (type == 8 and audio_type["network_info"]) :
                threading.Thread(target=say_something,args=(message,),daemon=True).start()