import cv2
import matplotlib.pyplot as plt
import numpy as np
# 轮廓检测时，对象必须是白色的，背景是黑色的。
#读取图片
img=cv2.imread("C:/Users/Lenovo/Desktop/shucaishibie/cut_image/cut_image_2.jpg")
#灰度
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#高斯滤波
img = cv2.GaussianBlur(gray,(9,9),0)
#canny边缘检测
canny = cv2.Canny(img, 100, 150)
#膨胀
kernel = np.ones((3, 3), np.uint8)
open = cv2.dilate(canny, kernel,iterations=1)
print(np.shape(open))
#阈值设定
thres_label = 20000
new_label = np.zeros(open.shape,np.uint8)
contours,hierarchy = cv2.findContours(open,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
n=len(contours)  #轮廓的个数
for i in range(n):
    temp = np.zeros(open.shape,np.uint8)
    temp[open == i] = i
    for num,values in enumerate(contours):
#小于阈值去除
        if cv2.contourArea(values) < thres_label:
            cv2.drawContours(temp,contours,num,0,thickness=-1)
    new_label += temp
#新图像
img1 = new_label
cv2.namedWindow("title", cv2.WINDOW_NORMAL)
cv2.resizeWindow("title", 1000, 700)
cv2.imshow("title", img1)
cv2.waitKey(0)
cv2.destroyAllWindows()

