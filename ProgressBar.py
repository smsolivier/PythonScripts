import time 
import Timer

''' print a command line progress bar for a for loop ''' 

class progressbar:
	j = 0 # store iteration number 

	def __init__(self, max, TIME=False, TIME2=False, width=50):
		self.max = max # max number of iterations 
		self.width = width # width of progress bar 
		self.time = TIME
		self.time2 = TIME2 

		if (self.time):
			self.tt = Timer.timer(' ')

		# start bar 
		print('[>' + ' '*(self.width-1) + '] 0%\r', end='')
		self.prev = time.time() 

	def update(self):
		self.j += 1 # update iteration counter 

		output = lambda str: print(str, end='')

		output('[')

		percent = float(self.j)/self.max # percent complete 

		pos = int(self.width * percent) # cursor position 

		output('='*pos)

		output('>')

		output(' '*(self.width-pos-1))
		output('] ' + '{:.0f}'.format(percent*100) + '%')

		if (self.j < self.max):
			if (self.time2):
				print(' {:.3f} s/iter\r'.format(
					time.time() - self.prev), end='', flush=True)
				self.prev = time.time() 
			else:
				print('\r', end='', flush=True) # continue line 

		elif (self.j == self.max):
			if (self.time):
				self.tt.stop()
			else:
				print()
		else:
			print('too many')

if __name__=='__main__':
	N = 10
	bar = progressbar(N, True, True) 
	for i in range(N):
		time.sleep(.75) 
		bar.update() 
