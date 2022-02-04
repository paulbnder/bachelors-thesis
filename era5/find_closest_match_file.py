import numpy as np
import xarray as xr
import netCDF4 as nc
from pylab import *
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import os


diff_times = nc.Dataset("CAM5-1-0.25degree_All-Hist_est1_v3_run2.cam.h2.2000.TMQ_only_jan6.nc")
crnt_min_diff = 9999999999999



directory = os.fsencode('../data/test')
differences=[]
average_differences = []
filenames= []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print(filename)
    filename = "../data/test/" + filename
    find_time = nc.Dataset(filename)
    tmq_find_time = np.squeeze(find_time.variables['TMQ'])

    
    for crnt_step in range(8):
        print(crnt_step)
        tmq_crnt_it = diff_times.variables['TMQ'][crnt_step]
        crnt_it_diff = 0
        print("tmq_crnt_it.shape: ", tmq_crnt_it.shape)
        print("tmq_find_time.shape: ", tmq_find_time.shape)

        for y,x in np.ndindex(tmq_crnt_it.shape):
            crnt_it_diff += abs(tmq_crnt_it[y,x] - tmq_find_time[y,x])
        differences.append(crnt_it_diff)
        average_differences.append(crnt_it_diff/884736)
        filenames.append(filename)

        if crnt_it_diff/884736 < crnt_min_diff:
            crnt_min_diff = crnt_it_diff
            min_file = filename
            
print("average differences: ", average_differences)
print("differences: ", differences)

differences_array = np.array(differences)
average_differences_array = np.array(average_differences)
filenames_array = np.array(filenames)

np.savetxt('differences.txt', differences_array)
np.savetxt('average_differences.txt', average_differences_array)
np.savetxt('filenames.txt', filenames_array)

print('crnt_min_diff: ', crnt_min_diff)
print('min_file: ', min_file)
