#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

class Capsaicin: 
	def __init__(self, fname):
		self.fname = fname 

		f = open(self.fname, 'r') 

		self.FCF = False 
		self.converged = False
		for line in f: 
			if ('uncollided flux source calculation' in line):
				self.FCF = True 

			if ('User-defined convergence test' in line):
				for line in f:
					if ('converged?' in line):
						spl = line.split() 
						if (spl[1]=='yes'):
							self.converged = True 
						else:
							self.converged = False 
						break 

			if ('Solution summary' in line):
				line = next(f) 
				spl = line.split() 
				self.niter = int(spl[1]) 

				line = next(f) 
				spl = line.split() 
				self.wtime = float(spl[2]) 

		# if (self.converged==False):
			# print('WARNING: ' + self.fname + ' did not converge') 

if __name__=='__main__':
	import sys 

	base = '../snow/pipe' 
	if (len(sys.argv)>1):
		base = sys.argv[1]

	fps = Capsaicin(base + '/fps.txt')  
	pbj = Capsaicin(base + '/pbj.txt') 
	pbj_fcf = Capsaicin(base + '/pbj_fcf.txt')  

	print('fps: {} iterations, {} s'.format(fps.niter, fps.wtime)) 
	print('pbj: {} iterations, {} s'.format(pbj.niter, pbj.wtime)) 
	print('pbj+fcf: {} iterations, {} s'.format(pbj_fcf.niter, pbj_fcf.wtime)) 