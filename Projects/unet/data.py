from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import numpy as np
import os
import glob
import cv2
import definition

"""
先把训练用的的数据图片和标签图片合并起来
再用keras预处理进行数据扩充
最后再把数据图片和标签图片分开
"""


class myAugmentation(object):
    "构造方法"

    def __init__(self):
        # 目录检查
        if not os.path.isdir(definition.Augment_MergePath):
            os.makedirs(definition.Augment_MergePath)
        if not os.path.isdir(definition.Augment_LabelPath):
            os.makedirs(definition.Augment_LabelPath)
        if not os.path.isdir(definition.Augment_ImgPath):
            os.makedirs(definition.Augment_ImgPath)
        self.slices = 30
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
        print("合并标签和数据图片,进行同步变换...")
        # 列出原始的训练用图片和标签
        trainImgNames = os.listdir(definition.TrainImgPath)
        trainLabelNames = os.listdir(definition.TrainLabelPath)
        self.slices = len(trainImgNames)
        if len(trainImgNames) != len(trainLabelNames) or len(trainImgNames) == 0 or len(trainLabelNames) == 0:
            print("训练数据中图片和标签数量不匹配!")
            return 0
        for i in range(len(trainImgNames)):
            img_t = load_img(definition.TrainImgPath + "/" + str(i) + "." + definition.FileExtension)
            img_l = load_img(definition.TrainLabelPath + "/" + str(i) + "." + definition.FileExtension)
            x_t = img_to_array(img_t)
            x_l = img_to_array(img_l)
            x_t[:, :, 2] = x_l[:, :, 0]
            img_tmp = array_to_img(x_t)
            img_tmp.save(definition.Augment_MergePath + "/" + str(i) + "." + definition.FileExtension)
            img = x_t
            img = img.reshape((1,) + img.shape)
            savedir = definition.Augment_MergePath + "/" + str(i)
            if not os.path.lexists(savedir):
                os.mkdir(savedir)
            self.doAugmentate(img, savedir, str(i), len(trainImgNames))
        print("变换完毕!")

    "augmentate one image"

    def doAugmentate(self, img, save_to_dir, save_prefix, imgnum, batch_size=1, save_format=definition.FileExtension):
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
        print("分开训练数据图片和训练标签图片...")
        for i in range(self.slices):
            path = definition.Augment_MergePath + "/" + str(i)
            train_imgs = glob.glob(path + "/*." + definition.FileExtension)
            savedir = definition.Augment_ImgPath + "/" + str(i)
            if not os.path.lexists(savedir):
                os.mkdir(savedir)
            savedir = definition.Augment_LabelPath + "/" + str(i)
            if not os.path.lexists(savedir):
                os.mkdir(savedir)
            for imgname in train_imgs:
                tempName = imgname.replace("\\", "/")  # windows的目录分隔符是'\',linux是/
                midname = tempName[tempName.rindex("/") + 1:tempName.rindex("." + definition.FileExtension)]
                img = cv2.imread(imgname)
                img_train = img[:, :, 2]  # cv2 read image rgb->bgr
                img_label = img[:, :, 0]

                cv2.imwrite(definition.Augment_ImgPath + "/" + str(
                    i) + "/" + midname + "_train" + "." + definition.FileExtension,
                            img_train)
                cv2.imwrite(
                    definition.Augment_LabelPath + "/" + str(
                        i) + "/" + midname + "_label" + "." + definition.FileExtension,
                    img_label)
        print("分离完毕!")

    "split perspective transform images"

    def splitTransform(self):
        # path_merge = "transform"
        # path_train = "transform/data/"
        # path_label = "transform/label/"
        path_merge = "deform/deform_norm2"
        path_train = "deform/train/"
        path_label = "deform/label/"
        print("split perspective transform images...")
        train_imgs = glob.glob(definition.Augment_MergePath + "/*." + definition.FileExtension)
        for imgname in train_imgs:
            tempName = imgname.replace("\\", "/")  # windows的目录分隔符是'\',linux是/
            midname = tempName[tempName.rindex("/") + 1:tempName.rindex("." + definition.FileExtension)]
            img = cv2.imread(imgname)
            img_train = img[:, :, 2]  # cv2 read image rgb->bgr
            img_label = img[:, :, 0]
            cv2.imwrite(definition.Augment_ImgPath + "/" + midname + "." + definition.FileExtension, img_train)
            cv2.imwrite(definition.Augment_LabelPath + "/" + midname + "." + definition.FileExtension, img_label)
        print("Done!")

"""
负责进行数据的转储和转储数据的读取
"""


class dataProcess(object):
    "构造方法"

    def __init__(self, out_rows, out_cols, ):
        self.out_rows = out_rows
        self.out_cols = out_cols
        if not os.path.isdir(definition.InputNpyPath):
            os.makedirs(definition.InputNpyPath)
        if not os.path.isdir(definition.OutputPath):
            os.makedirs(definition.OutputPath)
    "将训练数据转储进npy"

    def create_train_data(self):
        print("转储训练数据...")
        trainImgNames = os.listdir(definition.TrainImgPath)
        trainLabelNames = os.listdir(definition.TrainLabelPath)
        if len(trainImgNames) != len(trainLabelNames):
            print("训练图片和训练标签的数量不相等!无法dump训练数据")
        else:
            numOfImg = len(trainImgNames)
            print("共找到" + str(numOfImg) + "对训练数据")
            imgdatas = np.ndarray((numOfImg, self.out_rows, self.out_cols, 1), dtype=np.uint8)
            imglabels = np.ndarray((numOfImg, self.out_rows, self.out_cols, 1), dtype=np.uint8)
            for k in range(numOfImg):
                img = load_img(definition.TrainImgPath+"/"+str(k)+"."+definition.FileExtension, grayscale=True)
                label = load_img(definition.TrainLabelPath+"/"+str(k)+"."+definition.FileExtension, grayscale=True)
                img = img_to_array(img)
                label = img_to_array(label)
                imgdatas[k] = img
                imglabels[k] = label
            print("加载完成,正在转储...")
            np.save(definition.InputNpyPath + '/imgs_train.npy', imgdatas)
            np.save(definition.InputNpyPath + '/imgs_mask_train.npy', imglabels)
            print("转储完成")

    "将测试数据转储进npy"

    def create_test_data(self):
        print("转储测试数据...")
        # 加载测试用图片和标签的路径
        testImgNames = os.listdir(definition.TestImgPath)
        numOfImg = len(testImgNames)
        print("共找到" + str(numOfImg) + "个测试数据")
        imgdatas = np.ndarray((numOfImg, self.out_rows, self.out_cols, 1), dtype=np.uint8)

        for k in range(numOfImg):
            img = load_img(definition.TestImgPath+"/"+str(k)+"."+definition.FileExtension, grayscale=True)
            img = img_to_array(img)
            imgdatas[k] = img

        print("加载完成,正在转储...")
        np.save(definition.InputNpyPath + '/imgs_test.npy', imgdatas)
        print("转储完成")

    "加载npy训练数据,返回含有训练数据和测试数据的数组"

    def load_train_data(self):
        print('-' * 30)
        print('加载训练数据')
        print('-' * 30)
        imgs_train = np.load(definition.InputNpyPath + "/imgs_train.npy")
        imgs_mask_train = np.load(definition.InputNpyPath + "/imgs_mask_train.npy")
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
        print('加载测试数据')
        print('-' * 30)
        imgs_test = np.load(definition.InputNpyPath + "/imgs_test.npy")
        imgs_test = imgs_test.astype('float32')
        imgs_test /= 255
        # mean = imgs_test.mean(axis = 0)
        # imgs_test -= mean
        return imgs_test


if __name__ == "__main__":
    aug = myAugmentation()
    aug.Augmentation()
    aug.splitMerge()
    aug.splitTransform()

    #mydata = dataProcess(definition.ImgW, definition.ImgH)
    #mydata.create_train_data()
    #mydata.create_test_data()
    # fp = open('./augment/image/0/0/0_0_1305_train.tif', 'w')
    # img = cv2.imread("F:/cj.jpg")
    # cv2.imwrite("F:/cj2.jpg",img)
