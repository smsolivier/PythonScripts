class Curve:

	def __init__(self, name):

		self.name = name 
		self.counter = 0

	def write(self, x, u):
		''' write to curve format for Visit ''' 

		f = open(self.name+str(self.counter)+'.curve', 'w')
		f.write('# var\n') 
		for i in range(len(x)):
			f.write('{} {}\n'.format(x[i], u[i]))

		f.close()

		self.counter += 1 