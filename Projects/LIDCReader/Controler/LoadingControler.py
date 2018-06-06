from PyQt5 import QtWidgets
from View.LoadingView import Ui_LoadingView
from PyQt5.QtCore import pyqtSignal, QObject, Qt, pyqtSlot

class LoadingControler(QtWidgets.QWidget, Ui_LoadingView):
    "自定义信号"

    def __init__(self):
        super(LoadingControler, self).__init__()
        self.setupUi(self)
        self.pushButton_Exit.setEnabled(False)  # 禁用退出按钮
        self.progressBar.setValue(0)
        self.Max=0
        # 绑定槽函数
        self.pushButton_Exit.clicked.connect(self.Exit)
    "定义退出按钮的槽函数"
    def Exit(self):
        self.close()
    "定义进度条步进方法"
    def MoveStep(self):
        self.progressBar.setValue(self.progressBar.value()+1)
        if self.progressBar.value()==self.Max:
            self.pushButton_Exit.setEnabled(True)
    "定义向进度条窗口发送消息的方法"
    def SendTest(self,msg):
        self.plainTextEdit_LoadingState.appendPlainText(msg)
    "定义装订进度条方法"
    def SetUpProgressBar(self,max):
        self.Max=max
        self.progressBar.setRange(0, max)  # 确定进度条的上下限
