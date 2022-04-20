import numpy as np
import xarray as xr
import netCDF4 as nc
from pylab import *
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import os

# directory = os.fsencode('./files_to_merge')


# filename = os.fsdecode(file)
# print(filename)

# file1 = "files_to_merge/" + filename
# destination_filename = "files_to_merge/" + filename
# # 
file_tmq = nc.Dataset('2012_08_7-9-17_tmqpsl_remapped.nc')
file_wind = nc.Dataset('2012_08_7-9-17_wind_remapped.nc')
file_labels = nc.Dataset('data-2012-08-17-01-1_0.nc')

dst = nc.Dataset('2012_08_17_combined.nc', "w", format="NETCDF4")

#     # set window coordinates
#     latmin = 0
#     latmax = 768
#     lonmin = 0
#     lonmax = 1152

#     # Dimensionen kopieren
for name, dimension in file_labels.dimensions.items():
    # print('creating dimension at dst: ', name, dimension)
    if name == 'time':
        dst.createDimension(
            name, (len(dimension) if not dimension.isunlimited else None))
    elif name == 'lat':
        dst.createDimension(
            name, (768 if not dimension.isunlimited else None))
    elif name == 'lon':
        dst.createDimension(
            name, (1152 if not dimension.isunlimited else None))
# print('dst after creating dimensions: ', dst)

#     # Variabeln kopieren
for name, variable in file_labels.variables.items():
    x = dst.createVariable(
        name, variable.datatype, variable.dimensions)
    print(name, variable.datatype, variable.dimensions)
    if name == 'LABELS':
        dst.variables[name][:,
                            :] = file_labels.variables[name][:, :]
    elif name == 'time':
            dst.variables[name][:] = file_labels.variables[name][:]
    elif name == 'lat':
        dst.variables[name][:] = file_labels.variables[name][:]
    elif name == 'lon':
        dst.variables[name][:] = file_labels.variables[name][:]

dst.variables['U850'][0, :, :] = file_wind.variables['Band5'][:]
dst.variables['V850'][0, :, :] = file_wind.variables['Band6'][:]
dst.variables['PSL'][0, :, :] = file_tmq.variables['Band5'][:]
dst.variables['TMQ'][0, :, :] = file_tmq.variables['Band6'][:]


#         if name == 'time':
#             dst.variables[name][:] = src.variables[name][:]
#         elif name == 'lat':
#             dst.variables[name][:] = src.variables[name][latmin:latmax]
#         elif name == 'lon':
#             dst.variables[name][:] = src.variables[name][lonmin:lonmax]
#         elif name == 'LABELS':
#             dst.variables[name][:,
#                                 :] = src.variables[name][latmin:latmax, lonmin:lonmax]
#         else:
#             dst.variables[name][0, :,
#                                 :] = src.variables[name][0, latmin:latmax, lonmin:lonmax]
#     water_vapor = dst.variables['TMQ'][0, :, :]
#     sea_level = dst.variables['PSL'][0, :, :]

#     # Add vapor flux
#     dst.createVariable('VF', 'float32', ('time', 'lat', 'lon'))
#     wind_u = dst.variables['U850'][0, :, :]
#     wind_v = dst.variables['V850'][0, :, :]
#     wind_u_copy = wind_u.copy()
#     wind_v_copy = wind_v.copy()
#     total_wind_speed = np.sqrt(np.absolute(wind_u_copy) +
#                                np.absolute(wind_v_copy))
#     vapor_flux = total_wind_speed * water_vapor
#     dst.variables['VF'][0, :, :] = vapor_flux

#     lat = dst.variables['lat'][:]
#     lon = dst.variables['lon'][:]
#     lon = lon-180
#     ax = plt.subplot(2, 3,  1, projection=ccrs.PlateCarree())
#     ax.coastlines(color='gray')
#     ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
#                  linewidth=0.3, color='gray', alpha=0.5)
#     ax.set_extent([lon[0], lon[-1],
#                    lat[0], lat[-1]], crs=ccrs.PlateCarree())
#     plt.contourf(lon, lat, water_vapor, cmap=cm.Blues,
#                  alpha=0.5, transform=ccrs.PlateCarree())

#     plt.contour(lon, lat, sea_level, levels=15,
#                 transform=ccrs.PlateCarree(), colors='grey', linewidths=0.3)

#     dst.sync()
#     dst.close()
