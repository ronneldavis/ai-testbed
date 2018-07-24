import argparse
import numpy as np
from models import ImageNetFeatureExtractor
from utils import dump_features

ap = argparse.ArgumentParser()
ap.add_argument("-m","--model", help="(VGG16, VGG19, Inceptionv3, ResNet50)", default="InceptionV3")

args = vars(ap.parse_args())

feature_extractor = ImageNetFeatureExtractor(model=args["model"], resize_to=(299, 299))
print "[+] Successfully loaded pre-trained model"

dump_features("dataset", labels=(np.arange(1000)/4)+1,
              hdf5_path="output/features.h5", feature_extractor=feature_extractor,
              image_formats=("jpg","png"))