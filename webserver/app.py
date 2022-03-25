#Import necessary libraries
#!/usr/bin/env python3
from flask import Flask, render_template, Response
import numpy as np
import cv2
import tensorflow as tf

#Initialize the Flask app
app = Flask(__name__)
camera = cv2.VideoCapture(0)
# camera = cv2.VideoCapture('rkisp device=/dev/video1 io-mode=4 ! video/x-raw,format=NV12,width=640,height=480,framerate=15/1 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

frame = None

 
def gen_frames():  
    print("gen_frame")

    while True:
        success, frame = camera.read()
        text = pred_img(frame)
        cv2.putText(img=frame, text=text, org=(150, 250), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(0, 255, 0),thickness=3)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    # return Response()

def pred_img(img): 
    # Display the resulting frame
    img = cv2.resize(img,(299,299))
    #Preprocess the image to required size and cast
    input_shape = input_details[0]['shape']
    input_tensor= np.array(np.expand_dims(img,0))

    input_index = interpreter.get_input_details()[0]["index"]
    interpreter.set_tensor(input_index, input_tensor)
    interpreter.invoke()

    output_details = interpreter.get_output_details()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print(output_data)
    pred = np.squeeze(output_data)

    index = np.argmax(pred)

    print(f"{Classes[index]}! with {str(max(pred))}\n")

    text = str(Classes[index]) + "  " + str(max(pred))
    return text

print("Start")
# vid = cv2.VideoCapture(0)

interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
Classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
text = ""




if __name__ == "__main__":
    # try:
    app.run(debug=True)
    # finally:
    #     print("release camera")
    #     camera.release()
