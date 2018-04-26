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
1. Luna16:文件形式:mhd/raw/csv,含有结节定位信息,(0/1)标签,标记为1的结节有直径信息<br>
2. DSB2017:文件形式:dcm/csv<br>
3. TCIA LIDC-IDRI:文件形式:dcm/xml/csv/xlsx<br>

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
