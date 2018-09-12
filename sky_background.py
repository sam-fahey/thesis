#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import healpy as H
from pylab import *
from matplotlib import cm
from scipy.interpolate import UnivariateSpline, PchipInterpolator
from scipy.interpolate import InterpolatedUnivariateSpline

nside = 64

zenpdf = np.load('/data/user/sfahey/FRB/L2_Analysis/scripts/zenith_pdf.npy')
bins = zenpdf.item()['b']
htotal = zenpdf.item()['htotal']
htotal = 1.*htotal*(len(bins)-1) / (sum(htotal) * 4.*np.pi)
# transform bin values into zenith (rad) increasing
bins = np.arccos(bins)

x = np.r_[bins[0], bins[:-1]+np.diff(bins)/2., bins[-1]]
y = np.r_[htotal[0], htotal, htotal[-1]]
pdf = PchipInterpolator( x, y )
density = np.linspace(0, np.pi, 1e3)
dense_pdf = pdf (density)

m = H.ma(np.zeros(H.nside2npix(nside), dtype=np.double))
pixel_theta, pixel_phi = H.pix2ang(nside, np.arange(H.nside2npix(nside)))

search_density = np.pi-density
for i in range(len(pixel_theta)):
  index = (np.abs((search_density) - pixel_theta[i])).argmin()
  m[i] = dense_pdf[index]

cool_cmap = cm.inferno
cool_cmap.set_under('w')

plt.figure(figsize=(8, 5))

moll = H.mollview(
  m,coord='C',flip='astro', cmap=cool_cmap, 
  cbar=True, title='', rot=180, xsize=1000, 
  margins=[0., 0., 0., 0.], hold=True,
  min=0.0295, max=0.175)
H.graticule(coord='C')

plt.title('$B_i$: Level2-pass2 background PDF')

plt.savefig('/home/sfahey/public_html/Likelihood/background_pdf_skymap_L2.pdf')
plt.savefig('/home/sfahey/public_html/Likelihood/background_pdf_skymap_L2.png')

