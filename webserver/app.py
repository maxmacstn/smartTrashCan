#Import necessary libraries
#!/usr/bin/env python3
from statistics import mode
from flask import Flask, render_template, Response
import numpy as np
import cv2
import time
import threading
from Classifier import Classifier
from Camera import Camera

#Initialize the Flask app
app = Flask(__name__)
show_frame = None


def processImage():
    global show_frame
    detection_rate = 5
    prev = 0
    while (1):
        time_elapsed = time.time() - prev
        frame = camera.frame
        if time_elapsed > 1./detection_rate and frame is not None:
            prev = time.time()
            frame = cv2.resize(frame,(299,299))
            # show_frame = frame
            text,show_frame = classifier.predict(frame)
            print(text)


def gen_frames():
    global show_frame
    while True:
        ret, buffer = cv2.imencode('.jpg', show_frame)
        out_frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + out_frame + b'\r\n')  # concat frame one by one and show result


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    # return Response()

@app.before_first_request
def initialize():
    pass



if __name__ == "__main__":

    camera = Camera()
    classifier = Classifier()
    detectThread = threading.Thread(target=processImage)
    detectThread.start()
    app.run(debug=True, host="0.0.0.0",  port ="5001", use_reloader=False)
    # Destroy all the windows
    # cv2.destroyAllWindows()


