from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import numpy as np
import os
import glob
# import cv2
# from libtiff import TIFF
"""
先把训练用的的数据图片和标签图片合并起来
再用keras预处理进行数据扩充
最后再把数据图片和标签图片分开
"""
class myAugmentation(object):
    "构造方法"
    def __init__(self, train_path="train",
                 label_path="label",
                 merge_path="merge",
                 aug_merge_path="aug_merge",
                 aug_train_path="aug_train",
                 aug_label_path="aug_label",
                 img_type="tif"):

        self.train_imgs = glob.glob(train_path + "/*." + img_type)
        self.label_imgs = glob.glob(label_path + "/*." + img_type)
        self.train_path = train_path
        self.label_path = label_path
        self.merge_path = merge_path
        self.img_type = img_type
        self.aug_merge_path = aug_merge_path
        self.aug_train_path = aug_train_path
        self.aug_label_path = aug_label_path
        self.slices = len(self.train_imgs)
        self.datagen = ImageDataGenerator(
            rotation_range=0.2,
            width_shift_range=0.05,
            height_shift_range=0.05,
            shear_range=0.05,
            zoom_range=0.05,
            horizontal_flip=True,
            fill_mode='nearest')

    "Start augmentation....."
    def Augmentation(self):
        trains = self.train_imgs
        labels = self.label_imgs
        path_train = self.train_path
        path_label = self.label_path
        path_merge = self.merge_path
        imgtype = self.img_type
        path_aug_merge = self.aug_merge_path
        if len(trains) != len(labels) or len(trains) == 0 or len(trains) == 0:
            print("trains can't match labels")
            return 0
        for i in range(len(trains)):
            img_t = load_img(path_train + "/" + str(i) + "." + imgtype)
            img_l = load_img(path_label + "/" + str(i) + "." + imgtype)
            x_t = img_to_array(img_t)
            x_l = img_to_array(img_l)
            x_t[:, :, 2] = x_l[:, :, 0]
            img_tmp = array_to_img(x_t)
            img_tmp.save(path_merge + "/" + str(i) + "." + imgtype)
            img = x_t
            img = img.reshape((1,) + img.shape)
            savedir = path_aug_merge + "/" + str(i)
            if not os.path.lexists(savedir):
                os.mkdir(savedir)
            self.doAugmentate(img, savedir, str(i))

    "augmentate one image"
    def doAugmentate(self, img, save_to_dir, save_prefix, batch_size=1, save_format='tif', imgnum=30):
        datagen = self.datagen
        i = 0
        for batch in datagen.flow(img,
                                  batch_size=batch_size,
                                  save_to_dir=save_to_dir,
                                  save_prefix=save_prefix,
                                  save_format=save_format):
            i += 1
            if i > imgnum:
                break

    "split merged image apart"
    def splitMerge(self):
        path_merge = self.aug_merge_path
        path_train = self.aug_train_path
        path_label = self.aug_label_path
        for i in range(self.slices):
            path = path_merge + "/" + str(i)
            train_imgs = glob.glob(path + "/*." + self.img_type)
            savedir = path_train + "/" + str(i)
            if not os.path.lexists(savedir):
                os.mkdir(savedir)
            savedir = path_label + "/" + str(i)
            if not os.path.lexists(savedir):
                os.mkdir(savedir)
            for imgname in train_imgs:
                midname = imgname[imgname.rindex("/") + 1:imgname.rindex("." + self.img_type)]
                img = cv2.imread(imgname)
                img_train = img[:, :, 2]  # cv2 read image rgb->bgr
                img_label = img[:, :, 0]
                cv2.imwrite(path_train + "/" + str(i) + "/" + midname + "_train" + "." + self.img_type, img_train)
                cv2.imwrite(path_label + "/" + str(i) + "/" + midname + "_label" + "." + self.img_type, img_label)

    "split perspective transform images"
    def splitTransform(self):
        # path_merge = "transform"
        # path_train = "transform/data/"
        # path_label = "transform/label/"
        path_merge = "deform/deform_norm2"
        path_train = "deform/train/"
        path_label = "deform/label/"
        train_imgs = glob.glob(path_merge + "/*." + self.img_type)
        for imgname in train_imgs:
            midname = imgname[imgname.rindex("/") + 1:imgname.rindex("." + self.img_type)]
            img = cv2.imread(imgname)
            img_train = img[:, :, 2]  # cv2 read image rgb->bgr
            img_label = img[:, :, 0]
            cv2.imwrite(path_train + midname + "." + self.img_type, img_train)
            cv2.imwrite(path_label + midname + "." + self.img_type, img_label)

"""
负责进行数据的转储和转储数据的读取
"""
class dataProcess(object):
    "构造方法"
    def __init__(self,
                 out_rows,
                 out_cols,
                 data_path="./data/train",
                 label_path="./data/train/label",
                 test_path="./data",
                 npy_path="./npydata",
                 img_type="tif"):

        self.out_rows = out_rows
        self.out_cols = out_cols
        self.data_path = data_path
        self.label_path = label_path
        self.img_type = img_type
        self.test_path = test_path
        self.npy_path = npy_path

    "将训练数据转储进npy"
    def create_train_data(self):
        print("转储训练数据...")
		# 1.加载训练用图片和标签的路径
        trainImgPath="F:/unet/data/train/image"
        trainLabelPath="F:/unet/data/train/label"
        trainImgNames = os.listdir(trainImgPath)
        trainLabelNames = os.listdir(trainLabelPath)
        if len(trainImgNames)!=len(trainLabelNames):
            print("训练图片和训练标签的数量不相等!无法dump训练数据")
        else:
            numOfImg=len(trainImgNames)
            print("共找到"+str(numOfImg)+"对训练数据")
            imgdatas = np.ndarray((numOfImg, self.out_rows, self.out_cols, 1), dtype=np.uint8)
            imglabels = np.ndarray((numOfImg, self.out_rows, self.out_cols, 1), dtype=np.uint8)
            for k in range(0,numOfImg):
                img = load_img(os.path.join(trainImgPath,trainImgNames[k]), grayscale=True)
                label = load_img(os.path.join(trainLabelPath,trainLabelNames[k]), grayscale=True)
                img = img_to_array(img)
                label = img_to_array(label)
                imgdatas[k] = img
                imglabels[k] = label
            print("加载完成,正在转储...")
            np.save(self.npy_path + '/imgs_train.npy', imgdatas)
            np.save(self.npy_path + '/imgs_mask_train.npy', imglabels)
            print("转储完成")

    "将测试数据转储进npy"
    def create_test_data(self):
        print("转储测试数据...")
        # 加载测试用图片和标签的路径
        testImgPath = "F:/unet/data/test"
        testImgNames = os.listdir(testImgPath)
        numOfImg = len(testImgNames)
        print("共找到" + str(numOfImg) + "个测试数据")
        imgdatas = np.ndarray((numOfImg, self.out_rows, self.out_cols, 1), dtype=np.uint8)

        for k in range(0, numOfImg):
            img = load_img(os.path.join(testImgPath, testImgNames[k]), grayscale=True)
            img = img_to_array(img)
            imgdatas[k] = img

        print("加载完成,正在转储...")
        np.save(self.npy_path + '/imgs_test.npy', imgdatas)
        print("转储完成")

    "加载npy训练数据,返回含有训练数据和测试数据的数组"
    def load_train_data(self):
        print('-' * 30)
        print('load train images...')
        print('-' * 30)
        imgs_train = np.load(self.npy_path + "/imgs_train.npy")
        imgs_mask_train = np.load(self.npy_path + "/imgs_mask_train.npy")
        imgs_train = imgs_train.astype('float32')
        imgs_mask_train = imgs_mask_train.astype('float32')
        imgs_train /= 255
        # mean = imgs_train.mean(axis = 0)
        # imgs_train -= mean
        imgs_mask_train /= 255
        imgs_mask_train[imgs_mask_train > 0.5] = 1
        imgs_mask_train[imgs_mask_train <= 0.5] = 0
        return imgs_train, imgs_mask_train

    "加载npy测试数据,返回含有测试数据的数组"
    def load_test_data(self):
        print('-' * 30)
        print('load test images...')
        print('-' * 30)
        imgs_test = np.load(self.npy_path + "/imgs_test.npy")
        imgs_test = imgs_test.astype('float32')
        imgs_test /= 255
        # mean = imgs_test.mean(axis = 0)
        # imgs_test -= mean
        return imgs_test


if __name__ == "__main__":
    # aug = myAugmentation()
    # aug.Augmentation()
    # aug.splitMerge()
    # aug.splitTransform()
    mydata = dataProcess(256, 256)
    mydata.create_train_data()
    mydata.create_test_data()
