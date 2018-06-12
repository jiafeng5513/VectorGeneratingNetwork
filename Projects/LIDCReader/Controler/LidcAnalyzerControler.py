from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, QObject, Qt, pyqtSlot
from View.LidcAnalyzerView import Ui_LidcAnalyzer
from PyQt5.QtWidgets import QFileDialog
from Model.LidcData import LidcData
from Controler.LoadingControler import LoadingControler
import pydicom
import pylab
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as figureCanvas
from Model.TableData import TableData
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QHeaderView

class LidcAnalyzerControler(QtWidgets.QWidget, Ui_LidcAnalyzer):
    TableDataSignal = pyqtSignal(int, int, str)

    def __init__(self):
        super(LidcAnalyzerControler, self).__init__()
        self.setupUi(self)
        # 尝试绘图
        self.figure = pylab.gcf()  # 返回当前的figure
        self.DcmCanvas = figureCanvas(self.figure)
        # 绑定信号槽
        self.pushButton_OpenLidc.clicked.connect(self.OnOpenLidcFolder)
        self.pushButton_ShowROI.clicked.connect(self.OnShowROI)
        self.pushButton_ShowLocus.clicked.connect(self.OnShowLocus)
        self.pushButton_ShowLung.clicked.connect(self.OnShowLung)
        self.pushButton_ShowLabel.clicked.connect(self.OnShowLabel)
        self.pushButton_ExportLabels.clicked.connect(self.OnExportLabel)
        self.pushButton_FrontSeries.clicked.connect(self.OnFrontSeries)
        self.pushButton_BackSeries.clicked.connect(self.OnBackSeries)
        self.pushButton_StartAnalyze.clicked.connect(self.OnAnalyzeStart)
        self.verticalScrollBar.valueChanged.connect(self.OnMoveScrollBar)
        self.gridLayout_ForImg.addWidget(self.DcmCanvas)
        self.verticalScrollBar.setEnabled(False)

        self.TableData = TableData()  # 声明类
        self.Model_Data = QStandardItemModel(4, 4)  # 初始化一个模型QStandardItemModel，4行13列
        self.TableData.TableViewInit(self.tableView, self.Model_Data)  # 调用类TableData中初始化表格函数
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.tableView.verticalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.TableDataSignal.connect(self.TableData.Model_setItem)  # 这里采用信号槽来绑定Model_setItem进行数据更新
        self.TableDataSignal.emit(0, 1, 'sdfsdf')  # 这里为表格添加一个数据，信号发送


    # =======================================================================
        """
        定义主界面上的槽函数
        """
    # 打开Lidc-idri文件夹
    def OnOpenLidcFolder(self):
        dir_path = QFileDialog.getExistingDirectory(self, "choose directory", "F:\\TCIA_LIDC-IDRI\\LIDC-IDRI\\")
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
        self.LidcData.start()  # 后台线程加载数据

    # 初始化主界面上的一切功能
    def OnDataLoadCompleted(self):
        self.plainTextEdit.appendPlainText("数据加载完成,主界面开始交互")
        self.plainTextEdit.appendPlainText("本次分析共找到"+str(len(self.LidcData.SeriesList))+"个series")
        self.CurrentSeriesNum = 0
        self.MaxSeriesNum = len(self.LidcData.SeriesList)-1
        self.CurrentImgNum = 0
        self.MaxImgNum = len(self.LidcData.SeriesList[self.CurrentSeriesNum].DcmFileList)-1
        self.verticalScrollBar.setRange(0,self.MaxImgNum)
        self.verticalScrollBar.setEnabled(True)

        self.ShowDicom()
        self.ShowLabelMsg()
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
        if self.CurrentSeriesNum-1>=0:
            self.CurrentSeriesNum=self.CurrentSeriesNum-1
            self.verticalScrollBar.setEnabled(False)
            self.CurrentImgNum = 0
            self.MaxImgNum = len(self.LidcData.SeriesList[self.CurrentSeriesNum].DcmFileList) - 1
            self.verticalScrollBar.setRange(0, self.MaxImgNum)
            self.verticalScrollBar.setEnabled(True)
            self.ShowDicom()
            self.ShowLabelMsg()
    # 后一个序列
    def OnBackSeries(self):
        print("后一个序列")
        if self.CurrentSeriesNum+1<=self.MaxSeriesNum:
            self.CurrentSeriesNum=self.CurrentSeriesNum+1
            self.verticalScrollBar.setEnabled(False)
            self.CurrentImgNum = 0
            self.MaxImgNum = len(self.LidcData.SeriesList[self.CurrentSeriesNum].DcmFileList) - 1
            self.verticalScrollBar.setRange(0, self.MaxImgNum)
            self.verticalScrollBar.setEnabled(True)
            self.ShowDicom()
            self.ShowLabelMsg()

    # 移动滑动条
    def OnMoveScrollBar(self,value):
        #self.plainTextEdit.appendPlainText(str(self.verticalScrollBar.value()))
        self.CurrentImgNum=self.verticalScrollBar.value()
        self.ShowDicom()
    "显示一张dicom"
    def ShowDicom(self):
        url=self.LidcData.SeriesList[self.CurrentSeriesNum].DcmFileList[self.CurrentImgNum]
        ds = pydicom.read_file(url)
        pixel_bytes = ds.PixelData
        pix = ds.pixel_array
        pylab.imshow(ds.pixel_array, cmap=pylab.cm.bone)
        self.DcmCanvas.draw()
        #pylab.show()

    "显示当前series的标签信息,参数"
    def ShowLabelMsg(self):
        if self.LidcData.SeriesList[self.CurrentSeriesNum].isCTSeries == True:
            self.lineEdit_StudyID.setText(self.LidcData.SeriesList[self.CurrentSeriesNum].XmlObj.StudyInstanceUID)
            seriesID = self.LidcData.SeriesList[self.CurrentSeriesNum].XmlObj.SeriesInstanceUID
            self.lineEdit_SeriesID.setText(seriesID)
            self.plainTextEdit.appendPlainText("from 当前序列的xml"+str(len(self.LidcData.SeriesList[self.CurrentSeriesNum].XmlObj.readingSessionList)))