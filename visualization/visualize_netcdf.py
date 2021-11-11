import matplotlib.pyplot as plt
from netCDF4 import Dataset as netcdf_dataset
import numpy as np
import cartopy.crs as ccrs
import xarray as xr
from matplotlib import cm
import matplotlib.colors as colors

# Funktion um nur einen Bereich einer Colormap zu nutzen
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

# NC Datei laden und die benötigten Variabeln extrahieren
data = xr.open_dataset('map_with_predictions.nc')
lat = data.lat
lon = data.lon
time = data.time
sea_level = data.PSL[0, :, :]
surface_wind_u = data.UBOT[0, :, :]
surface_wind_v = data.UBOT[0, :, :]
water_vapor = data.TMQ[0, :, :]
predictions = data.__xarray_dataarray_variable__[0, :, :]

# Karte mit dem PlateCarree Format
ax = plt.axes(projection=ccrs.PlateCarree())

# Variabeln auf Karte anzeigen
sea_level_pressure_data = ax.contour(lon, lat, sea_level,
             transform=ccrs.PlateCarree(), cmap=truncate_colormap(cm.Greys, 0, 0.1), linewidths=0.5)
surface_wind_data_u = plt.contourf(lon, lat, surface_wind_u,
             transform=ccrs.PlateCarree(), cmap=cm.Blues)        
surface_wind_data_v = plt.contourf(lon, lat, surface_wind_v,
             transform=ccrs.PlateCarree(), cmap=cm.Blues)          
water_vapor_data = plt.contourf(lon, lat, water_vapor,
             transform=ccrs.PlateCarree(), cmap=truncate_colormap(cm.binary, 0, 1), alpha=0.5)  
predictions_data = plt.contourf(lon, lat, predictions, levels=[0, 0.9, 1.9, 3],
             transform=ccrs.PlateCarree(), colors=['white', 'red', 'green'], alpha=0.2)  

# Legende anzeigen
plt.colorbar(surface_wind_data_u, label='Lowest model level meridional wind in m/s')
plt.colorbar(water_vapor_data, label='Total precipitable water in kg/m^2')
plt.colorbar(predictions_data, label='1=TC, 2=AR')

# Einheiten zu Konturlinien für den Luftdruck anzeigen
ax.clabel(
    sea_level_pressure_data,  
    colors=['black'],
    manual=False,  
    inline=False, 
    fmt='{:.0f}'.format,  
    fontsize='smaller'
)

# Küstenlinien auf Karte anzeigen
ax.coastlines()

# Karte öffnen
plt.show()