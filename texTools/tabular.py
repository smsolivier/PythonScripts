import numpy as np 

class Tabular:
	def __init__(self):
		self.df = []
		self.fmt = []
		self.head = [] 
		self.head_fmt = [] 
		self.cgroup = [] 
		self.rgroup = [] 
		self.break_after = [] 
		self.rgt = ''
		self.note = ''
		
	def AddRow(self, *args):
		row, fmt = self.Parse(args) 
		self.df.append(row)
		self.fmt.append(fmt) 

	def AddLineSpace(self):
		self.df.append([])
		self.fmt.append([]) 

	def SetHeader(self, *args):
		self.head, self.head_fmt = self.Parse(args)

	def SetRowGroupTitle(self, title):
		self.rgt = title 

	def AddColumnGroup(self, name, start, width):
		self.cgroup.append((name, start, start+width)) 

	def AddColumnBreak(self, c):
		self.break_after.append(c) 

	def AddRowGroup(self, name, start, height, rot=True):
		self.rgroup.append((name, start, start+height, rot))

	def AddNote(self, note):
		self.note = note

	def Parse(self, args):
		n = len(args)
		row = [] 
		fmt = [] 
		for i in range(n):
			if (isinstance(args[i], tuple)):
				row.append(args[i][0])
				fmt.append(args[i][1]) 
			else:
				row.append(args[i])
				fmt.append('{}')
		return row, fmt 

	def __str__(self):
		head = self.head 
		assert(len(head)>0)
		head_fmt = self.head_fmt 
		df = self.df 
		fmt = self.fmt 
		if (len(self.rgroup)):
			head.insert(0, self.rgt)
			head_fmt.insert(0, '{}') 
			for i in range(len(df)):
				df[i].insert(0, '') 
				fmt[i].insert(0, '{}') 
			for i in range(len(self.cgroup)):
				self.cgroup[i] = (self.cgroup[i][0], self.cgroup[i][1]+1, self.cgroup[i][2]+1) 
			for i in range(len(self.break_after)):
				self.break_after[i] += 1 

			for group in self.rgroup:
				if (group[3]):
					text = r'\rotatebox{90}{' + group[0] + '}'
				else: 
					text = group[0] 
				df[group[1]][0] = r'\multirow{' + str(group[2]-group[1]) + '}{*}{' + text + '}'

		h = len(df) 
		w = len(head) 

		cbreak = np.ones(w, dtype=int) 
		for i in range(len(self.cgroup)):
			cbreak[self.cgroup[i][2]-1] += 1 
		for i in range(len(self.break_after)):
			cbreak[self.break_after[i]] += 1
		cbreak[-1] = 0
		rbreak = np.ones(h, dtype=int)
		for group in self.rgroup:
			rbreak[group[2]-1] += 1 
		rbreak[-1] = 1 

		s = r'\begin{tabular}{' + 'c'*(sum(cbreak)+2) + '}\n\\toprule\n'
		if (len(self.cgroup)):
			loc = np.zeros(w, dtype=int) - 1 
			for i in range(len(self.cgroup)):
				group = self.cgroup[i]
				loc[group[1]] = i 
				loc[group[1]+1:group[2]-1] = -2 
			i = 0
			for idx in loc:
				if (idx==-1):
					s += ' & '*cbreak[i]
				elif (idx>=0):
					group = self.cgroup[idx] 
					s += '\\multicolumn{' + str(group[2] - group[1]) + '}{c}{' + group[0] + '} '

				i += 1

			s += '\\\\\n'
			for i in range(len(self.cgroup)):
				group = self.cgroup[i] 
				true_start = sum(cbreak[:group[1]+1])
				true_end = true_start + group[2] - group[1] - 1 
				s += r'\cmidrule{' + str(true_start) + '-' + str(true_end) + '}'
			s += '\n'

		for i in range(w):
			s += head_fmt[i].format(head[i]) + ' ' + '& '*cbreak[i]
		s += '\\\\\n\\midrule\n'

		for i in range(h):
			if (len(df[i])==0):
				s += '\\addlinespace\n'
			else:	
				for j in range(w):
					s += fmt[i][j].format(df[i][j]) + ' ' + '& '*cbreak[j]
				s += '\\\\\n'
				if (rbreak[i]>1):
					s += '\\addlinespace\n'

		s += '\\bottomrule\n\\end{tabular}'
		if (self.note):
			s += '\\\\\n' + self.note 
		return s 

	def Write(self, outname):
		f = open(outname, 'w')
		f.write(str(self))
		f.close() 
		print('created table', outname)