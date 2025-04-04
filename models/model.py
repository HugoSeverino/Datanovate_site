from typing import Tuple
import numpy as np
import onnxruntime as ort
import os
# from models import processing_model_onnx



BASE_DIR = os.path.abspath(os.path.dirname(__file__))


MODEL_RESHAPE_PATH = os.path.join(BASE_DIR, "other_output_model.onnx")  
options = ort.SessionOptions()
#options.optimized_model_filepath = MODEL_RESHAPE_PATH
other_output_model = ort.InferenceSession(MODEL_RESHAPE_PATH, sess_options=options) # sess_options enlève un warning inutile


MODEL_PATH = os.path.join(BASE_DIR, "model.onnx")
model = ort.InferenceSession(MODEL_PATH)

input_name = model.get_inputs()[0].name
print("DEBUG - Input name:", input_name)
print("DEBUG - Model input shape:", model.get_inputs()[0].shape)
print("DEBUG - Model input type:", model.get_inputs()[0].type)

# Renvoie la prediction + les probabilités
def predict(img: np.ndarray) -> Tuple[np.uint8, np.ndarray]:
    result = model.run(None, {input_name: img})
    rounded_result = np.round(result[0][0].tolist(), 4)

    return np.argmax(result), rounded_result


def predict_reshape(img: np.ndarray) -> list[np.ndarray]:
    results = other_output_model.run(None, {input_name: img})

    return results

