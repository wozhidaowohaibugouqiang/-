# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
#绿色阈值
greenLower = np.array([40, 100, 120])
greenUpper = np.array([67, 200, 200])

# 彩色图像全局直方图均衡化
def hisEqulColor1(img):
    # 将RGB图像转换到YCrCb空间中
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    # 将YCrCb图像通道分离
    channels = cv2.split(ycrcb)
    # 对第1个通道即亮度通道进行全局直方图均衡化并保存
    cv2.equalizeHist(channels[0], channels[0])
    # 将处理后的通道和没有处理的两个通道合并，命名为ycrcb
    cv2.merge(channels, ycrcb)
    # 将YCrCb图像转换回RGB图像
    cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)
    return img

def read_path(file_pathname):
    #遍历该目录下的所有图片文件
    for filename in os.listdir(file_pathname):
        print(filename)
        # 读取图像
        img = cv2.imread(file_pathname+'/'+filename)
        # 中值滤波
        img_median = cv2.medianBlur(img, 3)
        scr = img_median.copy()
        # 全局自适应直方图均衡化
        res1 = hisEqulColor1(scr)
        # 例图太大了，缩小一下
        # 正常显示的话就是cv.imshow('img1',res1)
        img_test = cv2.resize(res1, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
        # 转换为浮点数进行计算
        fsrc = np.array(img_test, dtype=np.float32) / 255.0
        (b, g, r) = cv2.split(fsrc)
        gray = 2 * g - b - r

        # 求取最大值和最小值
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

        # 计算直方图
        hist = cv2.calcHist([gray], [0], None, [256], [minVal, maxVal])
        # plt.plot(hist)
        # plt.show()
        # cv2.waitKey()

        # 转换为u8类型，进行otsu二值化
        gray_u8 = np.array((gray - minVal) / (maxVal - minVal) * 255, dtype=np.uint8)
        (thresh, bin_img) = cv2.threshold(gray_u8, -1.0, 255, cv2.THRESH_OTSU)
        # plt.savefig("C:/Users/Admin/Desktop/1.jpg")
        # cv2.imwrite('C:/Users/Lenovo/Desktop/1.jpg', bin_img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        # cv2.imshow('bin_img', bin_img)

        # 得到彩色的图像
        (b8, g8, r8) = cv2.split(img_test)
        color_img = cv2.merge([b8 & bin_img, g8 & bin_img, r8 & bin_img])
        hsv = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)
        # 去除颜色范围外的其余颜色
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        # 二值化操作
        ret, binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        # 膨胀操作，因为是对线条进行提取定位，所以腐蚀可能会造成更大间隔的断点，将线条切断，因此仅做膨胀操作
        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(binary, kernel, iterations=1)
        # 获取图像轮廓坐标，其中contours为坐标值，此处只检测外形轮廓
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            i = 1
            # cv2.boundingRect()返回轮廓矩阵的坐标值，四个值为x, y, w, h， 其中x, y为左上角坐标，w,h为矩阵的宽和高
            boxes = [cv2.boundingRect(c) for c in contours]
            for box in boxes:
                x, y, w, h = box
                if (w * h) > 45000 and (w > 200 or h > 200):
                    # save figure
                    save_path = "C:/Users/Lenovo/Desktop/xiangcai"
                    out_file_name = filename + '_' + str(i)
                    save_path_file = os.path.join(save_path, out_file_name + '.jpg')
                    cv2.imwrite(save_path_file, color_img[y:y + h, x:x + w])
                    i = i + 1

#注意*处如果包含家目录（home）不能写成~符号代替
#必须要写成"/home"的格式，否则会报错说找不到对应的目录
#读取的目录
read_path("C:/Users/Lenovo/Desktop/xiangcaiyuantu")

