from threading import Thread
import cv2, time
import platform

class Camera(object):
    def __init__(self):
        print("Init Camera")
        self.frame = None
        if(platform.system() == 'Linux'):
            #camera = cv2.VideoCapture('rkisp device=/dev/video8 io-mode=4 ! videoconvert ! video/x-raw,format=NV12,width=640,height=480,framerate=30/1 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
            #camera = cv2.VideoCapture('rkisp device=/dev/video1 io-mode=4 ! video/x-raw,format=NV12,width=640,height=480,framerate=15/1 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
            self.camera = cv2.VideoCapture("http://localhost:8080/stream?topic=/output/image_raw&type=ros_compressed")
        else:
            self.camera = cv2.VideoCapture(0)
            # self.camera = cv2.VideoCapture("http://192.168.1.14:8080/stream?topic=/output/image_raw&type=ros_compressed")


        self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # set buffer size 
        self.camera.set(cv2.CAP_PROP_FPS, 1)
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):

        while(1):
            success, self.frame = self.camera.read()
            if not success:
                print("Camera read failed:")
                # break
            else:
                self.frame = cv2.resize(self.frame,(299,299))
