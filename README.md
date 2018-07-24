#AI testbed

This is a toyy broject that performs reverse image search. Given a test image, it finds other images in the dataset that either match it or are similar. The neural network is written in Keras with a Tensorflow backend.

##Prepping your environment

Download the ukbench dataset and rename the folder to dataset from https://archive.org/details/ukbench and add it to the project folder. You can use any dataset you want as the training set.

Make sure you have pip and virtualenv installed. In a terminal run ``virtualenv venv `` followed by `` pip install -r requirements.txt `` to install all the requirements. You are now ready to train your dataset. 

## Training
You may have to give the training script executable permissions. You can do that by entering ``chmod +x train.sh``. To run the training script, run ``./train.sh``. This will train your network and give the accuracy following an evaluation.

##Testing
You can now test the dataset with images of your choosing. ENter ``python test.py --image test.jpg`` to run a saomple testcase. 