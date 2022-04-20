import numpy as np
import netCDF4 as nc
import os


diff_times = nc.Dataset("TMQ_2000_01_06_sample.nc")
crnt_min_diff = 999999999
directory = os.fsencode('../data/train')

# iterate over dataset
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print("processing file: ",filename)
    filename = "../data/train/" + filename
    find_time = nc.Dataset(filename)
    tmq_find_time = np.squeeze(find_time.variables['TMQ'])

    #iterate over the 8 timesteps and compare pixelwise with current file
    for crnt_step in range(8):
        print("processing timestep: ",crnt_step)
        tmq_crnt_it = diff_times.variables['prw'][crnt_step]
        crnt_it_diff = 0
        print("crnt_min_diff: ", crnt_min_diff)

        for y,x in np.ndindex(tmq_crnt_it.shape):
            crnt_it_diff += abs(tmq_crnt_it[y,x] - tmq_find_time[y,x])

        if crnt_it_diff < crnt_min_diff:
            crnt_min_diff = crnt_it_diff
            min_file = filename

print('minimum difference: : ', crnt_min_diff)
print('min_file: ', min_file)
