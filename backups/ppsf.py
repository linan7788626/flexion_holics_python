import numpy as np
import lensdemo_funcs as ldf
from matplotlib.pylab import *
import pyfits as pf
import aipy.deconv as ad
import scipy.signal as ss
import numpy.fft as nf

from fm2 import *
from flexion_moments import *
from lens_image import *
from half_light import *
from weight_func import *
from gn_flux import *

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
#print 'Model gam=',gamma1,gamma2
#print 'Model F=',F_model
#print 'Model G=',G_model

D=np.zeros((2,2,2))

D[:,:,0]=[[-2*g11-g22,-g21],[-g21,-g22]]
D[:,:,1]=[[-g21,-g22],[-g22,2*g12-g21]]
#--------------------------------------------------------------------------------------
sigma = 3.0
sig_psf=1.1
fmax=100.
eps=0.
bg=200.
noisefrac=.1

(xx,yy,img_source)=gmg(sigma,fmax,eps)[:3]
img_lensed=lq_flex_img(img_source,A,D)
psf_tmp=gmg(sig_psf,1.0,eps)[3]

nloop = 50
flex_ratio = np.zeros((nloop,4))
for i in range(nloop):
	#psf_tmp_f = nf.fftn(psf_tmp,psf_tmp.shape)
	#img_lensed_f = nf.fftn(img_lensed,img_lensed.shape)
	#img_smeared_f = psf_tmp_f*img_lensed_f
	#img_smeared = nf.ifftn(img_smeared_f,img_smeared_f.shape)

	img_smeared=ss.fftconvolve(img_lensed,psf_tmp,'same')

	#img_smeared=img_lensed
	#noise_add=np.random.standard_normal((np.shape(img_lensed)[0]\
	#	 ,np.shape(img_lensed)[1]))*noisefrac*np.sqrt(img_smeared+bg)
	#img_smeared=img_smeared+noise_add
#-------------------------------------------------------------------------------------
	factor=1.5
	rh1=halflight(img_lensed)
	sig21 = factor*(rh1)**2.0
	wf1 = winf(img_lensed,sig21)
	fm1 = flex_m(img_lensed,wf1,sig21)[0]
	
	rh2=halflight(img_smeared)
	sig22 = factor*(rh2)**2.0
	wf2 = winf(img_smeared,sig22)
	fm2 = flex_m(img_smeared,wf2,sig22)[0]
	
	flex_ratio[i][:] = fm1/fm2

#print flex_ratio
print np.mean([flex_ratio[:,0],flex_ratio[:,1]])
print np.mean([flex_ratio[:,2],flex_ratio[:,3]])
fcup=flex_m2(img_lensed,wf1,sig21)
fcdn=flex_m2(img_smeared,wf2,sig22)

fc1=fcup[0]/fcdn[0]
fc2=fcup[1]/fcdn[1]

print 1.0/fc1
print 1.0/fc2
#print 'Uncorrected Estimates='
##print 'Gamma=',gam_moments
#print 'F=',fm[0],fm[1]
#print 'G=',fm[2],fm[3]
#
#print 'Corrected Estimates='
#print 'F_corr=',fm[0]/fc1,fm[1]/fc1
#print 'G_corr=',fm[2]/fc2,fm[3]/fc2
#--------------------------------------------------------------------
levels = [0.30,10,30,50]
figure(num=None,figsize=(10,5),dpi=80, facecolor='w', edgecolor='k')


a = axes([0.05,0.1,0.4,0.8])
a.set_xlim(-5.0,5.0)
a.set_ylim(-5.0,5.0)
#a.contourf(xx,yy,zz,levels)
#a.contourf(xx,yy,img_lensed)
a.plot(flex_ratio[:,0],flex_ratio[:,1],'ro')
a.plot(flex_ratio[:,2],flex_ratio[:,3],'go')
#
#b = axes([0.55,0.1,0.4,0.8])
#b.set_xlim(0.0,50.0)
#b.set_ylim(0.0,50.0)
#b.contourf(xx,yy,img_smeared)
##b.contourf(zz)
show()
