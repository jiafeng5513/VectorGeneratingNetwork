"""
用于生成标签图
1.颜色定义:体外/体内非肺/肺/结节
2.步骤:体外上色
    2.1.体内肺部区域上色
    2.2.体内非肺部区域上色
    2.3.结节上色
3.
"""

import pydicom as dicom
import matplotlib.pyplot as plt
import numpy as np
import os
from skimage.segmentation import clear_border
from skimage.measure import label,regionprops, perimeter
from skimage.morphology import binary_dilation, binary_opening
from skimage.morphology import ball, disk, dilation, binary_erosion, remove_small_objects, erosion, closing, reconstruction, binary_closing
from skimage.filters import roberts, sobel
from skimage import measure, feature
from scipy import ndimage as ndi
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# 肺分割,第一个参数是一张CT,第二个参数决定是否绘制出处理过程
"""
生成mask并用mask找出原始肺部CT图片中的肺部数据,讲其他部分全部调0
    参数1:pydicom读出来的dcm文件
    参数2:是否绘制过程
"""
def get_segmented_lungs(im, plot=False):

    if plot == True:
        f, plots = plt.subplots(1, 8, figsize=(40, 5))
    '''
    Step 1: 以604(HU=400)为分界点二值化
    '''
    binary = im < 604
    if plot == True:
        plots[0].axis('off')
        plots[0].imshow(binary, cmap=plt.cm.bone)
    '''
    Step 2: 移除与边界相连的部分
    '''
    cleared = clear_border(binary)
    if plot == True:
        plots[1].axis('off')
        plots[1].imshow(cleared, cmap=plt.cm.bone)
    '''
    Step 3: 标记连通区域
    '''
    label_image = label(cleared)
    if plot == True:
        plots[2].axis('off')
        plots[2].imshow(label_image, cmap=plt.cm.bone)
    '''
    Step 4: 只保留两个最大的连通区域
    '''
    areas = [r.area for r in regionprops(label_image)]
    areas.sort()
    if len(areas) > 2:
        for region in regionprops(label_image):
            if region.area < areas[-2]:
                for coordinates in region.coords:
                    label_image[coordinates[0], coordinates[1]] = 0
    binary = label_image > 0
    if plot == True:
        plots[3].axis('off')
        plots[3].imshow(binary, cmap=plt.cm.bone)
    '''
    Step 5: 半径为2的腐蚀操作,分离附着于血管的肺结节
    '''
    selem = disk(2)
    binary = binary_erosion(binary, selem)
    if plot == True:
        plots[4].axis('off')
        plots[4].imshow(binary, cmap=plt.cm.bone)
    '''
    Step 6: 半径为10的闭操作,合并粘在肺壁上的结节
    '''
    selem = disk(10)
    binary = binary_closing(binary, selem)
    if plot == True:
        plots[5].axis('off')
        plots[5].imshow(binary, cmap=plt.cm.bone)
    '''
    Step 7: 填充小洞
    '''
    edges = roberts(binary)#边缘检测,Roberts算子,也可以使用sobel算子
    binary = ndi.binary_fill_holes(edges)#空洞填充
    if plot == True:
        plots[6].axis('off')
        plots[6].imshow(binary, cmap=plt.cm.bone)
    '''
    Step 8: 使用掩码提取原始图像中的肺区域
    '''
    get_high_vals = binary == 0
    im[get_high_vals] = 0
    if plot == True:
        plots[7].axis('off')
        plots[7].imshow(im, cmap=plt.cm.bone)

    return im


"""
使用类似的方法生成着色Label图片
"""
def GenerateLabel(img,plot=False):
    if plot == True:
        f, plots = plt.subplots(1, 8, figsize=(40, 5))
    '''
    Step 1: 以604(HU=400)为分界点二值化
    '''
    binary = img < 604
    if plot == True:
        plots[0].axis('off')
        plots[0].imshow(binary, cmap=plt.cm.bone)
    '''
    Step 2: 移除与边界相连的部分
    '''
    cleared = clear_border(binary)
    if plot == True:
        plots[1].axis('off')
        plots[1].imshow(cleared, cmap=plt.cm.bone)
    '''
    Step 3: 标记连通区域
    '''
    label_image = label(cleared)
    if plot == True:
        plots[2].axis('off')
        plots[2].imshow(label_image, cmap=plt.cm.bone)
    '''
    Step 4: 只保留两个最大的连通区域
    '''
    areas = [r.area for r in regionprops(label_image)]
    areas.sort()
    if len(areas) > 2:
        for region in regionprops(label_image):
            if region.area < areas[-2]:
                for coordinates in region.coords:
                    label_image[coordinates[0], coordinates[1]] = 0
    binary = label_image > 0
    if plot == True:
        plots[3].axis('off')
        plots[3].imshow(binary, cmap=plt.cm.bone)
    '''
    Step 5: 半径为2的腐蚀操作,分离附着于血管的肺结节
    '''
    selem = disk(2)
    binary = binary_erosion(binary, selem)
    if plot == True:
        plots[4].axis('off')
        plots[4].imshow(binary, cmap=plt.cm.bone)
    '''
    Step 6: 半径为10的闭操作,合并粘在肺壁上的结节
    '''
    selem = disk(10)
    binary = binary_closing(binary, selem)
    if plot == True:
        plots[5].axis('off')
        plots[5].imshow(binary, cmap=plt.cm.bone)
    '''
    Step 7: 填充小洞
    '''
    edges = roberts(binary)#边缘检测,Roberts算子,也可以使用sobel算子
    binary = ndi.binary_fill_holes(edges)#空洞填充
    if plot == True:
        plots[6].axis('off')
        plots[6].imshow(binary, cmap=plt.cm.bone)
    '''
    step7.1:着色
    '''
    # opencv开一张空白图,遍历binary,0区域一种颜色,1区域一种颜色

    '''
    step 7.2:ROI勾出来
    
    step 7.3:ROI区域另行着色
    '''
    '''
    Step 8: 使用掩码提取原始图像中的肺区域
    '''
    get_high_vals = binary == 0
    img[get_high_vals] = 0
    if plot == True:
        plots[7].axis('off')
        plots[7].imshow(img, cmap=plt.cm.bone)

    return img





if __name__ == '__main__':

    url = "../Demo/000047.dcm"
    ds = dicom.read_file(url)
    pixel_bytes = ds.PixelData
    pix = ds.pixel_array
    # pylab.imshow(ds.pixel_array, cmap=pylab.cm.bone)
    # plt.imshow(ds.pixel_array,cmap=pylab.cm.bone)

    # ax = self.DcmFigure.add_subplot(111)
    # ax.imshow(ds.pixel_array, cmap=pylab.cm.bone)  # 默认配置
    get_segmented_lungs(pix, True)
    plt.show()

