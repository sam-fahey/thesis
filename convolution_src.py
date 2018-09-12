from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

def gaussian_2d (X, Y, x, y, sigma):
  Z = (1. / (2*np.pi*(sigma**2))) * np.exp(-1.*((X-x)**2+(Y-y)**2)/(2*sigma**2))
  return Z

fig = plt.figure(figsize=(12,4))
ax = fig.gca(projection='3d')

# Make data.
sigma = 1
lim_sig = 5
limits = [-1*lim_sig*sigma, lim_sig*sigma]
X = np.linspace(limits[0], limits[1], 101)
Y = np.linspace(limits[0], limits[1], 101)
X, Y = np.meshgrid(X, Y)

# GridSpec nrows ncols
grid = plt.GridSpec(1, 3)

# grid row col
ax1 = plt.subplot(grid[0, 0], projection='3d')
Z1 = gaussian_2d (X, Y, 0, 0, 2)
Z2 = (1. / (2*np.pi*(2**2))) * np.exp(-1.*((X-2)**2/(2*0.7**2)+(Y-3)**2/(2*0.4**2)))

# plot first surface
surf = ax1.plot_surface(X, Y, Z1, cmap=cm.inferno, linewidth=0, alpha=1)
ax1.set_xlim(limits)
ax1.set_ylim(limits)
ax1.set_zlim(0,1.1*np.amax(Z1))
ax1.set_title('Event PSF')

ax2 = plt.subplot(grid[0, 1], projection='3d')
surf = ax2.plot_surface(X, Y, Z2, cmap=cm.inferno, linewidth=0)
ax2.set_xlim(limits)
ax2.set_ylim(limits)
ax2.set_zlim(0,1.1*np.amax(Z2))
ax2.set_title('Source PDF')

ax3 = plt.subplot(grid[0, 2], projection='3d')
Z = Z1*Z2
surf = ax3.plot_surface(X, Y, Z, cmap=cm.inferno, linewidth=0)
ax3.set_xlim(limits)
ax3.set_ylim(limits)
ax3.set_zlim(0,1.1*np.amax(Z))
ax3.set_title('Convolution')
# Add a color bar which maps values to colors.
#fig.colorbar(surf, shrink=0.5, aspect=5)

ax1.view_init(30, 280)
ax2.view_init(30, 280)
ax3.view_init(30, 280)

fig.subplots_adjust(left=0, right=0.95, bottom=0.05, top=0.95)
plt.savefig('/home/sfahey/public_html/Likelihood/convolution_signal.pdf')
plt.savefig('/home/sfahey/public_html/Likelihood/convolution_signal.png')
