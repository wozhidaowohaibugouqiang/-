# noinspection PyUnresolvedReferences
import numpy  as np # 1
# noinspection PyUnresolvedReferences
import argparse  # 2
import cv2  # 4
import os
# noinspection PyUnresolvedReferences
import math
file_pathname = ('C:/Users/Lenovo/Desktop/xiangcai')#读取文件路径
for filename in os.listdir(file_pathname):
    img = cv2.imread(file_pathname+'/'+filename)
    for k in range(8):
        x=k*45
        h, w = img.shape[:2]
        center = (w / 2, h / 2)
        scale = 1.0
        angle =x
        # 2.1获取M矩阵
        # """
        # M矩阵
        # [
        # cosA -sinA (1-cosA)*centerX+sinA*centerY
        # sinA cosA  -sinA*centerX+(1-cosA)*centerY
        # ]
        # """
        M = cv2.getRotationMatrix2D(center, angle, scale)
        # 2.2 新的宽高，radians(angle) 把角度转为弧度 sin(弧度)
        new_H = int(w * math.fabs(math.sin(math.radians(angle))) + h * math.fabs(math.cos(math.radians(angle))))
        new_W = int(h * math.fabs(math.sin(math.radians(angle))) + w * math.fabs(math.cos(math.radians(angle))))
        # 2.3 平移
        M[0, 2] += (new_W - w) / 2
        M[1, 2] += (new_H - h) / 2
        rotate = cv2.warpAffine(img, M, (new_W, new_H), borderValue=(0, 0, 0))
        save_path = r'C:/Users/Lenovo/Desktop/xiangcai2'#保存文件路径
        out_file_name = filename+'_' + str(k)
        save_path_file = os.path.join(save_path, out_file_name + '.jpg')
        cv2.imwrite(save_path_file, rotate)
        k=k+1


