import numpy as np 

class matrix:
	''' prints latex matrix ''' 

	def __init__(self, A, fname, fmt='{:.2f}'):
		rows = np.shape(A)[0] # number of rows 
		cols = np.shape(A)[1] # number of columns 

		out = open(fname, 'w')

		out.write(r'\begin{matrix}' + ' \n')

		for i in range(rows):
			for j in range(cols-1):
				out.write(fmt.format(A[i,j]) + ' & ') 

			if (i == rows-1):
				out.write(fmt.format(A[i,-1]) + ' \n')
			else:
				out.write(fmt.format(A[i,-1]) + ' \\\\\n')

		out.write(r'\end{matrix}' + ' \n')

		out.close()

if __name__ == '__main__':
	import numpy as np 

	A = np.random.random((3,3))

	matrix(A, 'trix.tex')