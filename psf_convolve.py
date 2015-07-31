import numpy as np



def psf_convolve(img_in,sig_psf_in):

# inputs img, sig_psf
# output, lensed image, psf
	nx_psf=int(10*sig_psf_in)/2+1
	
	xc_psf=(nx_psf-1.)/2.
	yc_psf=xc_psf
	
	nx=(np.shape(img_in))[0]
	ny=(np.shape(img_in))[1]
	
	psf=np.zeros((nx_psf,nx_psf))
	for i in range(nx_psf):
		for j in range(nx_psf):
	        	psf[i,j]=np.exp(-((i-xc_psf)**2+(j-yc_psf)**2)/(2.*sig_psf_in**2))
	psf=psf/np.sum(psf)
	
	img_smeared=img_in*0
	for i in range(nx):
		for j in range(ny):
			for i1 in range(nx_psf):
	            		di=i1-int(xc_psf)
	            		i2=i+di
				for j1 in range(nx_psf):
	                		dj=j1-int(yc_psf)
	                		j2=j+dj
	                		if (i2>=0 and i2<nx and j2>=0 and j2<nx):
	                		    	img_smeared[i,j]=img_smeared[i,j]\
							    +img_in[i2,j2]*psf[i1,j1]
	
	return img_smeared
