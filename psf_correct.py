import numpy as np
import lensdemo_funcs as ldf
from matplotlib.pylab import *
import pyfits as pf

from flexion_moments import *
from lens_image import *
from half_light import *
from weight_func import *
from psf_convolve import *

kappa=0.
gamma1=0.
gamma2=0.
A=np.array([[1-kappa-gamma1,-gamma2],[-gamma2,1-kappa+gamma1]])

g11=0.004
g12=0.004
g21=0.0
g22=0.0

F_model=[g11+g22,g21-g12]
G_model=[g11-g22,g21+g12]
print 'Model gam=',gamma1,gamma2
print 'Model F=',F_model
print 'Model G=',G_model

D=np.zeros((2,2,2))

D[:,:,0]=[[-2*g11-g22,-g21],[-g21,-g22]]
D[:,:,1]=[[-g21,-g22],[-g22,2*g12-g21]]
#--------------------------------------------------------------------------------------
sigma=3.
rmax=6*sigma
nx=fix(2.4*rmax)
xc=nx/2.
yc=nx/2.


img_source=np.zeros((nx,nx))
img_lensed=np.zeros((nx,nx))

fmax=100.

eps=0.
bg=200.
noisefrac=.1

for i in range(nx):
	for j in range(nx):
        	r=np.sqrt(((i-xc)/(1.+eps))**2+((j-yc)/(1.-eps))**2)
		if (r < rmax):
            		img_source[i,j]=fmax*np.exp(-(r**2/2/sigma**2))

img_lensed=lq_flex_img(img_source,A,D)
sig_psf=3.

img_smeared=psf_convolve(img_lensed,sig_psf)
#img_smeared=img_lensed
noise_add=np.random.standard_normal((nx,nx))*noisefrac*np.sqrt(img_smeared+bg)
img_smeared=img_smeared+noise_add
#-------------------------------------------------------------------------------------
rh=halflight(img_smeared)
factor=1.5;
print 'Factor=',factor
#flex_factor=psf_correct(img_smeared,psf)
#print,'Flex_factor=',flex_factor
sig2 = factor*(rh)**2.0
wf = winf(img_smeared,sig2)
fm=flex_m(img_smeared,wf,sig2)[0]
print 'Uncorrected Estimates='
#print 'Gamma=',gam_moments
print 'F=',fm[0],fm[1]
print 'G=',fm[2],fm[3]

#print 'Corrected Estimates='
#print 'F_corr=',F_moments*flex_factor[0]
#print 'G_corr=',G_moments*flex_factor[1]
