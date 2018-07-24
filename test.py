import numpy as np
import h5py
import argparse
from utils import triplet_loss, extract_features
from keras.models import load_model
from sklearn.metrics import pairwise_distances
import cv2

from models import ImageNetFeatureExtractor
from models import get_triplet_network

image_ids = h5py.File("output/embeddings.h5", mode="r")["image_ids"][:]

model = load_model("output/model.h5", custom_objects={"triplet_loss":triplet_loss})
embeddings = h5py.File("output/embeddings.h5", mode="r")["embeddings"][:]

feature_extractor = ImageNetFeatureExtractor(model='vgg16', resize_to=(299, 299))

def get_categories(image):
    image = cv2.resize(cv2.imread(image, 1), (299, 299))
    images = [image, image, image, image]
    test_features = feature_extractor.extract(images)

    test_embeddings = model.predict([test_features, test_features, test_features])
    test_embeddings = test_embeddings[:,:,2]

    test_query = test_embeddings[0]

    distances = pairwise_distances(test_query.reshape(1,-1), embeddings)
    indices = np.argsort(distances)[0][:4]

    images = [str(image_ids[index]) for index in indices]
    return [images, distances]

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i","--image", help="Path to query image")
    args = vars(ap.parse_args())
    print(get_categories(args["image"]))
