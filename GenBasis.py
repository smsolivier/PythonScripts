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

	x2 = np.linspace(-1, 1)
	for i in range(N):
		B.append(np.poly1d(coef[i,::-1]))
		dB.append(B[i].deriv())

	return B, dB

if __name__=='__main__':
	B, dB = genBasis(3, -1, 1) 
	for i in range(len(B)):
		print(B[i]) 
