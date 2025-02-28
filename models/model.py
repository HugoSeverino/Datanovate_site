import numpy as np
import tensorflow as tf
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.h5")  

model = tf.keras.models.load_model(MODEL_PATH)

def predict(img):
    return np.argmax(model.predict(img))