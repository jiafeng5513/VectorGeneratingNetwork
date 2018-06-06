from PyQt5 import QtCore, QtGui, QtWidgets
from View.LidcAnalyzerView import Ui_LidcAnalyzer
from PyQt5.QtWidgets import QFileDialog
from Model.LidcData import LidcData
from Controler.LoadingControler import LoadingControler
import time

class LidcAnalyzerControler(QtWidgets.QWidget, Ui_LidcAnalyzer):
    def __init__(self):
        super(LidcAnalyzerControler, self).__init__()
        self.setupUi(self)
        #绑定信号槽
        self.pushButton_OpenLidc.clicked.connect(self.OnOpenLidcFolder)
        self.pushButton_ShowROI.clicked.connect(self.OnShowROI)
        self.pushButton_ShowLocus.clicked.connect(self.OnShowLocus)
        self.pushButton_ShowLung.clicked.connect(self.OnShowLung)
        self.pushButton_ShowLabel.clicked.connect(self.OnShowLabel)
        self.pushButton_ExportLabels.clicked.connect(self.OnExportLabel)
        self.pushButton_FrontSeries.clicked.connect(self.OnFrontSeries)
        self.pushButton_BackSeries.clicked.connect(self.OnBackSeries)
        self.pushButton_StartAnalyze.clicked.connect(self.OnAnalyzeStart)
    #=======================================================================
        """
        定义主界面上的槽函数
        """
    # 打开Lidc-idri文件夹
    def OnOpenLidcFolder(self):
        dir_path = QFileDialog.getExistingDirectory(self, "choose directory", "../")
        self.lineEdit_LidcRootDir.setText(dir_path)
    def OnAnalyzeStart(self):
        print("开始分析")
        self.LidcData = LidcData()
        self.LidcData.init(self.lineEdit_LidcRootDir.text())
        self.progressWidget = LoadingControler()
        self.LidcData.SetUpProgressBarSignal.connect(self.progressWidget.SetUpProgressBar)
        self.LidcData.MoveSignal.connect(self.progressWidget.MoveStep)
        self.LidcData.SendTextSignal.connect(self.progressWidget.SendTest)
        self.LidcData.AllCompletedSignal.connect(self.OnDataLoadCompleted)
        self.progressWidget.show()
        self.LidcData.start()

    # 初始化主界面上的一切功能
    def OnDataLoadCompleted(self):
        print("数据加载完成,主界面开始交互")
        self.plainTextEdit.appendPlainText("数据加载完成,主界面开始交互")
    # 显示ROI
    def OnShowROI(self):
        print("显示ROi")
    # 显示locus
    def OnShowLocus(self):
        print("显示Locus")
    # 启动肺实质分割
    def OnShowLung(self):
        print("启动肺实质分割")
    # 生成标注图
    def OnShowLabel(self):
        print("生成标注图")
    # 导出当前series的全部标注图
    def OnExportLabel(self):
        print("导出标注")
    # 前一个序列
    def OnFrontSeries(self):
        print("前一个序列")
    # 后一个序列
    def OnBackSeries(self):
        print("后一个序列")