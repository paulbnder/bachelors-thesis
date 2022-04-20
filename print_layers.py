from climatenet.models import CGNet
from climatenet.utils.utils import Config
config = Config('config.json')
cgnet = CGNet(config)
cgnet.load_model('trained_cgnet')
layers = [module for module in cgnet.network.modules()]

for i in range(len(layers)):
    print("layer %i:" % i)
    print(layers[i])