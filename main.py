#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author : kly time:2019/4/14
import yolo
import os
from PIL import Image
import glob
if __name__ == '__main__':
    yolo = yolo.YOLO()
    path = "D:\work//new\Test\INA-T//*.jpg"
    outdir = "D:\work//new\Test\out"
    for jpgfile in glob.glob(path):
        img = Image.open(jpgfile)
        num = jpgfile[-10: -4]
        print(num)
        img = yolo.detect_image(img, num)
        #img.save(os.path.join(outdir, os.path.basename(jpgfile)))
        print('ok')
    yolo.close_session()
