from climatenet.utils.data import ClimateDatasetLabeled, ClimateDataset
from climatenet.models import CGNet
from climatenet.utils.utils import Config
from climatenet.track_events import track_events
from climatenet.analyze_events import analyze_events
from climatenet.visualize_events import visualize_events

import torch
import torch.nn as nn
import torch.nn.functional as F
from climatenet.modules import *
from climatenet.utils.data import ClimateDataset, ClimateDatasetLabeled
from climatenet.utils.losses import jaccard_loss
from climatenet.utils.metrics import get_cm, get_iou_perClass
from torch.optim import Adam
from torch.utils.data import DataLoader
from tqdm import tqdm
import numpy as np
import xarray as xr

import os
from os import path

config = Config('config.json')
cgnet = CGNet(config)

train_path = '../data'
inference_path = '../data/inference'

train = ClimateDatasetLabeled(
    path.join(train_path, 'train_regional_windows'), config)
test = ClimateDatasetLabeled(
    path.join(train_path, 'test_regional_all'), config)
inference = ClimateDataset(inference_path, config)

# Uncomment to train a new model
cgnet.train(train)
#cgnet.save_model('trained_cgnet')

# Uncomment to load a saved model
#cgnet.load_model('trained_cgnet')

# Uncomment to evaluate on test set
cgnet.evaluate(test)

# # Create segmentation masks for inference dataset
# class_masks = cgnet.predict(inference)  # masks with 1==TC, 2==AR
# class_masks.to_netcdf("class_masks_bottommedium.nc")