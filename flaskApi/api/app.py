from flask import Flask, render_template, request
from tensorflow import keras
import cv2
import numpy as np
import os
from config import create_connection
app = Flask(__name__)

upload_folder = "static"

app.config['UPLOAD'] = upload_folder

@app.route('/')
def upload_file():  # put application's code here
    return render_template('main.html')

connection = create_connection()

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

    if clase == "0":
        class_name = "panda"
    elif clase == "1":
        class_name = "spectacle"
    elif clase == "2":
        class_name = "polar"
    elif clase == "3":
        class_name = "pardo"
    elif clase == "4":
        class_name = "malayo"
    else:
        class_name = "americanBlack"
    return class_name

@app.route('/classification', methods = ['GET','POST'])
def execute_classification():
    if request.method == 'POST':
        file = request.files['file']
        file_name = file.filename
        file.save(os.path.join("../static", file_name))
        image = os.path.join(app.config['UPLOAD'], file_name)
        path_model = "/Users/sergi/Documents/bearSorter.h5"
        class_name = predict_class(path_model, image)
        data = get_info(class_name)
        return render_template('image_render.html', inference=class_name, img=image, data=data)
    return render_template('image_render.html')

if __name__ == '__main__':
    app.run()
