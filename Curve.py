class Curve:

	def __init__(self, name='solution', freq=1):

		self.name = name 
		self.counter = 0
		self.freq = freq 

	def write(self, x, *args):
		''' write to curve format for Visit ''' 

		n = len(args) 

		if (self.counter%self.freq != 0):
			self.counter += 1
			return 

		f = open(self.name+str(self.counter)+'.curve', 'w')
		for var in range(n):
			f.write('# var' + str(var) + '\n') 
			for i in range(len(x)):
				f.write('{} {}\n'.format(x[i], args[var][i]))

		f.close()

		self.counter += 1 