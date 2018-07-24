
#! /bin/bash
source venv/bin/activate
# virtualenv is now active.
python extract_features.py --model VGG16 
python train.py 
python evaluate.py