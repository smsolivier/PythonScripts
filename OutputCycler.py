import sys
import pathlib
import numpy as np 

class OutputCycler:
	def __init__(self):
		self.args = sys.argv 
		self.n = len(self.args)

		# search for .pdf and .tex strings 
		ext = ['.pdf', '.tex']
		self.paths = []
		self.opts = []
		for i in range(1, self.n):
			arg = self.args[i] 
			path = pathlib.Path(arg)
			if (path.suffix in ext):
				self.paths.append(path)
			else:
				self.opts.append(arg)

		self.count = np.zeros(len(self.paths), dtype=int)

	def Get(self, i=0):
		count = self.count[i] 
		self.count[i] += 1
		if (count==0):
			return self.paths[i]
		else:
			return self.paths[i].with_name(self.paths[i].stem + '_' + str(count) + self.paths[i].suffix)

	def GetOpt(self, i, default):
		tp = type(default)
		if (i<len(self.opts)):
			if (tp==bool):
				return True if self.opts[i]=='1' else False 
			return tp(self.opts[i])
		else:
			return default

	def Good(self, i=0):
		if (i<len(self.paths)):
			return True
		else:
			return False

if __name__=='__main__':
	oc = OutputCycler()
	if (oc.Good()):
		print(oc.Get())
		print(oc.Get())
		print(oc.Get())
	if (oc.Good(1)):
		print(oc.Get(1))
		print(oc.Get(1))
		print(oc.Get(1))