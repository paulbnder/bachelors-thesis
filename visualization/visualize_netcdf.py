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
data = xr.open_dataset('variables_cutout.nc')
predictions_netcdf = xr.open_dataset('predictions_cutout.nc')
lat = data.lat
lon = data.lon
time = data.time
sea_level = data.PSL[0, :, :]
surface_wind_u = data.UBOT[0, :, :]
surface_wind_v = data.VBOT[0, :, :]
water_vapor = data.TMQ[0, :, :]
predictions = predictions_netcdf.__xarray_dataarray_variable__[0, :, :]
labels = data.LABELS[:, :]
print('water_vapor: ', water_vapor)

plt.subplots_adjust(left=0.1, right=1, top=1, bottom=0)

# Anzahl an Klassen in Expertenlabels ausgeben
unique, counts = np.unique(labels, return_counts=True)
print(dict(zip(unique, counts)))

# Karte mit dem PlateCarree Format
ax_blank = plt.subplot(3, 1, 1, projection=ccrs.PlateCarree())
ax_preds = plt.subplot(3, 1, 2, projection=ccrs.PlateCarree())
ax_labels = plt.subplot(3, 1, 3, projection=ccrs.PlateCarree())
#ax = plt.axes(projection=ccrs.PlateCarree())
axis = [ax_blank, ax_preds, ax_labels]

# Variabeln auf Karte anzeigen
for ax in axis:
    sea_level_pressure_data = ax.contour(lon, lat, sea_level, levels=15,
                                         transform=ccrs.PlateCarree(), colors='black', linewidths=0.3)
    water_vapor_data = ax.contourf(lon, lat, water_vapor,
                                   transform=ccrs.PlateCarree(), cmap=truncate_colormap(cm.Blues, 0, 1), alpha=0.5)
    wind_vectors = ax.quiver(lon[::20], lat[::20], surface_wind_u[::20, ::20],
                             surface_wind_v[::20, ::20], color='grey')

# Add predictions and labels

predictions_data = ax_preds.contourf(lon, lat, predictions, levels=[0, 0.9, 1.9, 3],
                                     transform=ccrs.PlateCarree(), colors=['white', 'red', 'green'], alpha=0.3)
label_data = ax_labels.contourf(lon, lat, labels, levels=[0, 0.9, 1.9, 3],
                                transform=ccrs.PlateCarree(), colors=['white', 'red', 'green'], alpha=0.3)

# Legende anzeigen
plt.colorbar(water_vapor_data,
             label='Total precipitable water in kg/m^2', shrink=0.5, ax=ax_blank, pad=0.1)
# plt.colorbar(predictions_data, label='1=TC, 2=AR',
#              shrink=0.5, ax=ax_blank, pad=0.1)

# Einheiten zu Konturlinien für den Luftdruck anzeigen
# ax_preds.clabel(
#     sea_level_pressure_data,
#     colors=['black'],
#     manual=False,
#     inline=False,
#     fmt='{:.0f}'.format,
#     fontsize='smaller'
# )

# Küstenlinien auf Karte anzeigen
for ax in axis:
    ax.coastlines(color='gray')
    ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                 linewidth=0.3, color='gray', alpha=0.5)

# Karte öffnen
plt.savefig('maps_for_comparison', pad_inches=0, dpi=1000)
plt.show()
