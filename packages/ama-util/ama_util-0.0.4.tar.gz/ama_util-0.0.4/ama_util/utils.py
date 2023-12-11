import torch
import numpy as np

## my own invention based on the mathmatical definition
def cal_gau(sizeofGau,sig,m):
    x = np.linspace(-2,2,sizeofGau)
    y = np.linspace(-2,2,sizeofGau)
    output = np.zeros((sizeofGau,sizeofGau))
    for i,x_ in enumerate(x):
        for j,y_ in enumerate(y):
            partA = 1/(2*np.pi*sig*sig)
            partB = -1*(np.square(x_-m)+np.square(y_-m))*(1/2/sig/sig)
            partC = np.exp(partB)
            output[i,j] = partA*partC
    output=torch.Tensor(output)
    return output