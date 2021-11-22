import numpy as np
import xarray as xr
import netCDF4 as nc
from pylab import *
import cartopy.crs as ccrs

src = nc.Dataset("data_for_cutout.nc")
dst = nc.Dataset("cutout.nc", "w")

# Eventuell nicht notwendig
for name in src.ncattrs():
    dst.setncattr(name, src.getncattr(name))
# Dimensionen kopieren
for name, dimension in src.dimensions.items():

    if name == 'time':
        dst.createDimension(
            name, (len(dimension) if not dimension.isunlimited else None))
    else:
        dst.createDimension(
            name, (500 if not dimension.isunlimited else None))
print(dst)
# Variabeln kopieren
for name, variable in src.variables.items():
    x = dst.createVariable(
        name, variable.datatype, variable.dimensions)
    print('shape: ', np.shape(dst.variables[name]))
    if name == 'time':

        dst.variables[name][:] = src.variables[name][:]
    elif name == 'lat' or name == 'lon':
        print('name: ', name)
        dst.variables[name][:500] = src.variables[name][:500]
    elif name == 'LABELS':
        print('name: ', name)
        dst.variables[name][:500, :500] = src.variables[name][:500, :500]
    else:

        dst.variables[name][0, :500, :500] = src.variables[name][0, :500, :500]
    print('shape: ', np.shape(dst.variables[name]))
print(dst)
water_vapor = dst.variables['TMQ'][0, :, :]
lat = dst.variables['lat'][:500]
lon = dst.variables['lon'][:500]

ax = plt.subplot(3, 1, 1, projection=ccrs.PlateCarree())
ax.coastlines(color='gray')
ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
             linewidth=0.3, color='gray', alpha=0.5)

water_vapor_data = ax.contourf(lon, lat, water_vapor,
                               transform=ccrs.PlateCarree(), cmap=cm.Blues, alpha=0.5)
plt.show()
