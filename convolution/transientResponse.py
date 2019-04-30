import math

import numpy as np

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import convolutionStrategies as cs

def lowpassFilter(nArray, K):
    return list(map(lambda n: lowpassFilterHelper(n, K) , nArray))

def lowpassFilterHelper(n, K):
    if n == 0:
        return K / 2.0
    else:
        return math.sin( (2 * math.pi * n) / K ) / ( math.pi * n)


print()
n = list(range(0, 20))
sth = lowpassFilter(n, 8)



plot([go.Scatter(x=n, y=sth, mode = 'markers')])