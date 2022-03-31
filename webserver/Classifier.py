import classify
import threading
import cv2
import platform 
import numpy as np
if(platform.system() == 'Linux'):
    import tflite_runtime.interpreter as tflite
else:
    import tensorflow as tf


EDGETPU_SHARED_LIB = {
  'Linux': 'libedgetpu.so.1',
  'Darwin': 'libedgetpu.1.dylib',
  'Windows': 'edgetpu.dll'
}[platform.system()]

model_path_tpu="model_edgetpu.tflite"
model_path = "model.tflite"

class Classifier(object):
    def __init__(self):
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.Classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

        self.detection_rate = 5
        self.prev = 0

        print("Initialize tensorflow")
        if(platform.system() == 'Linux'):
            self.interpreter = tflite.Interpreter(model_path_tpu, experimental_delegates=[tflite.load_delegate(EDGETPU_SHARED_LIB)])
            print("Now using TensorFlow with TPU")
        else:
            self.interpreter = tf.lite.Interpreter(model_path)

        self.interpreter.allocate_tensors()

        # Get input and output tensors.
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        print("Done init tensorflow")

    def predict(self, frame):
        # Display the resulting frame
        # img = cv2.resize(img,(299,299))
        #Preprocess the image to required size and cast
        input_shape = self.input_details[0]['shape']
        input_tensor= np.array(np.expand_dims(frame,0))

        input_index = self.interpreter.get_input_details()[0]["index"]
        self.interpreter.set_tensor(input_index, input_tensor)
        self.interpreter.invoke()

        output_details = self.interpreter.get_output_details()
        output_data = self.interpreter.get_tensor(output_details[0]['index'])
        # print(output_data)
        pred = np.squeeze(output_data)
        index = np.argmax(pred)

        classes = classify.get_output(self.interpreter)
        scores = 0
        for c in classes:
            scores += c.score
        # print(pred)
        print(f"{self.Classes[classes[0].id]}! with {classes[0].score}\n")

        # text = str(Classes[index]) + "  " + str(max(pred))
        text = str(self.Classes[index]) + "  " + str("{:.2f}".format(classes[0].score))
        cv2.putText(img=frame, text=text, org=(0, 50), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=3)
        return text, frame

    