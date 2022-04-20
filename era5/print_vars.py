import numpy as np
import xarray as xr
import netCDF4 as nc
from pylab import *
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

dst = nc.Dataset("TMQ_2000_01_06_sample.nc")

# Dimensionen kopieren
for name, dimension in dst.dimensions.items():
    print(name, dimension)

# print('dst after creating dimensions: ', dst)

# Variabeln kopieren
for name, variable in dst.variables.items():
    print(name, variable, variable.dimensions)
