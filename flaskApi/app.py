from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow import keras
import cv2
import numpy as np
import os
import psycopg2
import config
from config import create_connection
app = Flask(__name__)

upload_folder = "static"

app.config['UPLOAD'] = upload_folder

@app.route('/')
def upload_file():  # put application's code here
    return render_template('main.html')

connection = create_connection()
if connection is None:
    print("Error to connect with postgreSql")
else:
    print("successfull connection")

def get_info(class_name):
    cursor = connection.cursor()
    select_query = "SELECT * FROM osos WHERE especie = %s"
    cursor.execute(select_query, (class_name,))
    data = cursor.fetchall()
    cursor.close()
    return data


def predict_class(path_model, image):
    img = cv2.imread(image)
    img = cv2.resize(img, (150, 150))
    image_expanded = np.expand_dims(img, 0)
    model = keras.models.load_model(path_model)
    result = model.predict(image_expanded)
    clase = str(int(np.argmax(result)))

    if clase == "1":
        class_name = "spectacle"
    else:
        class_name = "panda"
    return class_name

@app.route('/classification', methods = ['GET','POST'])
def execute_classification():
    if request.method == 'POST':
        file = request.files['file']
        file_name = file.filename
        file.save(os.path.join("static" , file_name))
        image = os.path.join(app.config['UPLOAD'], file_name)
        path_model = "/Users/sergi/Documents/ososModel.h5"
        class_name = predict_class(path_model, image)
        data = get_info(class_name)
        return render_template('image_render.html', inference=class_name, img=image, data=data)
    return render_template('image_render.html')

if __name__ == '__main__':
    app.run()
