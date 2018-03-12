class Curve:

	def __init__(self, name, freq=1):

		self.name = name 
		self.counter = 0
		self.freq = freq 

	def write(self, x, u):
		''' write to curve format for Visit ''' 

		if (self.counter%self.freq != 0):
			self.counter += 1
			return 

		f = open(self.name+str(self.counter)+'.curve', 'w')
		f.write('# var\n') 
		for i in range(len(x)):
			f.write('{} {}\n'.format(x[i], u[i]))

		f.close()

		self.counter += 1 