import numpy as np
import lensdemo_funcs as ldf
from matplotlib.pylab import *
import pyfits as pf

from flexion_moments import *
from lens_image import *
from half_light import *
from weight_func import *

fmax = 100.
eps = 0.0


sigma=3.0
rmax=6.0*sigma

nn1=int(2.4*rmax)
nn2=int(2.4*rmax)

xc1 = nn1/2.0
yc1 = nn2/2.0

xi1 = np.linspace(0.0,nn1,nn1) 	# coordinate for x-axis
xi2 = np.linspace(0.0,nn2,nn2)	# coordinate for y-axis
xx,yy = np.meshgrid(xi1,xi2)

img_source = np.zeros((nn1,nn2))
img_lensed = np.zeros((nn1,nn2))

for i in range(nn1):
	for j in range(nn2):
		r=np.sqrt(((i-xc1)/(1.0+eps))**2.0+((j-yc1)/(1.0-eps))**2.0)
		if r < rmax:
			img_source[i,j] = fmax*exp(-(r/sigma)**1.5/2.0)

kappa=0.0
gamma1=0.0
gamma2=0.0
A1=np.array([[1.0-kappa-gamma1,-gamma2],[-gamma2,1-kappa+gamma1]])

g11= 0.00
g12= 0.02
g21= 0.02
g22= 0.00


D1=np.zeros((2,2,2))
D1[0,0,0]=-2.0*g11-g22
D1[0,0,1]=-g21
D1[0,1,0]=-g21
D1[0,1,1]=-g22

D1[1,0,0]=-g21
D1[1,0,1]=-g22
D1[1,1,0]=-g22
D1[1,1,1]=2.0*g12-g21

(xx,yy) = lq_flex(xx,yy,A1,D1)	# 3d gaussian function
zz = img_source

#img_lensed = lq_flex_img(img_source,A1,D1)	# 3d gaussian function
#zz = img_lensed
#img_lensed = lq_flex_img2(img_source,0.0,0.0,0.0,0.04,0.0,0.0,0.0)	# 3d gaussian function
#zz = img_lensed
#--------------------------------------------------------------------------------------------
rh = halflight(xx,yy,zz)
factor = 1.5
sig2 = (factor*rh)**2.0
wf = winf(xx,yy,zz,sig2)
fm = flex_m(xx,yy,zz,wf,sig2)
                                                                                         
F_model = np.array([g11+g22,g21-g12])
G_model = np.array([g11-g22,g21+g12])
print F_model, G_model
print 'F1 = %f' %(fm[0])
print 'F2 = %f' %(fm[1])
print 'G1 = %f' %(fm[2])
print 'G2 = %f' %(fm[3])
#--------------------------------------------------------------------
#levels = [0.01,0.30,0.45,0.60,0.75,0.9,1.05]
figure(num=None,figsize=(10,5),dpi=80, facecolor='w', edgecolor='k')


a = axes([0.05,0.1,0.4,0.8])
a.set_xlim(0.0,nn1)
a.set_ylim(0.0,nn2)
#a.contourf(xx,yy,zz,levels)
a.contourf(xx,yy,zz)

b = axes([0.55,0.1,0.4,0.8])
b.set_xlim(0.0,nn1)
b.set_ylim(0.0,nn2)
#b.contourf(xld,yld,zz,levels)
#b.contourf(xx,yy,zz)
b.contourf(xx,yy,wf*zz)
show()
