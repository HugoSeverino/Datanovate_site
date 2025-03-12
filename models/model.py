import numpy as np
import onnxruntime as ort

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.onnx")  

model = ort.InferenceSession(MODEL_PATH)


def predict(img):
    input_name = model.get_inputs()[0].name
    return np.argmax(model.run(None, {input_name: img}))

def predict_probas(img):
    input_name = model.get_inputs()[0].name
    result = model.run(None, {input_name: img})

    rounded_result = np.round(result[0][0].tolist(), 4)
    return rounded_result