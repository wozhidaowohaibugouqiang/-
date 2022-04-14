# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt

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



# 使用2g-r-b分离土壤与背景

img = cv2.imread('C:/Users/Lenovo/Desktop/datebase/ercai/10.020002.jpg')
scr = img.copy()
#全局自适应直方图均衡化
res1 = hisEqulColor1(scr)
#例图太大了，缩小一下
#正常显示的话就是cv.imshow('img1',res1)
img_test=cv2.resize(res1, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
cv2.imshow('src', img_test)

# 转换为浮点数进行计算
fsrc = np.array(img_test, dtype=np.float32) / 255.0
(b, g, r) = cv2.split(fsrc)
gray = 2 * g - b - r

# 求取最大值和最小值
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

# 计算直方图
#hist = cv2.calcHist([gray], [0], None, [256], [minVal, maxVal])
#plt.plot(hist)
#plt.show()
#cv2.waitKey()

# 转换为u8类型，进行otsu二值化
gray_u8 = np.array((gray - minVal) / (maxVal - minVal) * 255, dtype=np.uint8)
(thresh, bin_img) = cv2.threshold(gray_u8, -1.0, 255, cv2.THRESH_OTSU)
# plt.savefig("C:/Users/Admin/Desktop/1.jpg")
#cv2.imwrite('C:/Users/Lenovo/Desktop/1.jpg', bin_img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
#cv2.imshow('bin_img', bin_img)

# 得到彩色的图像
(b8, g8, r8) = cv2.split(img_test)
color_img = cv2.merge([b8 & bin_img, g8 & bin_img, r8 & bin_img])
cv2.imwrite('C:/Users/Lenovo/Desktop/2.jpg', color_img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
cv2.imshow('color_img', color_img)