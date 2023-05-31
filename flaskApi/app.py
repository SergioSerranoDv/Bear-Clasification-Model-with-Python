import base64

from flask import Flask, render_template, request
from tensorflow import keras
import cv2
import numpy as np
import os
from flaskApi.config import create_connection
app = Flask(__name__)
#Define path folder to upload the files
upload_folder = "static"
app.config['UPLOAD'] = upload_folder

#Load the bear classification model
path_model = os.path.join(app.config['UPLOAD'], "bearSorter.h5")
model = keras.models.load_model(path_model)

#Define the bear class names
class_names = ["panda", "spectacle", "polar", "pardo", "malayo", "americanBlack"]

#Define a threshold for bear classification confidence
classification_threshold = 0.5

@app.route('/')
def upload_file():  # put application's code here
    return render_template('main.html')
#
connection = create_connection()

def get_info_bear(class_name):
    cursor = connection.cursor()
    select_query = "SELECT * FROM osos WHERE especie = %s"
    cursor.execute(select_query, (class_name,))
    data = cursor.fetchall()
    cursor.close()
    return data


def predict_class(img):
    img = cv2.resize(img, (150, 150))
    image_expanded = np.expand_dims(img, 0)
    result = model.predict(image_expanded)
    class_index = int(np.argmax(result))
    confidence = result[0][class_index]
    if confidence >= classification_threshold:
        class_name = class_names[class_index]
        return class_name
    else:
        return "Unknown"

@app.route('/classification', methods = ['GET','POST'])
def execute_classification():
    if request.method == 'POST':
        file = request.files['file'].read()
        image_array = np.frombuffer(file, np.uint8)
        img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        class_name = predict_class(img)
        data = get_info_bear(class_name)
        image_base64 = base64.b64encode(file).decode('utf-8')
        return render_template('image_render.html', inference=class_name, img=image_base64, data=data)

if __name__ == '__main__':
    app.run()
