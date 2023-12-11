import numpy 
import joblib 
from PIL import Image
import os
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def load(model: str): 
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    model = joblib.load(current_dir + "/" + model)
    return model

def load_image(img: str): 
    image = Image.open(img)
    image = image.resize((300, 300))
    image = np.array(image) / 255.0
    return image

def predict(model: str, image_path: str): 
    model = load(model)
    image = load_image(image_path)
    image = image.reshape(1, -1)
    out = model.predict_proba(image)
    p = numpy.max(out) * 100
    classe = numpy.argmax(out)
    return out, p, classe