from .config import R_IS_INSTALLED, RPY2_IS_INSTALLED, RPY2_ERROR_MESSAGE, \
    USAGE_MESSAGE, FLOATMATRIX, FLOATVECTOR, R_NULL
from rpy2.robjects.packages import importr

base = importr("base")
stats = importr("stats")
esgtoolkit = importr("esgtoolkit")

def calculatereturns(x):
    """Calculate returns from a time series 

    """
    if not R_IS_INSTALLED:
        raise ImportError("R is not installed! \n" + USAGE_MESSAGE)
        
    if not RPY2_IS_INSTALLED:
        raise ImportError(RPY2_ERROR_MESSAGE + USAGE_MESSAGE)        
    
    z = stats.ts(FLOATVECTOR(x)) # will need to add frequency and handle multi-dimensional arrays

    # convert z to something that can be used in R 
    return z #config.ESGTOOLKIT_PACKAGE.calculatereturns(z)