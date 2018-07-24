import argparse
from models import get_triplet_network
from utils import extract_features, triplet_loss, get_triplets
import numpy as np
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint
import h5py
import os

features, labels = extract_features("output/features.h5")
print "[+] Finished loading extracted features"

model = get_triplet_network(features.shape)

data = []
for i in range(len(features)*5):
    anchor, positive, negative = get_triplets(features, labels)
    data.append([anchor, positive, negative])

data = np.array(data)
targets = np.zeros(shape=(5000,256,3))

callback = ModelCheckpoint("output/model.h5", period=1, monitor="val_loss")
X_train, X_test, Y_train, Y_test = train_test_split(data, targets)

model.compile(Adam(1e-4), triplet_loss)
model.fit([X_train[:,0], X_train[:,1], X_train[:,2]], Y_train, epochs=10,
          validation_data=([X_test[:,0], X_test[:,1], X_test[:,2]], Y_test),
          callbacks=[callback], batch_size=32)



db = h5py.File("output/embeddings.h5", mode="w")
embeddings = model.predict([features, features, features])
embeddings = embeddings[:,:,2]

embeddingsDB = db.create_dataset("embeddings", shape=embeddings.shape, dtype="float")
embeddingsDB[:] = embeddings

db2 = h5py.File("output/features.h5",mode="r")
image_ids = db2["image_ids"][:]
labels = db2["labels"][:]

imageIDDB = db.create_dataset("image_ids", shape=(len(labels),), dtype=h5py.special_dtype(vlen=unicode))
labelsDB = db.create_dataset("labels", shape=(len(labels),), dtype="int")

imageIDDB[:] = image_ids
labelsDB[:] = labels

db.close()

os.remove("output/features.h5")