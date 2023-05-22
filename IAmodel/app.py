from flask import Flask
import os

import tensorflow as tf
from tensorflow import keras
"""app = Flask(__name__)"""

model = keras.models.load_model("/Users/sergi/Downloads/saved_model.pb")
print(2)
""""@app.route('/')
def hello_world():  # put application's code here

    return tf.version.VERSION

    print("hello world")

if __name__ == '__main__':
    app.run()
"""