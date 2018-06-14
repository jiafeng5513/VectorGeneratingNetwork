"""
定义全局变量
"""
# 训练图片所在目录
TrainImgPath = "./data/train/image"
# 训练标签所在目录
TrainLabelPath = "./data/train/label"
# 测试图片所在目录
TestImgPath = "./data/test"
# 训练和测试所用的文件扩展名
FileExtension = "tif"
# 数据扩充操作时,存储中间结果的目录
Augment_MergePath = "./augment/merge"
# 数据扩充操作时,存储训练图片的目录
Augment_ImgPath = "./augment/image"
# 数据扩充操作时,存储标签的目录
Augment_LabelPath = "./augment/label"
# 训练和测试用npy转储文件所在目录
InputNpyPath = "./npydata"
# 测试结果图片和npy输出目录
OutputPath = "./result"
# 图片尺寸:横向
ImgW = 256
# 图片尺寸:纵向
ImgH = 256
