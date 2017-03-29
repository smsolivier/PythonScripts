#!/usr/bin/env python

import numpy as np

''' first order derivative solvers 
	Includes: 
		forward euler
		backward euler 
		crank nicolson 
		TBDF2
''' 

def forwardEuler(A, f0, dt, tend, tstart=0):
	''' Solves the system df/dt = Af using the forward euler method. 
		Uses uniform time steps 
		Inputs:
			A:  matrix A 
			f0: initial condition at t=0
			dt: time step 
			tend: ending time 
		Outputs:
			t:  time where solution is evaluated 
			f:  array of solutions 
	''' 
	N = int((tend - tstart)/dt) + 1 # number of time steps 
	t = np.linspace(tstart, tend, N)

	f = np.zeros((N, np.shape(A)[0])) # array to hold solution vector 
	f[0,:] = f0 # initial condition 
	for i in range(1, N):
		f[i,:] = np.dot(np.identity(np.shape(A)[0]) + A*dt, f[i-1,:]) # (I + Adt)f^n 

	return t, f 

def backwardEuler(A, f0, dt, tend):
	''' Solves the system df/dt = Af using the backward euler method 
		Uses uniform time steps 
		Inputs:
			A:  matrix A 
			f0: initial condition at t=0
			dt: time step 
			tend: ending time 
		Outputs:
			t:  time where solution is evaluated 
			f:  array of solutions 
	''' 
	N = int(tend/dt) + 1 # number of time steps 
	t = np.linspace(0, tend, N)

	f = np.zeros((N, np.shape(A)[0])) # solution array 
	f[0,:] = f0 # initial condition 

	for i in range(1, N):
		# f^n+1 = (I - Adt)f^n 
		f[i,:] = np.linalg.solve(np.identity(np.shape(A)[0]) - A*dt, f[i-1,:])

	return t, f 

def crank(A, f0, dt, tend):
	''' Solves the system df/dt = Af using the crank nicolson method 
		Uses uniform time steps 
		Inputs:
			A:  matrix A 
			f0: initial condition at t=0
			dt: time step 
			tend: ending time 
		Outputs:
			t:  time where solution is evaluated 
			f:  array of solutions 
	''' 
	N = int(tend/dt) + 1# number of time steps 
	t = np.linspace(0, tend, N)

	f = np.zeros((N, np.shape(A)[0]))
	f[0,:] = f0 # initial condition 

	for i in range(1, N):
		# solve (I - .5Adt)f^n+1 = (I + .5Adt)f^n 
		f[i,:] = np.linalg.solve(np.identity(np.shape(A)[0]) - .5*A*dt, 
			np.dot(np.identity(np.shape(A)[0]) + .5*A*dt, f[i-1,:]))

	return t, f

def TBDF2(A, f0, dt, tend):
	''' Solves the system df/dt = Af using the TBDF2 method  
		Uses uniform time steps 
		Inputs:
			A:  matrix A 
			f0: initial condition at t=0
			dt: time step 
			tend: ending time 
		Outputs:
			t:  time where solution is evaluated 
			f:  array of solutions 
	''' 
	size = np.shape(A)[0] # number of equations 
	N = int(tend/dt) + 1
	t = np.linspace(0, tend, N)

	f = np.zeros((N, np.shape(A)[0]))
	f[0,:] = f0 # initial condition 

	for i in range(1, N):
		# CN between i and i+1/2 
		fhalf = np.linalg.solve(np.identity(size) - .25*A*dt, 
			np.dot(np.identity(size) + .25*A*dt, f[i-1,:]))

		# trapezoidal between i, i+1/2 and i+1 
		f[i,:] = np.linalg.solve(np.identity(size) - 1/3*A*dt, 
			4/3*fhalf - 1/3*f[i-1,:])

	return t, f

def checkOrder(func):
	''' returns the order of convergence for solver func 
		solves df/dt = -f 
		compares to solution f = e^-t 
	''' 
	A = np.ones(1)

	f0 = np.ones(1)

	dt = np.array([.1, .01, .001])

	g = np.zeros(len(dt))
	for i in range(len(dt)):
		print(dt[i])
		t, f = func(-A, f0, dt[i], 1)

		g[i] = np.fabs(f[-1] - np.exp(-1))

	fit = np.polyfit(np.log(dt), np.log(g), 1)
	print(fit[0])

def lagged(A, f0, dt, tend): 
	''' Solves 
			df/dt = A(t, f) f 
		using lagged TBDF2
		Inputs:
			A:    matrix lambda function of t and f 
			f0:   initial conditions 
			dt:   time step 
			tend: ending time 
		Outputs:
			t: 	time of solutions 
			f:  solution as a function of time 
	''' 
	size = len(f0) # number of equations 
	N = int(tend/dt) + 1 # number of time steps 

	t = np.linspace(0, tend, N) # array of times 

	f = np.zeros((N, size)) # solution vector 
	f[0,:] = f0 # initial conditions 

	I = np.identity(size) # identity matrix 

	for i in range(1, N):
		fn = f[i-1,:] # store previous solution 

		# CN
		# solve (I - A*dt/4) f_n+1 = (I + A*dt/4) f_n 
		fhalf = np.linalg.solve(I - A(t[i]+dt/2, fn)*dt/4, np.dot(I + A(t[i], fn)*dt/4, fn))

		# TBDF 
		# solve (3I - Adt) f_n+1 = 4f_n+1/2 - f_n 
		f[i,:] = np.linalg.solve(3*I - A(t[i]+dt, fn)*dt, 4*fhalf - f[i-1,:])

	return t, f

def picard(A, f0, dt, tend, maxIter=100, tol=1e-8):
	''' Solves 
			df/dt = A(t, f) f 
		using fully iterated Picard TBDF-2 
		Inputs:
			A:    matrix lambda function of t, f 
			f0:   initial conditions 
			dt:   time step 
			tend: ending time 
		Outputs:
			t: 	time of solutions 
			f:  solution as a function of time 
	''' 
	size = len(f0) # number of equations
	N = int(tend/dt) + 1 # number of time steps 

	t = np.linspace(0, tend, N) # times 

	f = np.zeros((N,size)) # store solution 
	f[0,:] = f0 # initial conditions 

	I = np.identity(size) # identity matrix 

	# lambda function for computing L2 norms 
	criterion = lambda fnew, fold:  np.linalg.norm(fnew - fold, 2)/np.linalg.norm(fnew)

	for i in range(1, N): # loop through time steps 
		fn = f[i-1,:] # previous values 

		# converge f_n+1/2 
		fstar = np.copy(fn) # initialize at previous value 
		for j in range(maxIter): # iterate 

			# update fhalf 
			fhalf = np.linalg.solve(I - A(t[i]+dt/2, fstar)*dt/4, np.dot(I + A(t[i], fn)*dt/4, fn))

			# break iteration loop if criterion met, more than 2 iterations 
			if (criterion(fhalf, fstar) < tol and j > 2):
				break 

			fstar = np.copy(fhalf) # update fstar for next iteration 

		# if max iterations reached 
		if (j == maxIter - 1):
			print('max iterations reached')

		# iterate f_n+1 
		fold = np.copy(fhalf) # initialize as half value 
		for j in range(maxIter): # iterate 

			# update f 
			f[i,:] = np.linalg.solve(3*I - A(t[i]+dt, fold)*dt, 
				4*fhalf - fn)

			# break iteration loop if criterion met, more than 2 iterations 
			if (criterion(f[i,:], fold) < tol and j > 2):
				break 

			fold = np.copy(f[i,:]) # update fold 

		# if max iterations reached 
		if (j == maxIter - 1):
			print('max iterations reached')

	return t, f 

# --------- MMS for non-linear PRKEs --------
if __name__ == "__main__":
	# execute only if script 

	N0 = 1 
	lam = .08 
	Lam = 6e-5 
	Nref = 1 
	beta = .0075 
	C0 = beta*N0/(Lam*lam)
	alpha = 2*beta

	omega = 1

	tend = 1

	rho = lambda t, f:  alpha*N0*np.exp(-omega*t)/Nref - omega*Lam + \
		beta*omega/(lam - omega)*(np.exp((omega-lam)*t) - 1) - alpha*f[0]/Nref

	A = lambda t, f:  np.array([((rho(t, f) - beta)/Lam, lam), 
		(beta/Lam, -lam)])

	# dt = np.array([.0001, .001, .01, .1])
	dt = np.array([.0001, .0002, .0004])
	err_lag = np.zeros(len(dt))
	err_pic = np.zeros(len(dt))
	ex = np.exp(-omega*tend) # exact solution

	for i in range(len(dt)):
		t, f = picard(A, np.array([N0, C0]), dt[i], tend)
		err_pic[i] = np.fabs(ex - f[-1,0])/ex
		# err_pic[i] = np.linalg.norm(np.exp(-omega*t) - f[:,0], 2)

		t, f = lagged(A, np.array([N0, C0]), dt[i], tend)
		err_lag[i] = np.fabs(ex - f[-1,0])/ex
		# err_lag[i] = np.linalg.norm(np.exp(-omega*t) - f[:,0], 2)

	fit_pic = np.polyfit(np.log(dt), np.log(err_pic), 1)
	fit_lag = np.polyfit(np.log(dt), np.log(err_lag), 1)

	print('N_pic =', fit_pic[0])
	print('N_lag =', fit_lag[0])

	plt.loglog(dt, err_pic, label='Picard')
	plt.loglog(dt, err_lag, label='Lagged')
	plt.legend(loc='best')
	plt.show()