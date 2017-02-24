#!/usr/bin/env python

import numpy as np 

import Timer

def TDMA(a, b, c, d):
	''' Tri diagonal matrix solver 
		Inputs:
			a:  lower diagonal 
			b:  diagonal
			c:  upper diagonal
			d:  right hand side of Ax=b
		Outputs:
			x:  solution vector 
		Notes:
			all vectors should be length N 
			a[0] should be 0
			c[N] should be 0 
	''' 
	# assert inputs in correct shape 
	assert(len(a) == len(b) and len(b) == len(c) and len(c) == len(d)) 
	N = len(d)

	# storage arrays for modified coefficients	
	p = np.zeros(N)  
	q = np.zeros(N) 

	# functions to calculate p, q
	P = lambda i:  c[i]/(b[i] - p[i-1]*a[i])
	Q = lambda i:  (d[i] - q[i-1]*a[i])/(b[i] - p[i-1]*a[i])

	p[0] = c[0]/b[0]
	q[0] = d[0]/b[0]

	# build p and q arrays 
	for i in range(1, N):
		p[i] = P(i)
		q[i] = Q(i) 

	# back sub 
	x = np.zeros(N) # solution vector 
	x[-1] = q[-1] 
	for i in range(N-2, -1, -1):
		x[i] = q[i] - p[i]*x[i+1]

	return x

def lblTDMA(aW, aE, aN, aS, ap, b, Tguess, tol=1e-3):
	''' Line by Line TDMA solver 
		Sweeps left to right, right to left, top to bottom and bottom to top 
		Compares L2 norm of solutions before and after iteration 
		Inputs:
			aW:  matrix of elements to the left of the point 
			aE:  matrix of elements to the right of the point 
			aN:  matrix of elements above the point 
			aS:  matrix of elements below the point 
			b: 	 matrix of rhs's 
			Tguess:  initial guess for solution 
			tol:  tolerance for relative change 
		Outputs:
			T:  2D array of solution values 
	'''
	Nx = np.shape(aW)[1]
	Ny = np.shape(aW)[0]

	# assert inputs in correct shape 
	assert(np.shape(aW) == np.shape(aE))
	assert(np.shape(aE) == np.shape(aN))
	assert(np.shape(aN) == np.shape(aS))
	assert(np.shape(aS) == np.shape(ap))
	assert(np.shape(ap) == np.shape(b))
	assert(np.shape(b) == np.shape(Tguess))

	T = np.copy(Tguess)

	R = 1000000 # sufficiently large to pass through first loop 

	k = 0 # iteration counter 
	tt = Timer.timer('\tTDMA Time =') # time the while loop 
	while (R > tol):
		Tguess = np.copy(T) # store previous values 

		# sweep left to right 
		rhs = aE[:,0]*T[:,1] + b[:,0] 
		T[:,0] = TDMA(-aN[:,0], ap[:,0], -aS[:,0], rhs)
		for i in range(1, Nx-1):
			rhs = aW[:,i]*T[:,i-1] + aE[:,i]*T[:,i+1] + b[:,i] 
			T[:,i] = TDMA(-aN[:,i], ap[:,i], -aS[:,i], rhs)
		rhs = aW[:,-1]*T[:,-2] + b[:,-1] 
		T[:,-1] = TDMA(-aN[:,-1], ap[:,-1], -aS[:,-1], rhs)

		# sweep right to left 
		rhs = aW[:,-1]*T[:,-2] + b[:,-1] 
		T[:,-1] = TDMA(-aN[:,-1], ap[:,-1], -aS[:,-1], rhs)
		for i in range(Nx-2, 0, -1):
			rhs = aW[:,i]*T[:,i-1] + aE[:,i]*T[:,i+1] + b[:,i]
			T[:,i] = TDMA(-aN[:,i], ap[:,i], -aS[:,i], rhs)
		rhs = aE[:,0]*T[:,1] + b[:,0]
		T[:,0] = TDMA(-aN[:,0], ap[:,0], -aS[:,0], rhs)

		# sweep top to bottom 
		rhs = aS[0,:]*T[1,:] + b[0,:] 
		T[0,:] = TDMA(-aW[0,:], ap[0,:], -aE[0,:], rhs)
		for i in range(1,Ny-1):
			rhs = aN[i,:]*T[i-1,:] + aS[i,:]*T[i+1,:] + b[i,:] 
			T[i,:] = TDMA(-aW[i,:], ap[i,:], -aE[i,:], rhs)
		rhs = aN[-1,:]*T[-2,:] + b[-1,:]
		T[-1,:] = TDMA(-aW[-1,:], ap[-1,:], -aE[-1,:], rhs) 

		# sweep bottom to top 
		rhs = aN[-1,:]*T[-2,:] + b[-1,:] 
		T[-1,:] = TDMA(-aW[-1,:], ap[-1,:], -aE[-1,:], rhs)
		for i in range(Ny-2, 0, -1):
			rhs = aN[i,:]*T[i-1,:] + aS[i,:]*T[i+1,:] + b[i,:] 
			T[i,:] = TDMA(-aW[i,:], ap[i,:], -aE[i,:], rhs)
		rhs = aS[0,:]*T[1,:] + b[0,:] 
		T[0,:] = TDMA(-aW[0,:], ap[0,:], -aE[0,:], rhs)

		R = np.linalg.norm(T - Tguess,2) # compare previous and current

		k += 1 # update counter 

		# print change and iteration number 
		fmt = '{:5}'
		print('\r' + fmt.format(R), '\t', k, end='', flush=True)
		
	tt.stop() # stop timer 
	

	return T