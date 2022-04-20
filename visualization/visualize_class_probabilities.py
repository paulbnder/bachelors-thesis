import torch
import matplotlib.pyplot as plt
from climatenet.models import CGNet
import numpy as np
from torch.utils.data import DataLoader
from climatenet.models import CGNet
from climatenet.utils.data import ClimateDataset, ClimateDatasetLabeled
from climatenet.utils.utils import Config
from tqdm import tqdm


config = Config('config.json')
cgnet = CGNet(config)
cgnet.load_model('trained_cgnet')
inference_path = '../data/inference'
inference = ClimateDataset(inference_path, config)

collate = ClimateDataset.collate
loader = DataLoader(inference, batch_size=cgnet.config.pred_batch_size, collate_fn=collate)
epoch_loader = tqdm(loader)

for batch in epoch_loader:

    features = torch.tensor(batch.values).cuda()
    model_out =  torch.softmax(cgnet.network(features), 1)
    class_probabilities = np.squeeze(model_out)
    class_probabilities.cpu().detach().numpy()
    print("model_out.shape: ",class_probabilities[0,:,:].shape)
    fig, ax = plt.subplots()
    cax = ax.imshow(np.flipud(class_probabilities[0,:,:].cpu().detach().numpy()))
    plt.colorbar(cax,
                label='Prediction Probability', shrink=1, ax=[ax], location='bottom')
    ax.set_title("Probabilities for class BG")
    fig.savefig("class_prob_BG.png")