import numpy as np
import xarray as xr
import netCDF4 as nc
from pylab import *
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import os


src = nc.Dataset("TMQ_2000_01_06_sample.nc")
src2 = nc.Dataset("data-2000-01-06-01-1_1.nc")


# Dimensionen kopieren
for name, dimension in src.dimensions.items():
    print('dimension: ', name, dimension)

# print('dst after creating dimensions: ', dst)

# Variabeln kopieren
for name, variable in src.variables.items():
    print('variable: ', variable)


