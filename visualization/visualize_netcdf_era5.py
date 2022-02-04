import matplotlib.pyplot as plt
from netCDF4 import Dataset as netcdf_dataset
import numpy as np
import cartopy.crs as ccrs
import xarray as xr
from matplotlib import cm
import matplotlib.colors as colors
import netCDF4 as nc

# mng = plt.get_current_fig_manager()
# mng.window.showMaximized()
# mng.full_screen_toggle()

# Funktion um nur einen Bereich einer Colormap zu nutzen


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


# NC Datei laden und die benötigten Variabeln extrahieren
data = xr.open_dataset("files/era5_wind.nc")
#predictions_netcdf = xr.open_dataset('predictions.nc')
lat = data.latitude[:]
lon = data.longitude[:]-180


# water_vapor = data.TMQ[0, :, :]
# print('water vapor.shape: ', water_vapor.shape)

# print('water vapor: ', water_vapor)
# np.savetxt('water_vapor.txt', water_vapor)
# time = data.time
# sea_level = data.PSL[0, :, :]
surface_wind_u = data.u[0, :, :]
surface_wind_v = data.v[0, :, :]

#predictions = predictions_netcdf.__xarray_dataarray_variable__[0, :, :]
#print('predictions: ', predictions)

#surface_wind_u_copy = surface_wind_u.copy()
#surface_wind_v_copy = surface_wind_v.copy()
#total_wind_speed = np.sqrt(np.absolute(surface_wind_u_copy) +
#                           np.absolute(surface_wind_v_copy))
#vapor_flux = total_wind_speed * water_vapor

#labels = data.LABELS[:, :]


plt.subplots_adjust(left=0.02, right=0.98, top=0.99, bottom=0)

# Anzahl an Klassen in Expertenlabels ausgeben
#unique, counts = np.unique(labels, return_counts=True)


# Karte mit dem PlateCarree Format
ax_blank = plt.subplot(2, 3,  1, projection=ccrs.PlateCarree())
ax_preds = plt.subplot(2, 3,  2, projection=ccrs.PlateCarree())
ax_labels = plt.subplot(2, 3,  3, projection=ccrs.PlateCarree())
cbar_ax = plt.subplot(2, 3,  4, projection=None, visible=False)
ax_vapor_flux = plt.subplot(2, 3,  5, projection=ccrs.PlateCarree())
#ax = plt.axes(projection=ccrs.PlateCarree())
ax_blank.set_title('Weather variables')
ax_preds.set_title('Predictions')
ax_labels.set_title('Ground truth')
ax_vapor_flux.set_title('Vapor flux')
axis = [ax_blank, ax_preds, ax_vapor_flux, ax_labels]

# Variabeln auf Karte anzeigen

for ax in axis:

    # sea_level_pressure_data = ax.contour(lon, lat, sea_level, levels=15,
    #                                      transform=ccrs.PlateCarree(), colors='grey', linewidths=0.3)
    wind_vectors = ax.quiver(lon[::20], lat[::20], surface_wind_u[::20, ::20],
                             surface_wind_v[::20, ::20], color='grey')
    # if ax != ax_vapor_flux:
    #     water_vapor_data = ax.contourf(lon, lat, water_vapor,
    #                                    transform=ccrs.PlateCarree(), colors=("#F1F1F1", "#D5E9EE", "#BDD9E7", "#A7C6DD", "#95AFD0", "#8796C2", "#7C7BB2", "#755E9F", "#6F3C8B", "#6B0077"), alpha=0.7)
    # elif ax == ax_vapor_flux:
    #     vapor_flux_data = ax.contourf(lon, lat, vapor_flux,
    #                                   transform=ccrs.PlateCarree(), colors=("#ffffff", "#ABE0C1", "#87C5B0", "#66AAA0", "#498F8F", "#30747E", "#1C596D", "#0E3F5C"), alpha=0.7)

# np.savetxt('vapor_flux.txt', vapor_flux)
# print('labels: ', labels)
# # Add predictions and labels
# predictions_data = ax_preds.contourf(lon, lat, predictions, levels=[0, 0.9, 1.9, 3],
#                                      transform=ccrs.PlateCarree(), colors=[(0, 0, 0, 0), (1, 0, 0, 0.3), (0, 1, 0, 0.3)])
# label_data = ax_labels.contourf(lon, lat, labels, levels=[0, 0.9, 1.9, 3],
#                                 transform=ccrs.PlateCarree(), colors=[(0, 0, 0, 0), (1, 0, 0, 0.3), (0, 1, 0, 0.3)])

# Legende anzeigen
# plt.colorbar(water_vapor_data,
#              label='Total precipitable water in kg/m^2', shrink=1, ax=[cbar_ax], location='top')
# plt.colorbar(vapor_flux_data,
#              label='Vapor flux in kg/m*s', shrink=1, ax=[cbar_ax], location='top')
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
    grid = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                        linewidth=0.2, color='black', alpha=0.5)
    grid.right_labels = False
    grid.top_labels = False


# Karte öffnen
figure = plt.gcf()  # get current figure
figure.set_size_inches(18, 9)
plt.savefig('maps_for_comparison',  dpi=1000, bbox_inches='tight')
mng.full_screen_toggle()

# print('vf shape: ', vapor_flux.shape)
# print('wv shape: ', water_vapor.shape)
# print('labels shape: ', predictions.shape)
# print('predictions shape: ', labels.shape)
print('lat shape: ', lat.shape)
print('lon shape: ', lon.shape)


plt.show()
