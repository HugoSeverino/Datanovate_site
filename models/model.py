import numpy as np
import onnxruntime as ort
import os
# from models import processing_model_onnx



BASE_DIR = os.path.abspath(os.path.dirname(__file__))

MODEL_RESHAPE_PATH = os.path.join(BASE_DIR, "other_output_model.onnx")  

other_output_model = ort.InferenceSession(MODEL_RESHAPE_PATH)

MODEL_PATH = os.path.join(BASE_DIR, "model.onnx")  

model = ort.InferenceSession(MODEL_PATH)

input_name = model.get_inputs()[0].name


# Renvoie la prediction + les probabilités
def predict(img):
    result = model.run(None, {input_name: img})
    rounded_result = np.round(result[0][0].tolist(), 4)

    return np.argmax(result), rounded_result


def predict_reshape(img):
    results = other_output_model.run(None, {input_name: img})
    
    print(results[0].shape)
    print(results[1].shape)
    print(results[2].shape)
    print(results[3].shape)

    return results

