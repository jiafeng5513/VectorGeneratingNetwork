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

#====================函数定义========================
#读取Dicom文件中的病人信息
def loadFileInformation(filename):
    information = {}
    ds = dicom.read_file(filename)
    information['PatientID'] = ds.PatientID
    information['PatientName'] = ds.PatientName
    information['PatientBirthDate'] = ds.PatientBirthDate
    return information

# 某个病人CT_path=image_path+'/00cba091fa4ad62cc3200a657aeb957e'
# ct_scan = read_ct_scan(某个病人CT_path)
def read_ct_scan(folder_name):
    # Read the slices from the dicom file
    slices = [dicom.read_file(folder_name + '/'+filename) for filename in os.listdir(folder_name)]
    # Sort the dicom slices in their respective order
    slices.sort(key=lambda x: int(x.InstanceNumber))
    # Get the pixel values for all the slices
    slices = np.stack([s.pixel_array for s in slices])
    slices[slices == -2000] = 0
    return slices

#绘出一个slice
def plot_ct_scan(scan):
    f, plots = plt.subplots(int(scan.shape[0] / 20) + 1, 4, figsize=(25, 25))
    for i in range(0, scan.shape[0], 5):
        plots[int(i / 20), int((i % 20) / 5)].axis('off')
        plots[int(i / 20), int((i % 20) / 5)].imshow(scan[i], cmap=plt.cm.bone)

# 肺分割,第一个参数是一张CT,第二个参数决定是否绘制出处理过程
def get_segmented_lungs(im, plot=False):

    if plot == True:
        f, plots = plt.subplots(8, 1, figsize=(5, 40))
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

# 对一个slice进行分割
def segment_lung_from_ct_scan(ct_scan):
    return np.asarray([get_segmented_lungs(slice) for slice in ct_scan])

# 三维重建绘制
def plot_3d(image, threshold=-300):
    # Position the scan upright,
    # so the head of the patient would be at the top facing the camera
    p = image.transpose(2, 1, 0)
    p = p[:, :, ::-1]

    verts, faces = measure.marching_cubes_classic(p, threshold)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Fancy indexing: `verts[faces]` to generate a collection of triangles
    mesh = Poly3DCollection(verts[faces], alpha=0.1)
    face_color = [0.5, 0.5, 1]
    mesh.set_facecolor(face_color)
    ax.add_collection3d(mesh)

    ax.set_xlim(0, p.shape[0])
    ax.set_ylim(0, p.shape[1])
    ax.set_zlim(0, p.shape[2])
#=====================执行===========================

ct_scan = read_ct_scan('./00cba091fa4ad62cc3200a657aeb957e')

# #实验1:用0更新-2000的亮度值
# random_dcm_path='./00cba091fa4ad62cc3200a657aeb957e/38c4ff5d36b5a6b6dc025435d62a143d.dcm'
# # print(loadFileInformation(random_dcm_path))
# lung = dicom.read_file(random_dcm_path)
# slice = lung.pixel_array
# slice[slice == -2000] = 0
# plt.imshow(slice, cmap=plt.cm.gray)
# plt.show()

# #实验2:显示一个序列
# plot_ct_scan(ct_scan)
# plt.show()

#实验3:对一张图片进行形态学处理并绘制流程(True为绘制流程,False为不绘制流程只处理)
# get_segmented_lungs(ct_scan[71], True)
# plt.show()

# #实验4:对一个序列的图片进行形态学处理并绘制
# segmented_ct_scan = segment_lung_from_ct_scan(ct_scan)
# plot_ct_scan(segmented_ct_scan)
# plt.show()

# #实验5:使用强度进行肺分割(604对应-400HU,小于此值的过滤掉)
# segmented_ct_scan = segment_lung_from_ct_scan(ct_scan)
# segmented_ct_scan[segmented_ct_scan < 604] = 0
# plot_ct_scan(segmented_ct_scan)
# plt.show()

#实验6:remove the two largest connected component
segmented_ct_scan = segment_lung_from_ct_scan(ct_scan)
selem = ball(2)
binary = binary_closing(segmented_ct_scan, selem)

label_scan = label(binary)

areas = [r.area for r in regionprops(label_scan)]
areas.sort()

for r in regionprops(label_scan):
    max_x, max_y, max_z = 0, 0, 0
    min_x, min_y, min_z = 1000, 1000, 1000

    for c in r.coords:
        max_z = max(c[0], max_z)
        max_y = max(c[1], max_y)
        max_x = max(c[2], max_x)

        min_z = min(c[0], min_z)
        min_y = min(c[1], min_y)
        min_x = min(c[2], min_x)
    if (min_z == max_z or min_y == max_y or min_x == max_x or r.area > areas[-3]):
        for c in r.coords:
            segmented_ct_scan[c[0], c[1], c[2]] = 0
    else:
        index = (max((max_x - min_x), (max_y - min_y), (max_z - min_z))) / (min((max_x - min_x), (max_y - min_y), (max_z - min_z)))

plot_3d(segmented_ct_scan, 604)
plt.show()