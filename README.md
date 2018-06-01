Vector-Generating Network
======================
#### A convolutional neural network with the ultimate goal of generating eigenvectors
#### 构想中的一种卷积神经网络


### 主要目标
用于肺结节分类和恶性预测,实现自动定位肺结节的位置,对每个结节进行恶性程度预测,并最终给出该病人患病的概率<br>

### 主要思路
1. 使用基于U-Net的NetA进行结节的定位和分割<br>
2. 使用NetB进行结节的恶性程度分类<br>
3. 使用特征向量描述一个完整的病例<br>
4. 使用NetC给出诊断结论<br>

### 数据集
1. [Luna16](https://luna16.grand-challenge.org/):<br>
   文件形式:mhd/raw,csv<br>
   组织结构:所有的mhd/raw文件存储在一个目录下;有两个csv文件,存储所有的标签;每一对mhd/raw中是一个序列.<br>
   标签形式:一个csv文件列出所有的候选结节,标记有定位信息和(0/1)标签,标记为1的结节在另一个csv文件中标有有直径信息和定位信息<br>
2. [DSB2017](https://www.kaggle.com/c/data-science-bowl-2017):<br>
   文件形式:dcm,csv<br>
   组织结构:图像数据分为两个stage文件夹,每个stage下存放一些series文件夹,每个series文件夹下存放一些dcm文件,每个dcm文件存储一张切片.<br>
   标签形式:在csv文件中对每个序列给出(0/1)标签<br>
3. [TCIA LIDC-IDRI](https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI):<br>
   文件形式:dcm,xml,csv,xlsx<br>
   组织结构:由1010个名称形如LIDC-IDRI-XXXX文件夹组成,每个文件夹存储一个病人的数据;<br>
           病人文件夹下,是study文件夹,注意有的病人有两个study,有的只有一个study;共有1308个study;<br>
           study文件夹下,是series文件夹,注意所有的study都只有一个series;共有1308个series,其中1018个CTseries,290个CR/DX series<br>
           series文件夹下有该series的全部slice和一个xml文件,需要注意的是,dcm文件按名称排序的顺序并不是解刨学顺序,而Instance Number的顺序是解刨学顺序<br>
           除此之外,还有数个表格文件<br>
   标签形式:series文件夹下的xml文件中,存储标记信息,xml标注含义请看[XmlPattern](https://github.com/AngelaViVi/VectorGeneratingNetwork/Projects/LIDCReader/XmlPattern.xml).<br>
           另外,lidc-idri nodule counts.xlsx描述每个病人的结节总数,3mm以上的结节数,3mm以下的结节数<br>
           LIDC-IDRI_MetaData.csv中给出了每个patient ID,扫描形式,seriesID的对应关系以及一些其他的元数据信息<br>
           tcia-diagnosis-data-2012-04-20.xls中存储了158个病人的详细诊断信息,包括病人层次的诊断结论,原发位置,确诊方式以及结节层次的诊断结论和确诊方式等<br>
### 参考项目
1. [DSB2017第一名:grt123](https://github.com/lfz/DSB2017)<br>
2. [Unet细胞分割](https://github.com/zhixuhao/unet)<br>
   对应的CSDN博客:[全卷机神经网络图像分割(U-net)-keras实现](https://blog.csdn.net/u012931582/article/details/70215756)<br>
3. [Unet图像分割](https://github.com/ZFTurbo/ZF_UNET_224_Pretrained_Model)<br>
4. [Luna16数据预处理](https://gitlab.tianchi.aliyun.com/jchen/TCM_AI)<br>
   对应的CSDN博客[这篇经验说不定会帮你夺冠医疗AI大赛哦](https://blog.csdn.net/c2a2o2/article/details/77466692)<br>
5. DSB2017数据集预处理(肺部图像形态学分割)[Candidate Generation and LUNA16 preprocessing](http://www.cnblogs.com/skykill/p/8016606.html)<br>
   注意这篇文章虽然写的是处理Luna16,但是实际上他是处理DSB2017.事实上,这种分割方法并不是针对某个数据集的,但是这两个数据集的读取方式是不同的<br>
6. 关于内存溢出问题的解决方案[TensorFlow和Keras解决大数据量内存溢出问题](https://zhuanlan.zhihu.com/p/35866604)<br>
7. LIDC-IDRI数据集:<br>
   [LIDC-IDRI肺结节公开数据集Dicom和XML标注详解](https://blog.csdn.net/dcxhun3/article/details/54289598)<br>
8. [lidc nodule detection with CNN and LSTM network](https://github.com/zhwhong/lidc_nodule_detection)<br>
   这个项目中对LIDC-IDRI的读取部分非常值得参考<br>
   对应的博客文章:[LIDC-IDRI肺结节Dicom数据集解析与总结](https://www.jianshu.com/p/9c1facf70b01)<br>
### 工具
1. Raw/mhd图像查看,三维检视:[Fiji](http://imagej.net/Fiji)<br>
2. dcm/DICOM标准文件查看:[RadiAnt](https://www.radiantviewer.com/)<br>
3. 绘图工具:[Draw.io](https://www.draw.io/)<br>

### 参考文献
见./Reference/

### 工程说明
1. ./log/:存放开发日志,记录一些想法和debug日志等信息.<br>
2. ./Project/:具体工程的父目录.<br>
3. ./Reference/:存放参考文献,主要是论文和论文的翻译版.<br>
4. ./Tools/:存放Protable的工具.<br>

### 工程结构约定:
1. 按照上述目录结构存放<br>
2. 如果是Demo,项目内部附带所需数据,如果数据大于100MB,在存放数据的文件夹下放置placeholder,并在项目的README中给出下载地址.<br>
3. 每个工程独立存放在一个文件夹中,并放置在Project文件夹下,每个工程自带自己的README文件.<br>
4. 如果有参考,论文下载到Reference文件夹下,博客和项目的地址除了在工程内部的README注明外,还要在整个项目的README中注明.<br>

### build
1. Anaconda3-5.1.0 with python 3.6.4<br>
2. CUDA_9.0.176_win10<br>
3. cudnn-9.0-windows10-x64-v7.zip<br>
4. tensorflow 1.7.0<br>
5. keras 2.1.6<br>
