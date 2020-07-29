# head_shoulder-detection-by-yolov3
本科毕设的时候做的一个人体头肩检测小项目，用了大概3600张图片做fine tune，yolov3主体是用的https://github.com/qqwweee/keras-yolo3 这位大佬的。最近经常有人找我问，就干脆传上来了。代码没有怎么整理过，仅供参考。内容主要是用pyqt5做了个小演示程序，包括本地视频的检测与保存和网络摄像头实时检测，效果演示见：https://www.bilibili.com/video/BV1R4411M7nC 。视频检测部分在这位大佬代码的基础上把画标注框时用的plt换成了cv2，使检测速度略微提升，具体可见下表。在做数据集的时候用的一些小脚本也一起传上来了，也是参考别的大佬写的魔改到能用的0.0

如果这能对您有所帮助，可以点个 ***星*** 
### 文件说明 
大佬写的yolov3里的相关内容就不多赘述  
#### 一、实用工具
1.	XML文件处理相关  
1.1 批量修改XML文件图片路径等（path.py）  
1.2 统计XML个数与标注个数（tongji.py）    
1.3 将测试集的XML转换为txt，方便后续的验证(xml2txt.py)  
2.	网络爬虫（netbug.py）在百度图片上爬取指定关键词图片用于训练。 
3.	anchor box 聚类（anchor box.py）K-means生成新的anchorbox  
4.	图像压缩演示（test111.py）仅作为演示用（写论文的时候水张图进去）  
5.	从视频中截取图片（v2p.py）  
6.  YOLO V3类，在这个里面修改了画框的工具(yolo1.py)  
#### 二、测试相关 
1.检测测试集，并生成detectedbox.txt（main.py）  
2.评价测试集的准确率召回率等及可视化(dect.py)   
#### 三、演示demo
1.包括本地视频的检测与保存和网络摄像头实时检测（video_box.py）  
如果没有网络摄像头，可以在手机上下一个IP摄像头（好像只有安卓版本），可以将手机摄像头内容推成http流  
2.退出按钮的函数好像没写的很好，当时也懒得改了。。。
#### 四、关于绘制框与速度
测试环境：
 CPU: Intel i5 4210H 2.9GHz
 GPU: GTX 850m
 
 目标数  | PLT  | CV2
 ---- | ----- | ------  
 1  | 0.005s | 0.0017s
 3  | 0.016s | 0.0021s
 5  | 0.027s | 0.0024s
 7  | 0.038s | 0.0026s
 9  | 0.046s | 0.0031s
 
 结论：目标数较多时，使用CV2画框有较大提升。（后面用1080Ti也测过，但没记录数据，视频中人数较多时，平均有好几FPS的提升）
 #### 五、预训练模型与测试集
 测试集图片来自INRIA Person Dataset的测试集，手动标注头肩特征。  
 链接：https://pan.baidu.com/s/1cA0RRBRS-jtSBUGbp4NzgQ  
 提取码：fhcs  
 预训练模型记得换anchor(也在网盘中)  
 链接：https://pan.baidu.com/s/1guHLeGDUKlRF3EwWgMzVLQ  
 提取码：fmsy  
 #### 六、测试集上表现
  INRIA Testing Set   |  ----- 
 ---- | ----- 
 precision  | 98.36%  
 recall  | 96.22%  

 #### 七、如果以上内容能对您有所帮助，希望来个 ***星***

 
