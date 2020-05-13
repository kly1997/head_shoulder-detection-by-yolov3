##修改xml文件中的path，与实际数据路径对应
##authorleo

# coding=utf-8
import os
import os.path
import xml.dom.minidom

file_path = 'VOCdevkit\VOC2007\Annotations'
files = os.listdir(file_path)  # 得到文件夹下所有文件名称
s = []
for xmlFile in files:  # 遍历文件夹
    if not os.path.isdir(xmlFile):  # 判断是否是文件夹,不是文件夹才打开
        print(xmlFile)
        # xml文件读取操作
        # 将获取的xml文件名送入到dom解析
        dom = xml.dom.minidom.parse(os.path.join(file_path, xmlFile))  ###最核心的部分,路径拼接,输入的是具体路径
        root = dom.documentElement
        # 获取标签对path之间的值
        original_path = root.getElementsByTagName('path')
        original_folder = root.getElementsByTagName('folder')
        original_name = root.getElementsByTagName('filename')
        original_label = root.getElementsByTagName('name')
        # 原始信息
        p0 = original_path[0]
        f0 = original_folder[0]
        n0 = original_name[0]

        path0 = p0.firstChild.data   #原始路径

        print(path0)
        # 修改
        o_path, jpg_name = os.path.split(path0)  #获取图片名
        modify_path=file_path+''+jpg_name   #修改后path
        p0.firstChild.data = 'D:\work//new\VOCdevkit\VOC2007\JPEGImages\\' + xmlFile.split('.')[0] + '.jpg'
        f0.firstChild.data = 'Annotations'
        n0.firstChild.data = xmlFile.split('.')[0] + '.jpg'

#        a = int(xmlFile.split('.')[0])
#        if (1019 <= a and a <= 1055) or (1195 <= a and a <= 1199) or (946 <= a and a <= 985):
#            width = root.getElementsByTagName('width')
#            for i in range(len(width)):
#                width[i].firstChild.data = 480
#            height = root.getElementsByTagName('height')
#            for i in range(len(height)):
#                height[i].firstChild.data = 640
#        else:
#            width = root.getElementsByTagName('width')
#            for i in range(len(width)):
#                width[i].firstChild.data = 640
#            height = root.getElementsByTagName('height')
#            for i in range(len(height)):
#                height[i].firstChild.data = 480
#        depth = root.getElementsByTagName('depth')
#        for i in range(len(depth)):
#            if depth[i].firstChild.data == '1':
#                depth[i].firstChild.data = '3'
#                print('b&w')
#            else:
#                print('n_c')

        #name = root.getElementsByTagName('name')
        #for i in range(len(name)):
        #    print(name[i].firstChild.data)
        #   if name[i].firstChild.data == 'person':
        #       name[i].firstChild.data = 'head_shoulder'
        #        print('head_shoulder')
        #        print(name[i].firstChild.data)

        # 保存修改到xml文件中
        with open(os.path.join(file_path, xmlFile), 'w') as fh:
            dom.writexml(fh)
            print('修改path OK!')
