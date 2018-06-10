"""
Model for Lidc-idri
描述LIdc-Idri数据集的组织结构
为了尽量简化流程提高效率,我做如下规定:
    1.LIDC-IDRI父目录下,应当存放名字形如LIDC-IDRI-XXXX的Patient文件夹若干
    2.LIDC-IDRI父目录下,应当存放有LIDC-IDRI_MetaData.csv
    3.每个Patient目录下,应当存放有一个或者两个Study文件夹,以Study UID 命名
    4.每个Study目录下,应当有唯一一个series文件夹,以Series UID命名
    5.每个Series文件夹下,应当存放一系列DCM文件和一个xml文件

为了能实现监控加载流程,要这么做:
    1.将加载过程写成一个线程
    2.在这里定义三个关键信号,并在需要的时候发信号
    3.在AnalyzerControler中相应的位置,先构造本类对象和Loading界面的controler,
    4.在现场连接信号槽.
    5.启动线程
"""
import os
import pydicom
from PyQt5.QtCore import pyqtSignal, QThread, QObject, Qt, pyqtSlot
from PyQt5.QtWidgets import QApplication
import sys
from Model.XmlData import XmlLabelForCT, XmlLabelSlim

"描述LidcSeries"


class LidcSeries(object):
    "构造函数"

    def __init__(self, patientAbsPath, studyName, seriesName):
        self.SeriesID = seriesName
        self.SeriesAbsPath = '%s\\%s\\%s' % (patientAbsPath, studyName, seriesName)
        self.isCTSeries = False  # 当前序列是否是CT序列,只有CT序列需要进行解刨学排序和xml解析
        # 找到series路径下的全部文件,把DCM文件和xml文件的绝对路径分别存储
        self.DcmFileList = []
        # 先检查是否存在DcmList.txt,如果存在,从txt中直接取出xml文件和排好序的dcm文件列表
        if os.path.exists(self.SeriesAbsPath + "\\DcmList.txt"):
            # 找到了当前series的排序缓存文件
            print("找到排序缓存,跳过文件排序")
            SortFile = open(self.SeriesAbsPath + "\\DcmList.txt", 'r')
            lines = SortFile.readlines()  # 读取全部内容
            self.XmlFilePath = lines[0].replace('\n', '')  # 已经取出xml文件
            for i in range(1, len(lines)):  # 读取排好序的dcm列表
                self.DcmFileList.append(lines[i].replace('\n', ''))
            if pydicom.read_file(self.DcmFileList[0]).Modality == "CT":  # 识别是否为CT序列
                self.isCTSeries = True
                self.XmlObj = XmlLabelForCT(self.XmlFilePath)
            else:
                self.isCTSeries = False
                self.XmlObj = XmlLabelSlim(self.XmlFilePath)
        else:
            # 没找到当前series的排序缓存文件
            itemNames = os.listdir(self.SeriesAbsPath)  # 获取该目录下的所有文件

            for itemName in itemNames:
                itemAbsPath = os.path.join(self.SeriesAbsPath, itemName)  # 获取每个item的绝对路径
                if "dcm" in itemName:  # 发现dcm文件
                    self.DcmFileList.append(itemAbsPath)
                elif "xml" in itemName:  # 发现xml标签文件
                    self.XmlFilePath = itemAbsPath
            # 把dcm文件的绝对路径按照解刨学顺序排列,并创建排序缓存文件
            self.SortDcmListBySliceLocation(self.DcmFileList)

    "为DcmList按照SliceLocation排序"

    def SortDcmListBySliceLocation(self, dcmlist):
        if self.isCTSeries == False:  # 只有CT序列需要排序
            return dcmlist
        else:
            # 先询问有没有排序文件,如果有,直接加载,如果没有,现场排序并生成排序文件
            print("按照SliceLocation字段对dcm文件列表进行排序,待排序列表长度为:" + str(len(dcmlist)))
            flag = 1
            for index in range(len(dcmlist) - 1, 0, -1):
                if flag:
                    flag = 0
                    for two_index in range(index):
                        ds1 = pydicom.read_file(dcmlist[two_index]).SliceLocation
                        ds2 = pydicom.read_file(dcmlist[two_index + 1]).SliceLocation
                        if ds1 < ds2:  # 排序依据是SliceLocation从大到小(基本全是负数)
                            dcmlist[two_index], dcmlist[two_index + 1] = dcmlist[two_index + 1], dcmlist[two_index]
                            flag = 1
                else:
                    break
            # 在此处保存排序文件
            SortFile = open(self.SeriesAbsPath + "\\DcmList.txt", 'w')
            SortFile.writelines(self.XmlFilePath + "\n")  # 先写入xml的路径
            for word in dcmlist:  # 按照解破学顺序把dcm文件路径依次写入txt
                SortFile.writelines(word + "\n")
            SortFile.close()
            return dcmlist


"====================================================================================================="

"""
描述Lidi数据集
实现一个Qt线程用来进行后台数据的加载
"""


class LidcData(QThread):
    MoveSignal = pyqtSignal()
    SendTextSignal = pyqtSignal(str)
    SetUpProgressBarSignal = pyqtSignal(int)
    AllCompletedSignal = pyqtSignal()

    def __init__(self):
        super(LidcData, self).__init__()
        self.SeriesList = []
        self.PatientList = []
        self.MetaDataFilePath = ""
        self.RootDir = ""

    def init(self, rootdir):
        self.RootDir = rootdir

    def run(self):
        # 找到所有的Patient目录和MetaData.csv文件
        if os.path.exists(self.RootDir):  # 判断路径是否存在
            item_names = os.listdir(self.RootDir)  # 获取该目录下的所有文件或文件夹的名字
            for itemName in item_names:
                item_abs_path = os.path.join(self.RootDir, itemName)  # 获取每个item的绝对路径
                if os.path.isdir(item_abs_path):
                    self.PatientList.append(item_abs_path)
                elif itemName == "LIDC-IDRI_MetaData.csv":
                    self.MetaDataFilePath = item_abs_path
            self.SetUpProgressBarSignal.emit(len(self.PatientList))  # 发出信号,总长度探测OK
            self.SendTextSignal.emit("根目装载成功!检测到" + str(len(self.PatientList)) + "个patient..")
        else:
            self.SendTextSignal.emit("路径不存在")
        # 迭代PatientList,找到所有的序列
        for Patient in self.PatientList:
            studies = os.listdir(Patient)  # studies是当前patient文件夹下的study文件夹相对名的列表,
            for study in studies:
                series = os.listdir(os.path.join(Patient, study))  # series是当前study下的series文件夹的名字
                self.SeriesList.append(LidcSeries(Patient, study, series[0]))
                self.SendTextSignal.emit("第" + str(len(self.SeriesList)) + "个序列处理完成!")
            self.MoveSignal.emit()
        self.SendTextSignal.emit("全部处理完成!")
        self.AllCompletedSignal.emit()

    def __del__(self):
        self.wait()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = LidcData()  # in Asus Laptop
    obj.init("F:\\TCIA_LIDC-IDRI\LIDC-IDRI")
    # obj = LidcData("G:\\TCIA_LIDC-IDRI\\LIDC-IDRI-Sample")  # in B234 Desktop
    obj.start()
    print("异步")
    for seri in obj.SeriesList:  # start是异步方法,这样写是不会输出任何东西的
        print(seri.SeriesID)
        print("xml" + seri.XmlFilePath)
        print(len(seri.DcmFileList))
    sys.exit(app.exec_())
