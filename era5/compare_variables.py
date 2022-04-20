from turtle import position
import matplotlib.pyplot as plt
from netCDF4 import Dataset as netcdf_dataset
import numpy as np
import cartopy.crs as ccrs
import xarray as xr
from matplotlib import cm
import matplotlib.colors as colors
import netCDF4 as nc

# Damit Margins bei speichern und anzeigen gleich sind 
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
mng.full_screen_toggle()
plt.subplots_adjust(left=0.02, right=0.98, top=0.99, bottom=0)

# Funktion um nur einen Bereich einer Colormap zu nutzen
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


# NC Datei laden und die benötigten Variabeln extrahieren
data = xr.open_dataset("data-2000-01-06-01-1_2.nc")

data2 = xr.open_dataset("CAM5-1-0.25degree_All-Hist_est1_v3_run2.cam.h2.2000.TMQ_only_jan6.nc")
mult_steps = xr.open_dataset("TMQ_2000_01_06_sample.nc")

lat = data.lat[:]
lon = data.lon[:]
lat2 = mult_steps.lat[:]
lon2 = mult_steps.lon[:]

tmq = data.TMQ[0, :, :]
tmq2 = data2.variables['TMQ'][3] #Zeitschritt von 0-7 einsetzen
tmq_crnt_step = mult_steps.variables['prw'][3] #Zeitschritt von 0-7 einsetzen


# Karte mit dem PlateCarree Format
ax_mult_steps = plt.subplot(2, 3,  2, projection=ccrs.PlateCarree())
ax_one_step = plt.subplot(2, 3,  1, projection=ccrs.PlateCarree())
ax2 = plt.subplot(2, 3,  3, projection=ccrs.PlateCarree())


ax2.set_title('TMQ from \nCAM5-1-0.25degree_All-Hist_est1_v3_run2.cam.h2.2000.TMQ_only_jan6.nc')
ax_one_step.set_title('TMQ from data-2000-01-06-01-1_2')
ax_mult_steps.set_title('TMQ from TMQ_2000_01_06_sample.nc')
axis = [ax_mult_steps, ax_one_step, ax2]

# Variabeln auf Karte anzeigen
for ax in axis:
    if ax == ax_one_step:
        tmq_cont_1 = ax.contourf(lon, lat, tmq,
                                       transform=ccrs.PlateCarree(), colors=("#F1F1F1", "#D5E9EE", "#BDD9E7", "#A7C6DD", "#95AFD0", "#8796C2", "#7C7BB2", "#755E9F", "#6F3C8B", "#6B0077"), alpha=0.9)
    if ax == ax_mult_steps:
        tmq_cont_2 = ax.contourf(lon2, lat2, tmq_crnt_step,
                                       transform=ccrs.PlateCarree(), colors=("#F1F1F1", "#D5E9EE", "#BDD9E7", "#A7C6DD", "#95AFD0", "#8796C2", "#7C7BB2", "#755E9F", "#6F3C8B", "#6B0077"), alpha=0.9)

tmq_cont_3 = ax2.contourf(lon, lat, tmq2,
                                       transform=ccrs.PlateCarree(), colors=("#F1F1F1", "#D5E9EE", "#BDD9E7", "#A7C6DD", "#95AFD0", "#8796C2", "#7C7BB2", "#755E9F", "#6F3C8B", "#6B0077"), alpha=0.9)

# Küstenlinien auf Karte anzeigen
for ax in axis:
    ax.coastlines(color='gray')
    grid = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                        linewidth=0.2, color='black', alpha=0.5)
    grid.right_labels = False
    grid.top_labels = False

# Legenden anzeigen

cbar_ax2 = plt.subplot(2, 3,  5, projection=None, visible=False)
plt.colorbar(tmq_cont_2,
             label='Total precipitable water in kg/m^2', shrink=1, ax=[cbar_ax2], location='top')
  

# Damit Margins bei speichern und anzeigen gleich sind 
figure = plt.gcf()  # get current figure
figure.set_size_inches(18, 9)
mng.full_screen_toggle()

# Karte anzeigen und speichern 
plt.savefig('Timestep 7',  dpi=1000, bbox_inches='tight')
plt.show()
