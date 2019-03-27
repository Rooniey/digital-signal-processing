from operations import computeSignal
from utility import pluck
import numpy as np

n = 1000
fp = 1000

def calculateStatistics():
    return NONE

def computeIntegral(signal):
    params = signal["params"]
    t1 = params["t1"]
    x = None
    if signal["isPeriodic"]:
        T =  params["T"]
        x = np.linspace(t1, t1+T, n)
    else:
        d = params["d"]
        x = np.linspace(t1, t1+d, int(fp*d))
    
    h = abs(x[1] - x[0]) 
    y = computeSignal(signal, x)
    data = sum(y[1:]) + sum(y[:-1])
    return (h/2)*data


