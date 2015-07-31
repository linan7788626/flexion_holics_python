import numpy as np
import lensdemo_funcs as ldf
from matplotlib.pylab import *
from lens_image import *
#------------------------------------------------------------------------------------------
def flex_m(img_in,w_in,sig2_in):
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
	
	Q111  =  np.sum((x_in-xc)**3*img_in)/fu
	Q112  =  np.sum((x_in-xc)**2*(y_in-yc)*img_in)/fu
	Q122  =  np.sum((x_in-xc)*(y_in-yc)**2*img_in)/fu
	Q222  =  np.sum((y_in-yc)**3*img_in)/fu
	
	Q1111 =  np.sum((x_in-xc)**4*img_in)/fu
	Q1112 =  np.sum((x_in-xc)**3*(y_in-yc)*img_in)/fu
	Q1122 =  np.sum((x_in-xc)**2*(y_in-yc)**2*img_in)/fu
	Q1222 =  np.sum((x_in-xc)*(y_in-yc)**3*img_in)/fu
	Q2222 =  np.sum((y_in-yc)**4*img_in)/fu
	
	# Go 6th moments!
	Q111111= np.sum((x_in-xc)**6*img_in)/fu
	Q111112= np.sum((x_in-xc)**5*(y_in-yc)*img_in)/fu
	Q111122= np.sum((x_in-xc)**4*(y_in-yc)**2*img_in)/fu
	Q111222= np.sum((x_in-xc)**3*(y_in-yc)**3*img_in)/fu
	Q112222= np.sum((x_in-xc)**2*(y_in-yc)**4*img_in)/fu
	Q122222= np.sum((x_in-xc)*(y_in-yc)**5*img_in)/fu
	Q222222= np.sum((y_in-yc)**6*img_in)/fu
#------------------------------------------------------------------------------------
	
	xi = Q1111+2.0*Q1122+Q2222
	
	zita1 = (Q111+Q122)/xi
	zita2 = (Q112+Q222)/xi
	
	delta1 = (Q111-3.0*Q122)/xi
	delta2 = (3.0*Q112-Q222)/xi
	
	ita1 = (Q1111-Q2222)/xi
	ita2 = 2.0*(Q1112+Q1222)/xi
	
	lambda1 = (Q1111-6.0*Q1122+Q2222)/xi
	lambda2 = 4.0*(Q1112-Q1222)/xi
	
	vixi = 4.0*xi
#-----------------------------------------------------------------------
	m00 = 0.25*(9.0+8.0*ita1)
	m01 = 0.25*(8.0*ita2)
	m02 = 0.25*(2.0*ita1+lambda1)
	m03 = 0.25*(2.0*ita2+lambda2)
	
	m10 = 0.25*(8.0*ita2)
	m11 = 0.25*(-8.0*ita1+9.0)
	m12 = 0.25*(-2.0*ita2+lambda2)
	m13 = 0.25*(2.0*ita1-lambda1)
	
	m20 = 0.25*(10.0*ita1+7.0*lambda1)
	m21 = 0.25*(-10.0*ita2+7.0*lambda2)
	m22 = 0.25*(3.0)
	m23 = 0.0
	
	m30 = 0.25*(10.0*ita2+7.0*lambda2)
	m31 = 0.25*(10.0*ita1-7.0*lambda1)
	m32 = 0.0
	m33 = 0.25*(3.0)
	
	# Now, put in all of the corrections due to the shift in centroid
	m00=m00-(33*Q11**2+14*Q11*Q22+Q22**2+20*Q12**2)/(4.*xi)
	m01=m01-(32*Q12*Q22+32*Q11*Q12)/(4.*xi)
	m02=m02-(3*Q11**2-2*Q11*Q22-Q22**2-4*Q12**2)/(4.*xi)
	m03=m03-(2*Q11*Q12)/xi
	
	m10=m10-(32*Q12*Q22+32*Q11*Q12)/(4*xi)
	m11=m11-(Q11**2+14*Q11*Q22+20*Q12**2+33*Q22**2)/(4.*xi)
	m12=m12-(-2*Q12*Q22)/xi
	m13=m13-(Q11**2+4*Q12**2+Q11*Q22-3*Q22**2)/(4.*xi)
	
	m20=m20-3*(11*Q11**2-10*Q11*Q22-Q22**2-20*Q12**2)/(4.*xi)
	m21=m21-3*(8*Q11*Q12-32*Q12*Q22)/(4.*xi)
	m22=m22-3*(-2*Q11*Q22+Q11**2+Q22**2+4*Q12**2)/(4.*xi)
	m23=m23-0.
	
	m30=m30-3*(32*Q11*Q12-8*Q12*Q22)/(4.*xi)
	m31=m31-3*(Q11**2+20*Q12**2+10*Q11*Q22-11*Q22**2)/(4.*xi)
	m32=m32-0.
	m33=m33-3*(-2*Q11*Q22+Q11**2+Q22**2+4*Q12**2)/(4.*xi)
#-----------------------------------------------------------------------
	denom = 4.*xi*sig2_in
	#Put in the corrections due to finite aperture
	m00 = m00-(3*Q111111+6*Q111122+3*Q112222)/denom
	m01 = m01-(3*Q111112+6*Q111222+3*Q122222)/denom
	m02 = m02-(1*Q111111-2*Q111122-3*Q112222)/denom
	m03 = m03-(3*Q111112+2*Q111222-1*Q122222)/denom
	
	m10 = m10-(3*Q111112+6*Q111222+3*Q122222)/denom
	m11 = m11-(3*Q111122+6*Q112222+3*Q222222)/denom
	m12 = m12-(1*Q111112-2*Q111222-6*Q122222)/denom
	m13 = m13-(3*Q111122+2*Q112222-1*Q222222)/denom
	
	m20 = m20-(3*Q111111-6*Q111122-9*Q112222)/denom
	m21 = m21-(3*Q111112-6*Q111222-9*Q122222)/denom
	m22 = m22-(1*Q111111-6*Q111122+9*Q112222)/denom
	m23 = m23-(3*Q111112-10*Q111222+3*Q122222)/denom
	
	m30 = m30-(9*Q111112+6*Q111222-3*Q122222)/denom
	m31 = m31-(9*Q111122+6*Q112222-3*Q222222)/denom
	m32 = m32-(3*Q111112-10*Q111222+3*Q122222)/denom
	m33 = m33-(9*Q111122-6*Q112222+1*Q222222)/denom
	
	#Put in the new corrections for the limited mask
	
	m00=m00-(-3*Q22*Q1122-9*Q11*Q1111-6*Q12*Q1112-9*Q11*Q1122-6*Q12*Q1222-3*Q22*Q1111)/denom
	m01=m01-(-3*Q22*Q1112-9*Q11*Q1222-3*Q22*Q1222-6*Q12*Q1122-9*Q11*Q1112-6*Q12*Q2222)/denom
	m02=m02-(3*Q22*Q1122-3*Q11*Q1111-2*Q12*Q1112+9*Q11*Q1122+6*Q12*Q1222-Q22*Q1111)/denom
	m03=m03-(-6*Q12*Q1122-9*Q11*Q1112+3*Q11*Q1222-3*Q22*Q1112+Q22*Q1222+2*Q12*Q2222)/denom
	
	m10=m10-(-6*Q12*Q1122-3*Q11*Q1112-9*Q22*Q1112-3*Q11*Q1222-9*Q22*Q1222-6*Q12*Q1111)/denom
	m11=m11-(-6*Q12*Q1112-3*Q11*Q2222-6*Q12*Q1222-9*Q22*Q1122-3*Q11*Q1122-9*Q22*Q2222)/denom
	m12=m12-(6*Q12*Q1122-Q11*Q1112-3*Q22*Q1112+3*Q11*Q1222+9*Q22*Q1222-2*Q12*Q1111)/denom
	m13=m13-(-9*Q22*Q1122-3*Q11*Q1122+Q11*Q2222-6*Q12*Q1112+2*Q12*Q1222+3*Q22*Q2222)/denom
	
	m20=m20+3*(-3*Q22*Q1122+3*Q11*Q1111-6*Q12*Q1112+3*Q11*Q1122-6*Q12*Q1222-3*Q22*Q1111)/denom
	m21=m21+3*(-3*Q22*Q1112+3*Q11*Q1222-3*Q22*Q1222-6*Q12*Q1122+3*Q11*Q1112-6*Q12*Q2222)/denom
	m22=m22+3*(3*Q22*Q1122+Q11*Q1111-2*Q12*Q1112-3*Q11*Q1122+6*Q12*Q1222-Q22*Q1111)/denom
	m23=m23+3*(-6*Q12*Q1122+3*Q11*Q1112-Q11*Q1222-3*Q22*Q1112+Q22*Q1222+2*Q12*Q2222)/denom
	
	m30=m30-3*(-6*Q12*Q1122-3*Q11*Q1112+3*Q22*Q1112-3*Q11*Q1222+3*Q22*Q1222-6*Q12*Q1111)/denom
	m31=m31-3*(-6*Q12*Q1112-3*Q11*Q2222-6*Q12*Q1222+3*Q22*Q1122-3*Q11*Q1122+3*Q22*Q2222)/denom
	m32=m32-3*(6*Q12*Q1122-Q11*Q1112+Q22*Q1112+3*Q11*Q1222-3*Q22*Q1222-2*Q12*Q1111)/denom
	m33=m33-3*(3*Q22*Q1122-3*Q11*Q1122+Q11*Q2222-6*Q12*Q1112+2*Q12*Q1222-Q22*Q2222)/denom
	
#---------------------------------------------------------------------------------
	mm = np.array([[m00,m01,m02,m03]\
		      ,[m10,m11,m12,m13]\
		      ,[m20,m21,m22,m23]\
		      ,[m30,m31,m32,m33]])
	
	ym = np.array([zita1,zita2,delta1,delta2])
	ff = np.ones((4))
	ff = np.linalg.solve(mm,ym)
	gdenom = Q11+Q22+2.0*np.sqrt(Q11*Q22-Q12**2.0)
	gam1 = (Q11-Q22)/gdenom
	gam2 = 2.0*Q12/gdenom
	gamma_moments=np.array([gam1,gam2])
	return ff,gamma_moments
