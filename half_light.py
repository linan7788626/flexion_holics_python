import numpy as np
                                                               
def halflight(img_in):

	F=np.sum(img_in)
	
	nx=np.shape(img_in)[0]
	ny=np.shape(img_in)[1]
	xc=nx/2
	yc=ny/2
	
	x_in = np.linspace(0.0,nx-1,nx) 	# coordinate for x-axis
	y_in = np.linspace(0.0,ny-1,ny)	# coordinate for y-axis
	y_in,x_in = np.meshgrid(x_in,y_in)

	flux=np.sum(img_in)
	xc=np.sum(x_in*img_in)/flux
	yc=np.sum(y_in*img_in)/flux
	
	dr=0.1
	nbins=int(nx/2./dr)
	r = 0.0
#	for iter in range(1):
#		for ibin in range(nbins):
#			r1=dr*(ibin)
#			r2=dr*(ibin+1)
#			idx1=(x_in-xc)**2+(y_in-yc)**2 < r1**2
#			idx2=(x_in-xc)**2+(y_in-yc)**2 < r2**2
#			if (len(img_in[idx1]) > 0 and len(img_in[idx2])>0):
#				frac1=np.sum(img_in[idx1])/F
#				frac2=np.sum(img_in[idx2])/F
#			else:
#				frac1=0.
#				frac2=0.
#
#			if frac1<0.5 and frac2>0.5:
#				r = (r1+r2)/2.0
	for inter in range(3):
		for ibin in range(nbins):
			frac=0.0
			r=dr*(ibin+1)
			idx=(x_in-xc)**2+(y_in-yc)**2<r**2
			if (len(img_in[idx])>0):
				frac=np.sum(img_in[idx])/F
			else:
				frac=0.0
			if frac>0.5:
				ibin=nbins-1
				xc=np.sum(x_in[idx]*img_in[idx])/np.sum(img_in[idx])
				yc=np.sum(y_in[idx]*img_in[idx])/np.sum(img_in[idx])
				break
	return r
