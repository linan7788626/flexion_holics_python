import numpy as np

def gmg(sig_in,fmax_in,eps_in):
	rmax=6.0*sig_in
	
	nx=int(2.4*rmax)
	ny=int(2.4*rmax)
	
	xc = nx/2.0
	yc = ny/2.0
	
	x_in = np.linspace(0.0,nx,nx) 	# coordinate for x-axis
	y_in = np.linspace(0.0,ny,ny)	# coordinate for y-axis
	x_out,y_out = np.meshgrid(x_in,y_in)
	
	img_out = np.zeros((nx,ny))
	
	r=np.sqrt(((x_out-xc)/(1.0+eps_in))**2.0+((y_out-yc)/(1.0-eps_in))**2.0)
	img_out = fmax_in*np.exp(-(r/sig_in)**1.5/2.0)
	idx = r>=rmax
	img_out[idx]=0.0
	img_total = np.sum(img_out)
	img_norm = img_out/img_total

	return x_out,y_out,img_out,img_norm

