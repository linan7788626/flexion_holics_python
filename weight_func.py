import numpy as np
from half_light import *
#--------------------------------------------------------------------
def winf(img_in,sig2_in):
	
	fu = np.sum(img_in)
	nx = np.shape(img_in)[0]
	ny = np.shape(img_in)[1]

	x_in = np.linspace(0.0,nx-1,nx) 	# coordinate for x-axis
	y_in = np.linspace(0.0,ny-1,ny)	# coordinate for y-axis
	y_in,x_in = np.meshgrid(x_in,y_in)

	Q1 = np.sum(x_in*img_in)
	Q2 = np.sum(y_in*img_in)
	xc = Q1/fu #x position of the center of the image
	yc = Q2/fu #y position of the center of the image
	
	
	niter=1
	for k in range(niter):
		w = np.zeros((nx,ny))
		for i in range(nx):
			for j in range(ny):
				dx = x_in[i,j]-xc
				dy = y_in[i,j]-yc
				r = np.sqrt(dx**2.0+dy**2.0)
				w[i,j] = np.exp(-r**2.0/(2.0*sig2_in))
		
		flux=np.sum(w*img_in)
		xc = np.sum(x_in*w*img_in)/flux
		yc = np.sum(y_in*w*img_in)/flux

	wt = np.sum(w)
	w = w/wt
	return w

