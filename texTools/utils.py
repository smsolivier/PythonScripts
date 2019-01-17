''' general utilities for texTools ''' 

def writeNumber(x, fmt='{:.3f}'):
	''' Returns the string in Latex format: 
			\num{fmt.format(x)} 
	''' 
	return '\\num{' + fmt.format(x) + '}' 
