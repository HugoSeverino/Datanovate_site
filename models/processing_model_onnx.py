from skl2onnx.helpers.onnx_helper import load_onnx_model
from skl2onnx.helpers.onnx_helper import select_model_inputs_outputs
from skl2onnx.helpers.onnx_helper import save_onnx_model
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model.onnx") 

model = load_onnx_model(MODEL_PATH)

# récupération des sortie intermédiaires voulues via neutron.app
noms_sorties_intermediaires = ["StatefulPartitionedCall/sequential_5_1/max_pooling2d_15_1/MaxPool2d:0", 
                               "StatefulPartitionedCall/sequential_5_1/max_pooling2d_16_1/MaxPool2d:0", 
                               "StatefulPartitionedCall/sequential_5_1/max_pooling2d_17_1/MaxPool2d:0",
                               "StatefulPartitionedCall/sequential_5_1/reshape_5_1/Reshape:0"]

modified_model = select_model_inputs_outputs(
    model, 
    outputs=noms_sorties_intermediaires
)
save_onnx_model(modified_model, os.path.join(BASE_DIR, "other_output_model.onnx"))