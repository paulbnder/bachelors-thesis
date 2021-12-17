import numpy as np
import xarray as xr
import netCDF4 as nc
from pylab import *
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import os

directory = os.fsencode('data/test')

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print(filename)
    source_filename = "data/test/" + filename
    destination_filename = "data/test_regional_windows/" + filename

    src = nc.Dataset(source_filename)
    dst = nc.Dataset(destination_filename, "w", format="NETCDF4")

    # set window coordinates
    latmin = 200
    latmax = 700
    lonmin = 0
    lonmax = 600

    # Dimensionen kopieren
    for name, dimension in src.dimensions.items():
        # print('creating dimension at dst: ', name, dimension)
        if name == 'time':
            dst.createDimension(
                name, (len(dimension) if not dimension.isunlimited else None))
        elif name == 'lat':
            dst.createDimension(
                name, (latmax-latmin if not dimension.isunlimited else None))
        elif name == 'lon':
            dst.createDimension(
                name, (lonmax-lonmin if not dimension.isunlimited else None))
    # print('dst after creating dimensions: ', dst)

    # Variabeln kopieren
    for name, variable in src.variables.items():
        x = dst.createVariable(
            name, variable.datatype, variable.dimensions)
        if name == 'time':
            dst.variables[name][:] = src.variables[name][:]
        elif name == 'lat':
            dst.variables[name][:] = src.variables[name][latmin:latmax]
        elif name == 'lon':
            dst.variables[name][:] = src.variables[name][lonmin:lonmax]
        elif name == 'LABELS':
            dst.variables[name][:,
                                :] = src.variables[name][latmin:latmax, lonmin:lonmax]
        else:
            dst.variables[name][0, :,
                                :] = src.variables[name][0, latmin:latmax, lonmin:lonmax]
    # print('dst after copying variables: ', dst.variables)

    water_vapor = dst.variables['TMQ'][0, :, :]
    sea_level = dst.variables['PSL'][0, :, :]

    np.savetxt('output.txt', dst.variables['TMQ']
               [0, latmin:latmax, lonmin:lonmax])
    lat = dst.variables['lat'][:]
    lon = dst.variables['lon'][:]
    lon = lon-180
    ax = plt.subplot(2, 3,  1, projection=ccrs.PlateCarree())
    ax.coastlines(color='gray')
    ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                 linewidth=0.3, color='gray', alpha=0.5)
    ax.set_extent([lon[0], lon[-1],
                   lat[0], lat[-1]], crs=ccrs.PlateCarree())
    plt.contourf(lon, lat, water_vapor, cmap=cm.Blues,
                 alpha=0.5, transform=ccrs.PlateCarree())

    plt.contour(lon, lat, sea_level, levels=15,
                transform=ccrs.PlateCarree(), colors='grey', linewidths=0.3)

    dst.sync()
    dst.close()
