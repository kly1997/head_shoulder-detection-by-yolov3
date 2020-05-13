#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author : kly time:2019/4/15

# coding=utf-8
import os
import sys
import xml.etree.ElementTree as ET
import glob

def xml_to_txt(indir):
    os.chdir(indir)
    annotations = os.listdir('.')
    annotations = glob.glob(str(annotations) + '*.xml')

    for i, file in enumerate(annotations):
        with open('F:\DEEPL\yolo\Test//result\groundtruthbox1.txt', "a") as f_w:
            f_w.write(file.split('.')[0] + '.jpg' + '\n')
        # actual parsing
        in_file = open(file)
        tree = ET.parse(in_file)
        root = tree.getroot()
        print(file)
        i=0
        for object in root.iter('object'):
            i += 1
        with open('F:\DEEPL\yolo\Test//result\groundtruthbox1.txt', "a") as f_w:
            f_w.write(str(i) + '\n')
        for obj in root.iter('object'):
            current = list()
            name = obj.find('name').text
            xmlbox = obj.find('bndbox')
            xn = xmlbox.find('xmin').text
            xx = xmlbox.find('xmax').text
            yn = xmlbox.find('ymin').text
            yx = xmlbox.find('ymax').text
            # print xn
            width = int(xx) - int(xn)
            print(width)
            height = int(yx) - int(yn)
            print(height)

            with open('F:\DEEPL\yolo\Test//result\groundtruthbox1.txt', "a") as f_w:
                f_w.write(xn + ' ' + yn + ' ' + str(width) + ' ' + str(height) + ' '+'1')
                f_w.write('\n')


indir = 'F:\DEEPL\yolo\Test//annotations'  # xml目录

xml_to_txt(indir)