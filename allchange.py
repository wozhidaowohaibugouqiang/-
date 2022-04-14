#对文件夹下面图片进行切割
import numpy as np
import cv2
import os
#设定颜色HSV范围，假定为绿色
greenLower = np.array([40, 100, 120])
greenUpper = np.array([67, 200, 200])

def read_path(file_pathname):
    #遍历该目录下的所有图片文件
    for filename in os.listdir(file_pathname):
        print(filename)
        # 读取图像
        img = cv2.imread(file_pathname+'/'+filename)
        # 中值滤波
        img_median = cv2.medianBlur(img, 5)
        # 将图像转化为HSV格式qq
        hsv = cv2.cvtColor(img_median, cv2.COLOR_BGR2HSV)
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
                if (w *h)>45000 and (w>200 or h>200) :
                    #save figure
                    save_path = "C:/Users/Lenovo/Desktop/shucaishibie/test/xiaobaicai"
                    out_file_name = filename +'_'+ str(i)
                    save_path_file = os.path.join(save_path, out_file_name + '.jpg')
                    cv2.imwrite(save_path_file, img[y:y + h, x:x + w])
                    i=i+1
#注意*处如果包含家目录（home）不能写成~符号代替
#必须要写成"/home"的格式，否则会报错说找不到对应的目录
#读取的目录
read_path("C:/Users/Lenovo/Desktop/shucaishibie/vegetables_tf2.3-master/date/xiaobaicai")
