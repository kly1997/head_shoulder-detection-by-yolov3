#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author : kly time:2019/4/6

import cv2

vc = cv2.VideoCapture('C://Users\kly\Desktop//v2p//111//5.mp4')  # 读入视频文件
c = 1

if vc.isOpened():  # 判断是否正常打开
    rval, frame = vc.read()
else:
    rval = False

timeF = 60  # 视频帧计数间隔频率

while rval:  # 循环读取视频帧
    rval, frame = vc.read()
    if (c % timeF == 0):  # 每隔timeF帧进行存储操作
        cv2.imwrite('C://Users\kly\Desktop//v2p//222//e' + str(c) + '.jpg', frame)  # 存储为图像
    c = c + 1
    cv2.waitKey(1)
vc.release()

