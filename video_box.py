import time
import sys
import numpy

from timeit import default_timer as timer
import PyQt5.sip
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from cv2 import *
from yolo1 import YOLO
from PyQt5.QtWidgets import *
from PIL import Image


class VideoBox(QWidget):

    VIDEO_TYPE_OFFLINE = 0
    VIDEO_TYPE_REAL_TIME = 1

    STATUS_INIT = 0
    STATUS_PLAYING = 1
    STATUS_PAUSE = 2

    video_url = ""

    def __init__(self, video_url="", video_type=VIDEO_TYPE_OFFLINE, auto_play=False):
        self.yolo = YOLO()
        QWidget.__init__(self)
        self.video_url = video_url
        self.video_type = video_type  # 0: offline  1: realTime
        self.auto_play = auto_play
        self.status = self.STATUS_INIT  # 0: init 1:playing 2: pause

        # 组件展示
        self.pictureLabel = QLabel()
        init_image = QPixmap("cat.jpeg").scaled(720, 480)
        self.pictureLabel.setPixmap(init_image)

        # self.playButton = QPushButton()
        # self.playButton.clicked.connect(self.switch_video)
        self.playButton = QPushButton('save', self)
        self.openButton = QPushButton('webCam', self)
        self.transButton = QPushButton('trans', self)
        self.exitButton = QPushButton('exit', self)

        self.playButton.clicked.connect(self.switch_video)
        self.openButton.clicked.connect(self.openSlot)
        self.transButton.clicked.connect(self.transSlot)
        self.exitButton.clicked.connect(self.closeSlot)

        layout = QGridLayout(self)
        layout.addWidget(self.playButton, 4, 1, 1, 1)
        layout.addWidget(self.openButton, 4, 2, 1, 1)
        layout.addWidget(self.transButton, 4, 3, 1, 1)
        layout.addWidget(self.exitButton, 4, 4, 1, 1)
        layout.addWidget(self.pictureLabel, 0, 1, 3, 4)
        #control_box = QHBoxLayout()
        # control_box.setContentsMargins(0, 0, 0, 0)
        # control_box.addWidget(self.playButton)
        # layout = QVBoxLayout()
        #layout.addWidget(self.pictureLabel, 0, 1, 3, 4)
        #layout.addLayout(control_box)

        self.setLayout(layout)

        # timer 设置
        self.timer = VideoTimer()
        self.timer.timeSignal.signal[str].connect(self.show_video_images)

        # video 初始设置
        self.playCapture = VideoCapture()
        if self.video_url != "":
            self.set_timer_fps()
            if self.auto_play:
                self.switch_video()
            # self.videoWriter = VideoWriter('*.mp4', VideoWriter_fourcc('M', 'J', 'P', 'G'), self.fps, size)

    def reset(self):
        self.timer.stop()
        self.playCapture.release()
        self.status = VideoBox.STATUS_INIT
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def set_timer_fps(self):
        self.playCapture.open(self.video_url)
        fps = self.playCapture.get(CAP_PROP_FPS)
        self.timer.set_fps(fps)
        self.playCapture.release()

    def set_video(self, url, video_type=VIDEO_TYPE_OFFLINE, auto_play=False):
        self.reset()
        self.video_url = url
        self.video_type = video_type
        self.auto_play = auto_play
        self.set_timer_fps()
        if self.auto_play:
            self.switch_video()

    def play(self):
        if self.video_url == "" or self.video_url is None:
            return
        if not self.playCapture.isOpened():
            self.playCapture.open(self.video_url)
        self.timer.start()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.status = VideoBox.STATUS_PLAYING

    def stop(self):
        if self.video_url == "" or self.video_url is None:
            return
        if self.playCapture.isOpened():
            self.timer.stop()
            if self.video_type is VideoBox.VIDEO_TYPE_REAL_TIME:
                self.playCapture.release()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.status = VideoBox.STATUS_PAUSE

    def re_play(self):
        if self.video_url == "" or self.video_url is None:
            return
        self.playCapture.release()
        self.playCapture.open(self.video_url)
        self.timer.start()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.status = VideoBox.STATUS_PLAYING


    def openSlot(self):
        value, ok = QInputDialog.getText(self, "web_cam", "请输相机地址:", QLineEdit.Normal,
                                         "http://admin:admin@192.168.43.1:8081")
        if value == '':
            vid = cv2.VideoCapture(0)
        else:
            vid = cv2.VideoCapture(value)
        if not vid.isOpened():
            raise IOError("Couldn't open webcam or video")
        accum_time = 0
        curr_fps = 0
        fps = "FPS: ??"
        prev_time = timer()
        while True:
            return_value, frame = vid.read()
            image = Image.fromarray(frame)
            image = self.yolo.detect_image(image, 1)
            # result = cv2.cvtColor(numpy.asarray(image), cv2.COLOR_RGB2BGR)
            result = numpy.asarray(image)
            curr_time = timer()
            exec_time = curr_time - prev_time
            prev_time = curr_time
            accum_time = accum_time + exec_time
            curr_fps = curr_fps + 1
            if accum_time > 1:
                accum_time = accum_time - 1
                fps = "FPS: " + str(curr_fps)
                curr_fps = 0
            cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.50, color=(255, 0, 0), thickness=1)
            # result = cv2.resize(result, (500, 500), interpolation=cv2.INTER_CUBIC)
            # height, width = result.shape[:2]
            # if result.ndim == 3:
            #     rgb = cvtColor(result, COLOR_BGR2RGB)
            # elif result.ndim == 2:
            #     rgb = cvtColor(result, COLOR_GRAY2BGR)
            # temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
            # temp_pixmap = QPixmap.fromImage(temp_image)
            # # temp_pixmap = cv2.resize(temp_pixmap, (500, 500), interpolation=cv2.INTER_CUBIC)
            # self.pictureLabel.setPixmap(temp_pixmap)
            # result = cv2.resize(result, (1, 1), interpolation=cv2.INTER_CUBIC)
            cv2.imshow("result", result)
            # cv2.imshow("result", result)
            # if isOutput:
            #     out.write(result)
            #     print('ok')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.yolo.close_session()


    def transSlot(self):
        fileName, tmp = QFileDialog.getOpenFileName(self, 'Open Video', 'video', '*')
        if fileName is '':
            return
        if fileName.split('.')[-1] == ('jpg'or 'png' or 'jpeg'):
            image = Image.open(fileName)
            frame = self.yolo.detect_image(image, 1)
            frame = cv2.cvtColor(numpy.asarray(frame), cv2.COLOR_RGB2BGR)
            # self.yolo.close_session()
            height, width = frame.shape[:2]
            if frame.ndim == 3:
                rgb = cvtColor(frame, COLOR_BGR2RGB)
            elif frame.ndim == 2:
                rgb = cvtColor(frame, COLOR_GRAY2BGR)
            temp_image = []
            temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
            temp_pixmap = QPixmap.fromImage(temp_image)
            self.pictureLabel.setPixmap(temp_pixmap)
        else:
            print(fileName)
            vid = cv2.VideoCapture(fileName)
            if not vid.isOpened():
                raise IOError("Couldn't open webcam or video")
            # video_FourCC    = int(vid.get(cv2.CAP_PROP_FOURCC))
            # video_FourCC = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            # video_fps = vid.get(cv2.CAP_PROP_FPS)
            # video_size = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
            #               int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            # isOutput = True if output_path != "" else False
            # if isOutput:
            #     print("!!! TYPE:", type(output_path), type(video_FourCC), type(video_fps), type(video_size))
            #     print("!!! value:", output_path, video_FourCC, video_fps, video_size)
            #     out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size)                fin_time = timer()
            accum_time = 0
            curr_fps = 0
            fps = "FPS: ??"
            prev_time = timer()
            while True:
                s_time = timer()
                return_value, frame = vid.read()
                image = Image.fromarray(frame)
                result = self.yolo.detect_image(image, 1)
                s1_time = timer()
                # result = cv2.cvtColor(numpy.asarray(image), cv2.COLOR_RGB2BGR)
                #result = numpy.asarray(image)
                curr_time = timer()
                exec_time = curr_time - prev_time
                prev_time = curr_time
                accum_time = accum_time + exec_time
                curr_fps = curr_fps + 1
                if accum_time > 1:
                    accum_time = accum_time - 1
                    fps = "FPS: " + str(curr_fps)
                    curr_fps = 0
                cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                             fontScale=0.50, color=(255, 0, 0), thickness=1)
                #result = cv2.resize(result, (500, 500), interpolation=cv2.INTER_CUBIC)
                # height, width = result.shape[:2]
                # if result.ndim == 3:
                #     rgb = cvtColor(result, COLOR_BGR2RGB)
                # elif result.ndim == 2:
                #     rgb = cvtColor(result, COLOR_GRAY2BGR)
                # temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
                # temp_pixmap = QPixmap.fromImage(temp_image)
                # # temp_pixmap = cv2.resize(temp_pixmap, (500, 500), interpolation=cv2.INTER_CUBIC)
                # self.pictureLabel.setPixmap(temp_pixmap)
                # result = cv2.resize(result, (1, 1), interpolation=cv2.INTER_CUBIC)

                cv2.imshow("result", result)
                s2_time = timer()
                # cv2.imshow("result", result)
                # if isOutput:
                #     out.write(result)
                #     print('ok')

                print(s2_time - s1_time)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                      break

            self.yolo.close_session()


    def closeSlot(self):
        exit()


    def show_video_images(self):
        if self.playCapture.isOpened():
            success, frame = self.playCapture.read()
            if success:
                height, width = frame.shape[:2]
                if frame.ndim == 3:
                    rgb = cvtColor(frame, COLOR_BGR2RGB)
                elif frame.ndim == 2:
                    rgb = cvtColor(frame, COLOR_GRAY2BGR)

                temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
                temp_pixmap = QPixmap.fromImage(temp_image)
                self.pictureLabel.setPixmap(temp_pixmap)
            else:
                print("read failed, no frame data")
                success, frame = self.playCapture.read()
                if not success and self.video_type is VideoBox.VIDEO_TYPE_OFFLINE:
                    print("play finished")  # 判断本地文件播放完毕
                    self.reset()
                    self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
                return
        else:
            print("open file or capturing device error, init again")
            self.reset()

    def switch_video(self):
        fileName, tmp = QFileDialog.getOpenFileName(self, 'Open Video', 'video', '*')
        if fileName is '':
            return
        print(fileName)
        dir = QFileDialog.getExistingDirectory(self,
                                               "选取文件夹",
                                               "C:/")  # 起始路径
        output_path =dir+'/new_'+fileName.split('/')[-1]
        print(output_path)
        vid = cv2.VideoCapture(fileName)
        if not vid.isOpened():
            raise IOError("Couldn't open webcam or video")
        # video_FourCC    = int(vid.get(cv2.CAP_PROP_FOURCC))
        video_FourCC = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video_fps = vid.get(cv2.CAP_PROP_FPS)
        video_size = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                      int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        isOutput = True if output_path != "" else False
        if isOutput:
            print("!!! TYPE:", type(output_path), type(video_FourCC), type(video_fps), type(video_size))
            print("!!! value:", output_path, video_FourCC, video_fps, video_size)
            out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size)
        accum_time = 0
        curr_fps = 0
        fps = "FPS: ??"
        prev_time = timer()
        while True:
            return_value, frame = vid.read()
            image = Image.fromarray(frame)
            result = self.yolo.detect_image(image, 1)
            # result = np.asarray(image)
            curr_time = timer()
            exec_time = curr_time - prev_time
            prev_time = curr_time
            accum_time = accum_time + exec_time
            curr_fps = curr_fps + 1
            if accum_time > 1:
                accum_time = accum_time - 1
                fps = "FPS: " + str(curr_fps)
                curr_fps = 0
            cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.50, color=(255, 0, 0), thickness=2)
            # cv2.namedWindow("result", cv2.WINDOW_NORMAL)
            cv2.imshow("result", result)
            if isOutput:
                out.write(result)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.yolo.close_session()


class Communicate(QObject):

    signal = pyqtSignal(str)


class VideoTimer(QThread):

    def __init__(self, frequent=20):
        QThread.__init__(self)
        self.stopped = False
        self.frequent = frequent
        self.timeSignal = Communicate()
        self.mutex = QMutex()

    def run(self):
        with QMutexLocker(self.mutex):
            self.stopped = False
        while True:
            if self.stopped:
                return
            self.timeSignal.signal.emit("1")
            time.sleep(1 / self.frequent)

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True

    def is_stopped(self):
        with QMutexLocker(self.mutex):
            return self.stopped

    def set_fps(self, fps):
        self.frequent = fps




if __name__ == "__main__":
    mapp = QApplication(sys.argv)
    mw = VideoBox()
    #mw.set_video("F:\DEEPL\yolo\play\pyqt5-opencv-video-master//resource//video.mp4", VideoBox.VIDEO_TYPE_OFFLINE, False)
    mw.show()
    sys.exit(mapp.exec_())
