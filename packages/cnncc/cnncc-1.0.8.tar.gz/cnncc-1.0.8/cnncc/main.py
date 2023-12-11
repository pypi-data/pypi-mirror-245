from .models.resnet import model as resnet
import argparse
from .utils import pretty_print
from .models.logreg import logreg
    
def predict(model: str, image_path: str): 
    if model == "ResNet":
        print("Predicting for model: ResNet")
        model = resnet.load_pretrained_model()
        image = resnet.prepare_img_for_inference(image_path)
        out, p, classe = resnet.inference(model, image)
        
    elif model == "LR-1": 
        print("Predicting for model: Logistic Regression (raw)")
        out, p, classe = logreg.predict("model_raw_66.joblib", image_path)
    elif model == "LR-2": 
        print("Predicting for model: Logistic Regression (+ upsampling)")
        out, p, classe = logreg.predict("model_2_64.joblib", image_path)
    elif model == "LR-3": 
        print("Predicting for model: Logistic Regression (+ data augmentation)")
        out, p, classe = logreg.predict("model_12_61.joblib", image_path)
    
    return out, p, classe

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--image", type=str, required=True)
    args = parser.parse_args()
    out, p, classe = predict(args.model, args.image)
    pretty_print(out, p, classe)
    
# if __name__ == "__main__":
#     main()