import numpy as np
import tensorflow as tf
import cv2

def pred_img(img):
    print("button activate")
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
    pred = np.squeeze(output_data)

    index = np.argmax(pred)

    print(f"{Classes[index]}! with {str(max(pred))}\n")

    text = str(Classes[index]) + "  " + str(max(pred))
    return text

print("Start")
vid = cv2.VideoCapture(0)

interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
Classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
text = ""
while(True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    cv2.putText(img=frame, text=text, org=(150, 250), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(0, 255, 0),thickness=3)
    cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('p'):
    text = pred_img(frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
