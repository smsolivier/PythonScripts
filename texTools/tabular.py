import numpy as np 
import copy

class Tabular:
	def __init__(self, *args):
		self.df = []
		self.fmt = []
		self.head = [] 
		self.head_fmt = [] 
		self.cgroup = [] 
		self.rgroup = [] 
		self.break_after = [] 
		self.rgt = ''
		self.note = ''
		self.rhighlight = [] 
		self.chighlight = [] 
		self.fade_color = ''
		self.SetHeader(*args) 
		
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

	def SetRowEmphasis(self, *rows):
		self.rhighlight = [] 
		for n in range(len(rows)):
			self.rhighlight.append(rows[n])

	def SetColEmphasis(self, *cols):
		self.chighlight = [] 
		for n in range(len(cols)):
			self.chighlight.append(cols[n])

	def SetFadeColor(self, color):
		self.fade_color = color

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
		head = self.head.copy()
		assert(len(head)>0)
		head_fmt = self.head_fmt.copy()
		df = copy.deepcopy(self.df) # deep copy since list of lists
		fmt = copy.deepcopy(self.fmt)
		break_after = self.break_after.copy()
		cgroup = self.cgroup.copy()
		if (len(self.rgroup)):
			head.insert(0, self.rgt)
			head_fmt.insert(0, '{}') 
			for i in range(len(df)):
				df[i].insert(0, '') 
				fmt[i].insert(0, '{}') 
			for i in range(len(cgroup)):
				cgroup[i] = (cgroup[i][0], cgroup[i][1]+1, cgroup[i][2]+1) 
			for i in range(len(break_after)):
				break_after[i] += 1 

			for group in self.rgroup:
				if (group[3]):
					text = r'\rotatebox{90}{' + group[0] + '}'
				else: 
					text = group[0] 
				df[group[1]][0] = r'\multirow{' + str(group[2]-group[1]) + '}{*}{' + text + '}'
		h = len(df) 
		w = len(head) 

		row_fade = np.zeros(h, dtype=bool)
		if (self.rhighlight):
			for r in self.rhighlight:
				row_fade[r] = True
			row_fade = np.invert(row_fade)
		col_fade = np.zeros(w, dtype=bool)
		if (self.chighlight):
			for c in self.chighlight:
				col_fade[c] = True
			col_fade = np.invert(col_fade)
		fade = np.zeros((h,w), dtype=bool)
		for i in range(h):
			for j in range(w):
				fade[i,j] = (row_fade[i] or col_fade[j])
		if (self.rgroup):
			fade[:,0] = False

		cbreak = np.ones(w, dtype=int) 
		for i in range(len(cgroup)):
			cbreak[cgroup[i][2]-1] += 1 
		for i in range(len(break_after)):
			cbreak[break_after[i]] += 1
		cbreak[-1] = 0
		rbreak = np.ones(h, dtype=int)
		for group in self.rgroup:
			rbreak[group[2]-1] += 1 
		rbreak[-1] = 1 

		s = r'\begin{tabular}{' + 'c'*(sum(cbreak)+2) + '}\n\\toprule\n'
		if (len(cgroup)):
			loc = np.zeros(w, dtype=int) - 1 
			for i in range(len(cgroup)):
				group = cgroup[i]
				loc[group[1]] = i 
				loc[group[1]+1:group[2]-1] = -2 
			i = 0
			for idx in loc:
				if (idx==-1):
					s += ' & '*cbreak[i]
				elif (idx>=0):
					group = cgroup[idx] 
					s += '\\multicolumn{' + str(group[2] - group[1]) + '}{c}{' + group[0] + '} '

				i += 1

			s += '\\\\\n'
			for i in range(len(cgroup)):
				group = cgroup[i] 
				true_start = sum(cbreak[:group[1]+1])
				true_end = true_start + group[2] - group[1] - 1 
				s += r'\cmidrule{' + str(true_start) + '-' + str(true_end) + '}'
			s += '\n'

		for i in range(w):
			if (fade[:,i].all()):
				s += ('\\textcolor{{' + self.fade_color + '}}{{' + head_fmt[i] + '}}').format(head[i])
			else:
				s += head_fmt[i].format(head[i])
			s += ' ' + '& '*cbreak[i]
		s += '\\\\\n\\midrule\n'

		for i in range(h):
			if (len(df[i])==0):
				s += '\\addlinespace\n'
			else:	
				for j in range(w):
					if (fade[i,j]):
						s += ('\\textcolor{{' + self.fade_color + '}}{{' + fmt[i][j] + '}}').format(df[i][j])
					else:
						s += fmt[i][j].format(df[i][j])
					s += ' ' + '& '*cbreak[j]
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