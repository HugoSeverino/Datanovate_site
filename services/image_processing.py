import base64
from io import BytesIO
from PIL import Image
import numpy as np
import os 
def encoded_to_array(encoded: str) -> np.ndarray:
    image_data = base64.b64decode(encoded)
    img = Image.open(BytesIO(image_data))
    img = img.resize((28,28), Image.NEAREST)
    img = img.convert("L")  # niveaux de gris (0-255)

    # Conversion en numpy array + normalisation
    np_img = np.array(img, dtype=np.float32) / 255.0
    np_img = np_img.reshape(1, 1, 28, 28)  # channel first, comme MNIST/PyTorch

    # Image agrandie pour l'affichage
    enlarged_image = resize_scale(img, 5)
    buffered = BytesIO()
    enlarged_image.save(buffered, format="PNG")
    enlarged_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Debug
    print("DEBUG - Image shape :", np_img.shape)
    print("DEBUG - Image dtype :", np_img.dtype)
    print("DEBUG - Min pixel value :", np.min(np_img))
    print("DEBUG - Max pixel value :", np.max(np_img))
    print("DEBUG - Mean pixel value :", np.mean(np_img))

    return np_img, enlarged_base64



def array_to_base64(image: np.ndarray, scale_factor: int = 3) -> None:
    # Conversion en Image pour redimensionnement

    img = Image.fromarray(image, mode="L")
    enlarged_image = resize_scale(img, scale_factor)
    

    buffered = BytesIO() # Crée un "fichier temporaire" vide en mémoire
    enlarged_image.save(buffered, format="PNG") # sauvegarde l'image dans ce dernier sous format png
    enlarged_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8') # lit l'image png, l'encode en base64_str pour json

    return enlarged_base64





def resize_scale(img: Image, scale_factor: int) -> Image:
    # Calculer la nouvelle taille
    new_size = (img.size[0] * scale_factor, img.size[1] * scale_factor)

    # Agrandir l'image en utilisant la méthode 'NEAREST' pour conserver les pixels nets
    enlarged_image = img.resize(new_size, Image.NEAREST)

    return enlarged_image
