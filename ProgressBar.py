import time 
import Timer
class progressbar:
	j = 0 # store iteration number 

	def __init__(self, max, time=False, width=50):
		self.max = max # max number of iterations 
		self.width = width # width of progress bar 
		self.time = time

		if (self.time):
			self.tt = Timer.timer(' ')

		# start bar 
		print('[>' + ' '*self.width + '] 0%\r', end='')

	def update(self):
		self.j += 1 # update iteration counter 

		output = lambda str: print(str, end='')

		output('[')

		percent = float(self.j)/self.max # percent complete 

		pos = int(self.width * percent) # cursor position 

		output('='*pos)

		output('>')

		output(' '*(self.width-pos))
		output('] ' + '{:.0f}'.format(percent*100) + '%')

		if (self.j == self.max):
			if (self.time):
				self.tt.stop()
			else:
				print()
		else:
			print('\r', end='', flush=True) # continue line 
