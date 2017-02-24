import numpy as np 

def rsquared(y, f):
    ''' returns the R^2 value 
        Inputs:
          y: actual values 
          f: values from fit
    ''' 
    ybar = np.mean(y)

    sumsqy = np.sum((y-ybar)**2) 
    sumsqf = np.sum((f - ybar)**2)
    sumres = np.sum((y-f)**2)

    r = 1 - sumres/sumsqy

    return r
