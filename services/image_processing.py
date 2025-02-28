import base64
from io import BytesIO
from PIL import Image
import numpy as np

def encoded_to_array(encoded):

    image_data = base64.b64decode(encoded)
    img = Image.open(BytesIO(image_data))
    img.save("static/img/chiffre.png")
    img = img.resize((28,28), Image.NEAREST)
    img = img.convert("1")
    img.save("static/img/chiffre_norm.png")

    np_img = np.array(img)
    np_img = np_img.reshape(1, 28, 28, 1)
    print(np_img)
    return np_img

