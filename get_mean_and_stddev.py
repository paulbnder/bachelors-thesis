import numpy as np
import xarray as xr
import netCDF4 as nc
from pylab import *
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import os

directory = os.fsencode('../data/test_with_vapor_flux')
meanar = []
stdar = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print(filename)
    source_filename = "../data/test_with_vapor_flux/" + filename


    src = nc.Dataset(source_filename)
    m = np.mean(src.variables['VF'][0,:,:])
    s = np.std(src.variables['VF'][0,:,:])
    meanar.append(m)
    stdar.append(s)

print("mean: ", np.mean(meanar))
print("std: ", np.mean(stdar))


