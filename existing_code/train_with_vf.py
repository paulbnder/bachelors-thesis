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
    path.join(train_path, 'train_with_vapor_flux'), config)
test = ClimateDatasetLabeled(
    path.join(train_path, 'test_with_vapor_flux'), config)
inference = ClimateDataset(inference_path, config)

cgnet.train(train)


cgnet.save_model('trained_cgnet_vf')
# use a saved model with
# cgnet.load_model('trained_cgnet')


# Evaluation
cgnet.evaluate(test)

# cgnet.network.eval()

# class_masks = cgnet.predict(inference)  # masks with 1==TC, 2==AR
# class_masks.to_netcdf("class_masks.nc")
# event_masks = track_events(class_masks)  # masks with event IDs
# event_masks.to_netcdf("event_masks.nc")

#analyze_events(event_masks, class_masks, 'results/')
#visualize_events(event_masks, inference, 'pngs/')
