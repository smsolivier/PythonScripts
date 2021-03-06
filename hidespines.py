from matplotlib import rc 

''' Make matplotlib plots look nice 
	Remove right and top axes 
	changes label font 
	changes label size 
''' 

def hidespines(ax, ticksize=0):
	rc('font',**{'family':'sans-serif','sans-serif':['Times']})
	ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.xaxis.set_ticks_position('bottom')
	ax.yaxis.set_ticks_position('left')
	if (ticksize != 0):
		ax.xaxis.set_tick_params(labelsize=ticksize)
		ax.yaxis.set_tick_params(labelsize=ticksize)
