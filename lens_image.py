import numpy as np

def lq_flex(x1,x2,A,D):

	x1c = np.mean(x1)#[0,:])
	x2c = np.mean(x2)#[:,0])
	x1 = x1-x1c
	x2 = x2-x2c

	x1new=x1*0.0
	x2new=x2*0.0

	x1new = x1c+A[0,0]*x1+A[0,1]*x2 \
		   +0.5*D[0,0,0]*x1*x1     \
		   +0.5*D[0,0,1]*x1*x2     \
		   +0.5*D[0,1,0]*x2*x1     \
		   +0.5*D[0,1,1]*x2*x2
	x2new = x2c+A[1,0]*x1+A[1,1]*x2 \
		   +0.5*D[1,0,0]*x1*x1     \
		   +0.5*D[1,0,1]*x1*x2     \
		   +0.5*D[1,1,0]*x2*x1     \
		   +0.5*D[1,1,1]*x2*x2

	return (x1new,x2new)
#--------------------------------------------------------------------------------------------
def lq_flex_img_numpy(img_in,A,D):

	nx = np.shape(img_in)[0]
	ny = np.shape(img_in)[1]
	x1c=nx/2.0
	x2c=ny/2.0
	img_out=img_in*0.0

	xi = np.linspace(0,nx-1,nx)
	yi = np.linspace(0,ny-1,ny)
	xi,yi = np.meshgrid(xi,yi)

	dx1 = (xi-x1c)
	dx2 = (yi-x2c)

	xb1 = x1c+A[0,0]*dx1+A[0,1]*dx2 \
		 +0.5*D[0,0,0]*dx1*dx1     \
		 +0.5*D[0,0,1]*dx1*dx2     \
		 +0.5*D[0,1,0]*dx2*dx1     \
		 +0.5*D[0,1,1]*dx2*dx2
	xb2 = x2c+A[1,0]*dx1+A[1,1]*dx2 \
		 +0.5*D[1,0,0]*dx1*dx1     \
		 +0.5*D[1,0,1]*dx1*dx2     \
		 +0.5*D[1,1,0]*dx2*dx1     \
		 +0.5*D[1,1,1]*dx2*dx2

	idxb1 = xb1>nx-1
	xb1[idxb1] = xb1[idxb1]-nx+1
	idxb1 = xb1<0
	xb1[idxb1] = xb1[idxb1]+nx-1
	i1 = xb1.astype(int)
	wx = 1.-(xb1-i1)

	idxb2 = xb2>ny-1
	xb2[idxb2] = xb2[idxb2]-ny+1
	idxb2 = xb2<0
	xb2[idxb2] = xb2[idxb2]+ny-1
	j1 = xb2.astype(int)
	wy = 1.-(xb2-j1)

	iarr = np.array([i1,i1,i1+1,i1+1])
	jarr = np.array([j1,j1+1,j1,j1+1])
	warr = np.array([wx*wy,wx*(1.0-wy),(1.0-wx)*wy,(1.0-wx)*(1.0-wy)])
	img_out_tmp = img_in[iarr,jarr]*warr

	img_out = np.sum(img_out_tmp,axis=0)

	return img_out
#--------------------------------------------------------------------------------------------
def lq_flex_img(img_in,A,D):

	nx = np.shape(img_in)[0]
	ny = np.shape(img_in)[1]
	x1c=nx/2.0
	x2c=ny/2.0
	img_out=img_in*0.0

	ntmp=0
	for i in range(nx):
		for j in range(ny):
			dx1 = (i-x1c)
			dx2 = (j-x2c)

			xb1 = x1c
			xb2 = x2c
		
			xb1 = x1c+A[0,0]*dx1+A[0,1]*dx2 \
				 +0.5*D[0,0,0]*dx1*dx1     \
				 +0.5*D[0,0,1]*dx1*dx2     \
				 +0.5*D[0,1,0]*dx2*dx1     \
				 +0.5*D[0,1,1]*dx2*dx2
			xb2 = x2c+A[1,0]*dx1+A[1,1]*dx2 \
				 +0.5*D[1,0,0]*dx1*dx1     \
				 +0.5*D[1,0,1]*dx1*dx2     \
				 +0.5*D[1,1,0]*dx2*dx1     \
				 +0.5*D[1,1,1]*dx2*dx2

			i1 = int(xb1)
			wx = 1.-(xb1-i1)
			j1 = int(xb2)
			wy = 1.-(xb2-j1)

			iarr = np.array([i1,i1,i1+1,i1+1])
			jarr = np.array([j1,j1+1,j1,j1+1])
			warr = np.array([wx*wy,wx*(1.0-wy),(1.0-wx)*wy,(1.0-wx)*(1.0-wy)])

			if i1>=0 and i1+1<nx and j1>=0 and j1+1<ny:
				img_out[i,j]=np.sum(warr*img_in[iarr,jarr])
				#img_out[i,j]=img_in[i1,j1]
                     
                        
			#idx1 = iarr>=0
			#idx2 = iarr<nx
			#idx3 = jarr>=0
			#idx4 = jarr<ny
			#idx = idx1&idx2&idx3&idx4
			##idx = np.where(np.any(iarr>=0) and np.any(iarr<nx) \
			##	   and np.any(jarr>=0) and np.any(jarr<ny))
			##print idx
			##if len(warr[idx])==4:
			##	ntmp=ntmp+1
			##	print ntmp,img_in[iarr[idx],jarr[idx]]
			#if len(warr[idx])>0:
			#	img_out[i,j]=np.sum(warr[idx]*img_in[iarr[idx],jarr[idx]])
			#	#img_out[i,j]=img_in[i1,j1]
			#if i1>=0 and i1+1<nx and j1>=0 and j1+1<ny:
	
	return img_out
#--------------------------------------------------------------------------------------------
def lq_flex_img2(img_in,kapp,shea1,shea2,fflex1,fflex2,gflex1,gflex2):

	nx = np.shape(img_in)[0]
	ny = np.shape(img_in)[1]
	x1c=nx/2.0
	x2c=ny/2.0
	img_out=img_in*0.0

	for i in range(nx):
		for j in range(ny):
			
			
			dx2 = i-x1c
			dx1 = j-x2c

			the = dx1+dx2*1j
			thf = dx1-dx2*1j

			ffe = fflex1+fflex2*1j
			fff = fflex1-fflex2*1j
			gfe = gflex1+gflex2*1j
			gff = gflex1-gflex2*1j

			she = shea1+shea2*1j
			shf = shea1-shea2*1j

			bet = (1.0-kapp)*the-she*thf-0.25*fff*the*the \
					-0.5*ffe*the*thf-0.25*gfe*thf*thf

			xb1 = bet.real
			xb2 = bet.imag
		
			
			i1 = int(xb1)
			wx = 1.-(xb1-i1)
			j1 = int(xb2)
			wy = 1.-(xb2-j1)

			jarr = np.array([i1,i1,i1+1,i1+1])
			iarr = np.array([j1,j1+1,j1,j1+1])
			warr = np.array([wx*wy,wx*(1.0-wy),(1.0-wx)*wy,(1.0-wx)*(1.0-wy)])

			idx = np.where(np.all(iarr>=0) and np.all(iarr<nx) \
				   and np.all(jarr>=0) and np.all(jarr<ny))
			#if len(iarr[idx]) >0 and len(jarr[idx])>0:
			if i1>=0 and i1+1<nx and j1>=0 and j1+1<ny:
				#img_out[i,j]=np.sum(warr[idx]*img_in[iarr[idx],jarr[idx]])
				for k in range(4):
					img_out[i,j]=img_out[i,j] \
						+warr[k]*img_in[iarr[k],jarr[k]]
	
	return img_out
