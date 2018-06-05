"""
Model for Lidc-idri
描述LIdc-Idri数据集的组织结构
为了尽量简化流程提高效率,我做如下规定:
    1.LIDC-IDRI父目录下,应当存放名字形如LIDC-IDRI-XXXX的Patient文件夹若干
    2.LIDC-IDRI父目录下,应当存放有LIDC-IDRI_MetaData.csv
    3.每个Patient目录下,应当存放有一个或者两个Study文件夹,以Study UID 命名
    4.每个Study目录下,应当有唯一一个series文件夹,以Series UID命名
    5.每个Series文件夹下,应当存放一系列DCM文件和一个xml文件
"""
import os
import pydicom
import datetime


"描述LidcSeries"
class LidcSeries(object):
    "构造函数"
    def __init__(self, patientAbsPath, studyName, seriesName):
        self.SeriesID=seriesName
        self.SeriesAbsPath='%s\\%s\\%s' % (patientAbsPath, studyName, seriesName)
        # 找到series路径下的全部文件,把DCM文件和xml文件的绝对路径分别存储
        self.DcmFileList=[]
        # 先检查是否存在DcmList.txt,如果存在,从txt中直接取出xml文件和排好序的dcm文件列表
        if os.path.exists(self.SeriesAbsPath+"\\DcmList.txt"):
            SortFile = open(self.SeriesAbsPath + "\\DcmList.txt", 'r')
            lines = SortFile.readlines()  # 读取全部内容
            self.XmlFilePath = lines[0] # 已经取出xml文件



        itemNames = os.listdir(self.SeriesAbsPath)  # 获取该目录下的所有文件
        self.FindSortFile = False
        for itemName in itemNames:
            itemAbsPath = os.path.join(self.SeriesAbsPath, itemName)  # 获取每个item的绝对路径
            if("dcm" in itemName):#发现dcm文件
                self.DcmFileList.append(itemAbsPath)
            elif("xml" in itemName):#发现xml标签文件
                self.XmlFilePath=itemAbsPath
            elif("txt" in itemName):#发现txt排序文件
                self.SortFilePath=itemAbsPath
                self.FindSortFile=True#标记:找到了排序文件
        #把dcm文件的绝对路径按照解刨学顺序排列
        self.SortDcmListBySliceLocation(self.DcmFileList)


    "为DcmList按照SliceLocation排序"
    def SortDcmListBySliceLocation(self,dcmlist):
        if pydicom.read_file(dcmlist[0]).Modality!="CT":#只有CT序列需要排序
            return dcmlist
        else:
            #先询问有没有排序文件,如果有,直接加载,如果没有,现场排序并生成排序文件
            print("按照SliceLocation字段对dcm文件列表进行排序,待排序列表长度为:"+str(len(dcmlist)))
            flag = 1
            for index in range(len(dcmlist) - 1, 0, -1):
                if flag:
                    flag = 0
                    for two_index in range(index):
                        ds1 = pydicom.read_file(dcmlist[two_index]).SliceLocation
                        ds2 = pydicom.read_file(dcmlist[two_index+1]).SliceLocation
                        if ds1 < ds2:#排序依据是SliceLocation从大到小(基本全是负数)
                            dcmlist[two_index], dcmlist[two_index + 1] = dcmlist[two_index + 1], dcmlist[two_index]
                            flag = 1
                else:
                    break
            #在此处保存排序文件
            SortFile=open(self.SeriesAbsPath+"\\DcmList.txt",'w')
            SortFile.writelines(self.XmlFilePath + "\n")#先写入xml的路径
            for word in dcmlist:#按照解破学顺序把dcm文件路径依次写入txt
                SortFile.writelines(word+"\n")
            SortFile.close()
            return dcmlist

"====================================================================================================="

"描述Lidi数据集"
class LidcData(object):
    def __init__(self,rootdir):
        self.RootDir=rootdir
        self.PatientList=[]
        # 找到所有的Patient目录和MetaData.csv文件
        if (os.path.exists(self.RootDir)):  # 判断路径是否存在
            itemNames = os.listdir(self.RootDir)  # 获取该目录下的所有文件或文件夹的名字
            for itemName in itemNames:
                itemAbsPath = os.path.join(self.RootDir, itemName)#获取每个item的绝对路径
                if (os.path.isdir(itemAbsPath)):
                    self.PatientList.append(itemAbsPath)
                elif(itemName=="LIDC-IDRI_MetaData.csv"):
                    self.MetaDataFilePath=itemAbsPath
        else:
            print("路径不存在")
        #迭代PatientList,找到所有的序列
        self.SeriesList=[]
        for Patient in self.PatientList:
            studies=os.listdir(Patient)#studies是当前patient文件夹下的study文件夹相对名的列表,
            for study in studies:
                series=os.listdir(os.path.join(Patient,study))#series是当前study下的series文件夹的名字
                self.SeriesList.append(LidcSeries(Patient,study,series[0]))


if __name__ == '__main__':
    ds1 = pydicom.read_file("F:\\TCIA_LIDC-IDRI\LIDC-IDRI\LIDC-IDRI-0001\\1.3.6.1.4.1.14519.5.2.1.6279.6001.298806137288633453246975630178\\1.3.6.1.4.1.14519.5.2.1.6279.6001.179049373636438705059720603192\\000005.dcm")
    print(ds1.SliceLocation)

    obj=LidcData("F:\\TCIA_LIDC-IDRI\LIDC-IDRI")
    for seri in obj.SeriesList:
        print(seri.SeriesID)
        print("xml"+seri.XmlFilePath)
        print(len(seri.DcmFileList))
