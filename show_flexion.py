import numpy as np
from pylab import *
import pyfits as pf

from flexion_moments import *
from lens_image import *
from half_light import *
from weight_func import *

#@profile
def main():
    fmax = 1.0
    eps = 0.0

    sigma=3.0
    rmax=6.0*sigma

    nn1=int(2.4*rmax)
    nn2=int(2.4*rmax)

    xc1 = nn1/2.0
    yc1 = nn2/2.0

    xi1 = np.linspace(0.0,nn1-1,nn1) 	# coordinate for x-axis
    xi2 = np.linspace(0.0,nn2-1,nn2)	# coordinate for y-axis
    yy,xx = np.meshgrid(xi1,xi2)

    img_source = np.zeros((nn1,nn2))
    img_lensed = np.zeros((nn1,nn2))

    r=np.sqrt(((xx-xc1)/(1.0+eps))**2.0+((yy-yc1)/(1.0-eps))**2.0)
    idx =  r > rmax
    img_source = fmax*exp(-(r/sigma)**1.5/2.0)
    img_source[idx] = 0

    kappa=0.0
    gamma1=0.0
    gamma2=0.0
    A1=np.array([[1.0-kappa-gamma1,-gamma2],[-gamma2,1-kappa+gamma1]])

    g11= 0.02
    g12= 0.01
    g21= 0.00
    g22=-0.00

    D1=np.zeros((2,2,2))
    D1[0,0,0]=-2.0*g11-g22
    D1[0,0,1]=-g21
    D1[0,1,0]=-g21
    D1[0,1,1]=-g22

    D1[1,0,0]=-g21
    D1[1,0,1]=-g22
    D1[1,1,0]=-g22
    D1[1,1,1]=2.0*g12-g21

    img_lensed = lq_flex_img(img_source,A1,D1)	# 3d gaussian function
    zz = img_lensed
    #img_lensed = lq_flex_img2(img_source,0.0,0.0,0.0,0.04,0.0,0.0,0.0)	# 3d gaussian function
    #zz = img_lensed
    #--------------------------------------------------------------------------------------------
    rh = halflight(zz)
    factor = 1.5
    sig2 = (factor*rh)**2.0
    wf = winf(zz,sig2)
    all_moments = flex_m(zz,wf,sig2)
    fm = all_moments[0]
    gm = all_moments[1]
    #--------------------------------------------------------------------------------------------
    F_model = np.array([g11+g22,g21-g12])
    G_model = np.array([g11-g22,g21+g12])
    print F_model, G_model
    print 'F1 = %f' %(fm[0])
    print 'F2 = %f' %(fm[1])
    print 'G1 = %f' %(fm[2])
    print 'G2 = %f' %(fm[3])
##--------------------------------------------------------------------
    #levels = [0.0,0.15,0.30,0.45,0.60,0.75,0.90,1.05]
    figure(num=None,figsize=(10,5),dpi=80, facecolor='w', edgecolor='k')

    a = axes([0.05,0.1,0.4,0.8])
    a.imshow(img_source)

    b = axes([0.55,0.1,0.4,0.8])
    b.imshow(zz)
    show()
    return 0

if __name__ == '__main__':
    main()
