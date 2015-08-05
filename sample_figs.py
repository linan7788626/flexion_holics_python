import numpy as np
import lensdemo_funcs as ldf
from matplotlib.pylab import *
#import pyfits as pf
import time
st = time.time()

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

xi1 = np.linspace(0.0,nn1-1.0,nn1) 	# coordinate for x-axis
xi2 = np.linspace(0.0,nn2-1.0,nn2)	# coordinate for y-axis
yy,xx = np.meshgrid(xi1,xi2)

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

g11= 0.020
g12= 0.02
g21= 0.00
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


#img_lensed = lq_flex_img(img_source,A1,D1)	# 3d gaussian function
#zz = img_lensed
#img_lensed = lq_flex_img2(img_source,0.0,0.0,0.0,0.04,0.0,0.0,0.0)	# 3d gaussian function
#zz = img_lensed
#--------------------------------------------------------------------------------------------
inter = 1
nfactor = 1
factor_arr = np.zeros((nfactor))
F1_arr = np.zeros((inter,nfactor))
F2_arr = np.zeros((inter,nfactor))
G1_arr = np.zeros((inter,nfactor))
G2_arr = np.zeros((inter,nfactor))

for i in range(inter):
	img_lensed = lq_flex_img(img_source,A1,D1)	# 3d gaussian function
	noise_add = (np.random.standard_normal((nn1,nn2)))*0.02*np.sqrt(img_lensed+200)
	zz = img_lensed + noise_add
	#print mean(noise_add),np.std(noise_add)
	#print mean(zz),np.std(zz)
	for j in range(nfactor):

		rh = halflight(zz)
		factor = 0.4+j*0.2
		sig2 = factor*rh**2.0
		wf = winf(zz,sig2)
		fm = flex_m(zz,wf,sig2)[0]

		F_model = np.array([g11+g22,g21-g12])
		G_model = np.array([g11-g22,g21+g12])

		factor_arr[j]= factor
		F1_arr[i][j] = np.abs(fm[0]/F_model[0])-1.0
		F2_arr[i][j] = np.abs(fm[1]/F_model[1])-1.0
		G1_arr[i][j] = np.abs(fm[2]/G_model[0])-1.0
		G2_arr[i][j] = np.abs(fm[3]/G_model[1])-1.0

et = time.time()
print (et-st)
#--------------------------------------------------------------------
levels = [0.01,0.30,0.45,0.60,0.75,0.9,1.05]
figure(num=None,figsize=(12,6),dpi=80, facecolor='w', edgecolor='k')


a = axes([0.08,0.1,0.4,0.8])
#a.set_xlim(0.0,3.0)
#a.set_ylim(-1.5,1.5)
#a.contourf(xx,yy,img_source)
a.imshow(img_source)

b = axes([0.55,0.1,0.4,0.8])
#b.set_xlim(0.0,3.0)
#b.set_ylim(0,0.2)
#b.contourf(xx,yy,zz)
b.imshow(img_lensed)

show()
