import re
import numpy as np
import onnxruntime as ort
import onnx
from onnx import helper
from skl2onnx.helpers.onnx_helper import load_onnx_model
from skl2onnx.helpers.onnx_helper import select_model_inputs_outputs
from skl2onnx.helpers.onnx_helper import save_onnx_model
from skl2onnx.helpers.onnx_helper import enumerate_model_node_outputs
import os



BASE_DIR = os.path.abspath(os.path.dirname(__file__))

MODEL_RESHAPE_PATH = os.path.join(BASE_DIR, "model_reshape.onnx")  

model_reshape = ort.InferenceSession(MODEL_RESHAPE_PATH)

MODEL_PATH = os.path.join(BASE_DIR, "model.onnx")  

model = ort.InferenceSession(MODEL_PATH)

input_name = model.get_inputs()[0].name


# Renvoie la prediction + les probabilités
def predict(img):
    result = model.run(None, {input_name: img})

    rounded_result = np.round(result[0][0].tolist(), 4)

    return np.argmax(result), rounded_result


def predict_reshape(img):
    results = model_reshape.run(None, {input_name: img})
    
    return results[0]