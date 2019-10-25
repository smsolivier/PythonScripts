''' create a latex format table ''' 

import texTools.utils as utils

class table:
	''' Makes a Latex formatted table ''' 

	str = '' # stores table 

	def addLine(self, *args):
		''' stores list of values into str with & between and \\ \n at the end ''' 
		
		n = len(args)

		for i in range(n - 1):
			self.str += args[i] + ' & ' # add args to str

		self.str += args[-1] + ' \\\\\n'

	def addRow(self, name, array, fmt, hline=False):
		self.str += name + ' & ' 
		for i in range(len(array)-1):
			self.str += utils.writeNumber(array[i], fmt) + ' & '

		self.str += utils.writeNumber(array[-1], fmt) + ' \\\\\n'
		if (hline):
			self.str += r'\hline' 

	def save(self, outName='macros.tex'):
		''' Saves str to file outName ''' 

		out = open(outName, 'w')

		out.write(self.str)

		out.close()

		print('created table ', outName)

		self.str = '' # reset str 

if __name__ == '__main__':
	t = table()

	t.addLine('lineName', 'hello', 'world')
	t.addLine('test2', 'test2')
	a = [0,1,2]
	t.addRow('arange', a, '{:.1f}')

	t.save()