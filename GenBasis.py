import numpy as np 

def genBasis(p, a=0, b=1):
	N = p + 1
	x = np.linspace(a, b, N)
	coef = np.zeros((N, N))

	for k in range(N):
		A = np.zeros((N, N))
		for i in range(N):
			for j in range(N):
				A[i,j] = x[i]**j

		b = np.zeros(N)
		b[k] = 1 

		coef[k,:] = np.linalg.solve(A, b)

	B = [] 
	dB = [] 

	for i in range(N):
		B.append(np.poly1d(coef[i,::-1]))
		dB.append(B[i].deriv())

	return B, dB

def genLegendre(p):
	if (p==0):
		return np.array([0]), [np.poly1d(1)], [np.poly1d(0)]

	N = p + 1 
	x, w = np.polynomial.legendre.leggauss(N)

	coef = np.zeros((N, N))

	for k in range(N):
		A = np.zeros((N, N))
		for i in range(N):
			for j in range(N):
				A[i,j] = x[i]**j

		b = np.zeros(N)
		b[k] = 1 

		coef[k,:] = np.linalg.solve(A, b)

	B = [] 
	dB = [] 

	for i in range(N):
		B.append(np.poly1d(coef[i,::-1]))
		dB.append(B[i].deriv())

	return x, B, dB

if __name__=='__main__':
	import matplotlib.pyplot as plt 
	# B, dB = genBasis(3, -1, 1)
	nodes, B, dB = genLegendre(2) 
	x = np.linspace(-1, 1)
	for i in range(len(B)):
		plt.axvline(nodes[i], color='k', alpha=.3)
		plt.plot(x, B[i](x))

	plt.show()
