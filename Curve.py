class Curve:

	def __init__(self, name='solution', freq=1):

		self.name = name 
		self.counter = 0
		self.freq = freq 
		self.writes = 0

	def write(self, x, *args):
		''' write to curve format for Visit ''' 

		n = len(args) 

		if (self.counter%self.freq != 0):
			self.counter += 1
			return 

		f = open(self.name+str(self.writes)+'.curve', 'w')
		for var in range(n):
			f.write('# var' + str(var) + '\n') 
			for i in range(len(x)):
				val = 0 
				if (abs(args[var][i]) > 1e-18):
					val = args[var][i]
				f.write('{} {}\n'.format(x[i], val))

		f.close()

		self.counter += 1 
		self.writes += 1