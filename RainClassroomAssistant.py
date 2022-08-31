import sys
from PyQt5 import QtWidgets
from UI.MainWindow import MainWindow_Ui

if __name__ == "__main__":
    # 初始化
    app = QtWidgets.QApplication(sys.argv)
    main = QtWidgets.QMainWindow()
    ui = MainWindow_Ui()
    ui.setupUi(main)
    main.show()
    # 启动监听
    ui.active()
    # 主窗体循环
    app.exec_()

