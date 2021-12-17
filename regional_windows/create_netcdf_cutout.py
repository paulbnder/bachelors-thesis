import numpy as np
import xarray as xr
import netCDF4 as nc
from pylab import *
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

src = nc.Dataset("data_for_cutout.nc")
dst = nc.Dataset("cutout.nc", "w", format="NETCDF4")

# set window coordinates
latmin = 400
latmax = 580
lonmin = 0
lonmax = 600


# Dimensionen kopieren
for name, dimension in src.dimensions.items():
    # print('creating dimension at dst: ', name, dimension)
    if name == 'time':
        print('time', name, len(dimension), dimension)
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
print('lat: ', lat.size)
print('lon: ', lon.size)
ax = plt.subplot(2, 3,  1, projection=ccrs.PlateCarree())
ax.coastlines(color='gray')
ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
             linewidth=0.3, color='gray', alpha=0.5)
ax.set_extent([lon[0], lon[-1],
              lat[0], lat[-1]], crs=ccrs.PlateCarree())
print('extend: ', [lon[0], lon[-1],
                   lat[0], lat[-1]])
plt.contourf(lon, lat, water_vapor, cmap=cm.Blues,
             alpha=0.5, transform=ccrs.PlateCarree())

plt.contour(lon, lat, sea_level, levels=15,
            transform=ccrs.PlateCarree(), colors='grey', linewidths=0.3)

print('water_vapor.shape: ', water_vapor.shape)
np.savetxt('water_vapor.txt', water_vapor)
dst.sync()
dst.close()
# dst.to_netcdf("variables.nc")
plt.show()
