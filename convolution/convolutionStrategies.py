from numpy import convolve
from scipy import signal

def numpyConvolve(x, h):
    return convolve(h, x)

def scipyConvolve(x, h):
    return signal.fftconvolve(h, x)

def naiveConvolve(x, h):
    paddingLength = (len(h)-1)
    padding = paddingLength * [0]
    paddedX = padding + x + padding

    res = []
    for n in range(paddingLength, paddingLength + len(x) + len(h) - 1):
        aggr = 0
        for k in range(0, len(h)):
            aggr += h[k] * paddedX[n - k]
        res.append(aggr)
    return res



