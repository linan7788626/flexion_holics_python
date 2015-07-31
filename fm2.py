import numpy as np
import lensdemo_funcs as ldf
from matplotlib.pylab import *
import pyfits as pf
from lens_image import *
#------------------------------------------------------------------------------------------
def flex_m2(img_in,w_in,sig2_in):
	img_in=img_in*w_in

	nx = np.shape(img_in)[0]
	ny = np.shape(img_in)[1]

	x_in = np.linspace(0.0,nx-1,nx) 	# coordinate for x-axis
	y_in = np.linspace(0.0,ny-1,ny)	# coordinate for y-axis
	y_in,x_in = np.meshgrid(x_in,y_in)

	fu = np.sum(img_in)
	Q1 = np.sum(x_in*img_in)
	Q2 = np.sum(y_in*img_in)
	xc = Q1/fu #x position of the center of the image
	yc = Q2/fu #y 

	Q11   =  np.sum((x_in-xc)**2*img_in)/fu
	Q12   =  np.sum((x_in-xc)*(y_in-yc)*img_in)/fu
	Q22   =  np.sum((y_in-yc)**2*img_in)/fu
	
	Q1111 =  np.sum((x_in-xc)**4*img_in)/fu
	Q1112 =  np.sum((x_in-xc)**3*(y_in-yc)*img_in)/fu
	Q1122 =  np.sum((x_in-xc)**2*(y_in-yc)**2*img_in)/fu
	Q1222 =  np.sum((x_in-xc)*(y_in-yc)**3*img_in)/fu
	Q2222 =  np.sum((y_in-yc)**4*img_in)/fu
	
	xi = Q1111+2.0*Q1122+Q2222
	tmp_correct = np.zeros((2))
#-----------------------------------------------------------------------
	tmp_correct[0] = 9.0*xi-6.0*(Q11**2.0+Q22**2.0)
	tmp_correct[1] = xi
	return tmp_correct
