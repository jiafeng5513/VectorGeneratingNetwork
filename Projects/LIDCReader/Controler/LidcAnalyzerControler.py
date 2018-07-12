from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, QObject, Qt, pyqtSlot
from View.LidcAnalyzerView import Ui_LidcAnalyzer
from PyQt5.QtWidgets import QFileDialog
from Model.LidcData import LidcData
from Controler.LoadingControler import LoadingControler
import pydicom
import pylab
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as figureCanvas
import matplotlib.pyplot as plt
from Model.TableData import TableData
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QHeaderView
from utils import MaskGenerator


class LidcAnalyzerControler(QtWidgets.QWidget, Ui_LidcAnalyzer):
    TableDataSignal = pyqtSignal(int, int, str)
    TableDataCleanSignal = pyqtSignal()

    def __init__(self):
        super(LidcAnalyzerControler, self).__init__()
        self.setupUi(self)
        # 绘图
        self.DcmFigure = plt.figure(1)
        plt.title('Dcm Img')
        self.MaskFigure = plt.figure(2)
        plt.title('Mask Img')
        self.DcmCanvas = figureCanvas(self.DcmFigure)
        self.MaskCanvas = figureCanvas(self.MaskFigure)
        self.gridLayout_ForImg.addWidget(self.DcmCanvas)
        self.gridLayout_ForMask.addWidget(self.MaskCanvas)
        # 绑定信号槽
        self.pushButton_OpenLidc.clicked.connect(self.OnOpenLidcFolder)
        self.pushButton_ExportLabels.clicked.connect(self.OnExportLabel)
        self.pushButton_FrontSeries.clicked.connect(self.OnFrontSeries)
        self.pushButton_BackSeries.clicked.connect(self.OnBackSeries)
        self.pushButton_StartAnalyze.clicked.connect(self.OnAnalyzeStart)
        self.SliceScrollBar.valueChanged.connect(self.OnMoveScrollBar)
        self.SliceScrollBar.setEnabled(False)

        self.TableData = TableData()  # 声明类
        self.Model_Data = QStandardItemModel(4, 4)  # 初始化一个模型QStandardItemModel，4行13列
        self.TableData.TableViewInit(self.tableView, self.Model_Data)  # 调用类TableData中初始化表格函数
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.tableView.verticalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.TableDataSignal.connect(self.TableData.Model_setItem)  # 这里采用信号槽来绑定Model_setItem进行数据更新
        self.TableDataCleanSignal.connect(self.TableData.Model_clearnItem)
        self.radioButton_ShowLung.clicked.connect(self.OnClickedRadioButton_ShowLung)
        self.radioButton_ShowColorLabel.clicked.connect(self.OnClickedRadioButton_ShowColorLabel)
        self.checkBox_CtOnly.clicked.connect(self.OnClickedCheckBox_CtOnly)
        # 初始化
        self.radioButton_ShowLung.setChecked(True)
        self.radioButton_ShowColorLabel.setChecked(False)
        self.checkBox_CtOnly.setChecked(True)

    # =======================================================================
        """
        定义主界面上的槽函数
        """
    # 打开Lidc-idri文件夹
    def OnOpenLidcFolder(self):
        self.checkBox_CtOnly.setEnabled(True)
        dir_path = QFileDialog.getExistingDirectory(self, "choose directory", "F:\\TCIA_LIDC-IDRI\\LIDC-IDRI\\")
        self.lineEdit_LidcRootDir.setText(dir_path)

    # 开始分析
    def OnAnalyzeStart(self):
        print("开始分析")
        # 一旦开始分析,就不能再更改CtOnly的状态,除非重新选择目录
        self.checkBox_CtOnly.setEnabled(False)
        self.LidcData = LidcData(isCtOnly=self.checkBox_CtOnly.isChecked())
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
        self.SliceScrollBar.setRange(0,self.MaxImgNum)
        self.SliceScrollBar.setEnabled(True)

        self.ShowDicom()
        self.ShowLabelMsg()

    # 点选"显示肺实质分割结果"RadioButton
    def OnClickedRadioButton_ShowLung(self,checked):
        self.ShowDicom()

    # 点选"显示语义分割标签图"RadioButton
    def OnClickedRadioButton_ShowColorLabel(self,checked):
        self.ShowDicom()

    # 改变"忽略非CT标签"CheckBox的状态(默认选中)
    def OnClickedCheckBox_CtOnly(self,checked):
        print(str(checked))

    # 导出当前series的全部标注图
    def OnExportLabel(self):
        print("导出标注")

    # 前一个序列
    def OnFrontSeries(self):
        print("前一个序列")
        if self.CurrentSeriesNum-1>=0:
            self.CurrentSeriesNum=self.CurrentSeriesNum-1
            self.SliceScrollBar.setEnabled(False)
            self.CurrentImgNum = 0
            self.MaxImgNum = len(self.LidcData.SeriesList[self.CurrentSeriesNum].DcmFileList) - 1
            self.SliceScrollBar.setRange(0, self.MaxImgNum)
            self.SliceScrollBar.setEnabled(True)
            self.ShowDicom()
            self.ShowLabelMsg()

    # 后一个序列
    def OnBackSeries(self):
        print("后一个序列")
        if self.CurrentSeriesNum+1<=self.MaxSeriesNum:
            self.CurrentSeriesNum=self.CurrentSeriesNum+1
            self.SliceScrollBar.setEnabled(False)
            self.CurrentImgNum = 0
            self.MaxImgNum = len(self.LidcData.SeriesList[self.CurrentSeriesNum].DcmFileList) - 1
            self.SliceScrollBar.setRange(0, self.MaxImgNum)
            self.SliceScrollBar.setEnabled(True)
            self.ShowDicom()
            self.ShowLabelMsg()

    # 移动滑动条
    def OnMoveScrollBar(self,value):
        self.CurrentImgNum=self.SliceScrollBar.value()
        self.ShowDicom()

    "显示一张dicom"
    def ShowDicom(self):
        url=self.LidcData.SeriesList[self.CurrentSeriesNum].DcmFileList[self.CurrentImgNum]
        ds = pydicom.read_file(url)
        pixel_bytes = ds.PixelData
        pix = ds.pixel_array

        ax = self.DcmFigure.add_subplot(111)
        ax.imshow(ds.pixel_array,cmap=pylab.cm.bone)  # 原图

        lungImg,labelimg = MaskGenerator.GenerateLabel(ds.pixel_array)  # 生成图
        ax2 = self.MaskFigure.add_subplot(111)
        if self.radioButton_ShowLung.isChecked() is True:
            ax2.imshow(lungImg, cmap=pylab.cm.bone)
        else:
            ax2.imshow(labelimg, cmap=pylab.cm.bone)

        self.DcmCanvas.draw()
        self.MaskCanvas.draw()

    "显示当前series的标签信息,参数"
    def ShowLabelMsg(self):
        self.TableDataCleanSignal.emit()
        self.lineEdit_StudyID.setText("")
        self.lineEdit_SeriesID.setText("")
        """
        如果是CT序列:
            直接找XmlObj,
        """
        if self.LidcData.SeriesList[self.CurrentSeriesNum].isCTSeries == True:
            self.lineEdit_StudyID.setText(self.LidcData.SeriesList[self.CurrentSeriesNum].XmlObj.StudyInstanceUID)
            seriesID = self.LidcData.SeriesList[self.CurrentSeriesNum].XmlObj.SeriesInstanceUID
            self.lineEdit_SeriesID.setText(seriesID)
            self.plainTextEdit.appendPlainText("from 当前序列的xml"+str(len(self.LidcData.SeriesList[self.CurrentSeriesNum].XmlObj.readingSessionList)))
            i = 0
            for readingSession in self.LidcData.SeriesList[self.CurrentSeriesNum].XmlObj.readingSessionList:
                self.TableDataSignal.emit(0, i, readingSession.ID)  # 这里为表格添加一个数据，信号发送
                self.TableDataSignal.emit(1, i, str(len(readingSession.NoduleList)))
                k = 0
                for Nodule in readingSession.NoduleList:
                    if Nodule.LargerThan3mm == True:
                        k+=1
                self.TableDataSignal.emit(2, i, str(k))
                self.TableDataSignal.emit(3, i, str(len(readingSession.nonNoduleList)))
                i+=1
        elif self.LidcData.SeriesList[self.CurrentSeriesNum].XmlFilePath!="":
            # 不是CT序列,但是具有xml文件
            self.lineEdit_StudyID.setText(self.LidcData.SeriesList[self.CurrentSeriesNum].XmlObj.StudyInstanceUID)
            seriesID = self.LidcData.SeriesList[self.CurrentSeriesNum].XmlObj.SeriesInstanceUID
            self.lineEdit_SeriesID.setText(seriesID)
