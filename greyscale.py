import cv2
import matplotlib.pyplot as plt
import numpy as np
img = cv2.imread("C:/Users/Lenovo/Desktop/shucaishibie/cut_image/cut_image_2.jpg")
img = cv2.medianBlur(img, 9)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img = cv2.GaussianBlur(gray,(9,9),0)
canny = cv2.Canny(img, 100, 150)
kernel = np.ones((3, 3), np.uint8)
open = cv2.dilate(canny, kernel,iterations=3)
# 检测图像连通区(输入为二值化图像)
contours, hierarchy = cv2.findContours(open, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1)
for n in range(len(contours)):
    # 筛选面积较大的连通区，阈值为20000
    cnt = contours[n]
    area = cv2.contourArea(cnt)
    if area > 2000:
        x,y,w,h=cv2.boundingRect(cnt)
        img_ = cv2.rectangle(canny ,(x,y),(x+w,y+h),(255,255,255),4) # 画框
        img__= canny[y-h:y+h,x-w:x+w]
        cv2.namedWindow("title", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("title", 1000, 700)
        cv2.imshow("title", img_)
        cv2.waitKey(0)
        cv2.destroyAllWindows()