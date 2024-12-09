#% ------------------------------------------------------------------------%
#% This function is used to sample a set of evenly distributed weight
#% vectors from a unit simplex according to the NBI paper.
#%
#% Author: Dr. Ke Li
#% Affliation: CODA Group @ University of Exeter
#% Contact: k.li@exeter.ac.uk || https://coda-group.github.io/
#% ------------------------------------------------------------------------%
import numpy as np
import math

def setweight(w, c, v, unit, add, objdim, dim):
    if (dim == objdim):
        v = np.zeros(objdim)
    if (dim == 1):
        c       = c + 1
        v[0]    = unit - add
        w[:, c - 1]  = v
        return w, c 

    for i in range(int(unit - add) + 1):
        v[dim - 1]  = i
        w, c    = setweight(w, c, v, unit, add + i, objdim, dim - 1);
    return w, c
#%%
def noweight(unit, add, dim):
    M = 0
    if (dim == 1):
        M = 1
        return M
    for i in range(int(unit - add) + 1):
        M = M + noweight(unit, add + i, dim - 1)
    return M

#%%
def initweight(objDim, N):
    U = math.floor(N**(1/(objDim-1)))-2
    M = 0
    while (M < N):
        U = U + 1
        M = noweight(U, 0, objDim)

    W      = np.zeros((objDim, M))
    C      = 0
    V      = np.zeros(objDim)
    W, C   = setweight(W, C, V, U, 0, objDim, objDim)
    W      = W / (U + 0.0)

    pos     = (W < 1.0E-5)
    W[pos]  = 1.0E-5
    return W



