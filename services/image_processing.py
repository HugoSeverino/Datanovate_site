import base64
from io import BytesIO
from PIL import Image
import numpy as np

def encoded_to_array(encoded: str) -> np.ndarray:

    image_data = base64.b64decode(encoded)
    img = Image.open(BytesIO(image_data))
    img.save("static/img/chiffre.png")
    img = img.resize((28,28), Image.NEAREST)
    img = img.convert("1")
    img.save("static/img/chiffre_norm.png")

    enlarged_image = resize_scale(img, 5)
    enlarged_image.save("static/img/enlarged_chiffre_norm.png")

    np_img = np.array(img, dtype=np.float32)
    
    np_img = np_img.reshape(1, 28, 28, 1)
    
    return np_img


def save_from_array(image, file):
    from PIL import Image
    import numpy as np

    img = Image.fromarray(image, mode="L")
    enlarged_image = img.resize((280, 280))  # exemple d’agrandissement

    path = os.path.join("static", "img", file)
    enlarged_image.save(path)



def resize_scale(img: Image, scale_factor: int) -> Image:
    # Calculer la nouvelle taille
    new_size = (img.size[0] * scale_factor, img.size[1] * scale_factor)

    # Agrandir l'image en utilisant la méthode 'NEAREST' pour conserver les pixels nets
    enlarged_image = img.resize(new_size, Image.NEAREST)

    return enlarged_image
