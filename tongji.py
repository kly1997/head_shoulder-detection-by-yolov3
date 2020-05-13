#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author : kly time:2019/4/13

# -*- coding:utf-8 -*-
from xml.dom.minidom import parse
import glob
import time
import json


def readXml(xml_file):
    # 打开文件
    doc = parse(xml_file)
    return doc


def countTags(doc, labels, i, count):
    # 解析XML,根据标签统计个数
    for node in doc.getElementsByTagName("name"):
        tags = node.firstChild.data
        if tags == labels[i]:
            count[i] += 1

    # print(labels[i])
    # print(count)
    return count


if __name__ == '__main__':

    # 标签池
    labels = ['head_shoulder']
    # labels = ['yes_withcloth','no_without']
    xml_paths = glob.glob('C:\project\yolo\Test\Annotations//*.xml')
    # xml数量
    print('xml文件个数为：', len(xml_paths))
    start_time = time.time()

    # 初始化数目
    count = [0] * len(labels)

    # 统计所有xml文件
    for i in range(len(xml_paths)):
        for j in range(len(labels)):
            count = countTags(readXml(xml_paths[i]), labels, j, count)

    # 将标签与数目对应
    label_counts = dict(zip(labels, count))
    # 转成Json，方便以格式化输出
    json_label_counts = json.dumps(label_counts, indent=1)

    end_time = time.time()
    used_time = end_time - start_time
    print('各个标签数为：\n', json_label_counts)
    print('统计所耗时间：%.2fs' % used_time)
