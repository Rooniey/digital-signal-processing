import convolution.convolutionStrategies as cs

def convCorrelation(x, h):
    reversedH = h[::-1]
    return cs.numpyConvolve(x, reversedH)

def correlation(x, h):
    paddingLength = (len(h)-1)
    padding = paddingLength * [0]
    paddedX = padding + x + padding

    res = []
    for n in range(paddingLength, paddingLength + len(x) + len(h) - 1):
        aggr = 0
        for k in range(0, len(h)):
            aggr += h[k] * paddedX[k - n]
        res.append(aggr)
    return res

