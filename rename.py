import numpy as np
import cv2
import os

def read_path(file_pathname):
    #遍历该目录下的所有图片文件
    i=1
    for filename in os.listdir(file_pathname):
        print(filename)
        img = cv2.imread(file_pathname+'/'+filename)
        save_path = "C:/Users/Lenovo/Desktop/xiaoqingcaiyuantu"
        out_file_name ='xiaoqingcai'+'_'+ str(i)
        save_path_file = os.path.join(save_path, out_file_name + '.jpg')
        cv2.imwrite(save_path_file, img)
        i=i+1
#注意*处如果包含家目录（home）不能写成~符号代替
#必须要写成"/home"的格式，否则会报错说找不到对应的目录
#读取的目录
read_path("C:/Users/Lenovo/Desktop/datebase/xiaoqingcai")
