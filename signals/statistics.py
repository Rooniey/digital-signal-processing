from signals.signalGenerator import computeSignal
from commons.utility import pluck
import numpy as np
import math

n = 1000
fp = 1000

def calculateStatistics(signal):
    stats = dict()
    if(signal['isDiscrete'] == True):

        stats['average'] = averageDiscrete(signal)
        stats['averageAbsolute'] = absoluteAverageDiscrete(signal)
        stats['averagePower'] = averagePowerDiscrete(signal)
        stats['standardDeviation'] = standardDeviationDiscrete(signal, stats['average'])
        stats['effectiveValue'] = effectiveValueDiscrete(stats['averagePower'])

    else:
        t1, t2, x = prepareSignalForIntegral(signal)
        y = computeSignal(signal, x)
        coeff = 1 / (t2 - t1)

        stats['average'] = averageContinuous(coeff, x, y)
        stats['averageAbsolute'] = absoluteAverageContinuous(coeff, x, y)
        stats['averagePower'] = averagePowerContinuous(coeff, x, y)
        stats['standardDeviation'] = standardDeviationContinuous(coeff, x, y, stats['average'])
        stats['effectiveValue'] = effectiveValueContinuous(stats['averagePower'])

    return stats

# Statistics of discrete signals

def averageDiscrete(signal):
    l = len(signal['y'])
    return sum(signal['y'])/l

def absoluteAverageDiscrete(signal):
    l = len(signal['y'])
    return sum([abs(y) for y in signal['y']])/l

def averagePowerDiscrete(signal):
    l = len(signal['y'])
    return sum([y**2 for y in signal['y']])/l

def standardDeviationDiscrete(signal, averageValue):
    l = len(signal['y'])
    return sum([(y - averageValue)**2 for y in signal['y']])/l
    
def effectiveValueDiscrete(averagePower):
    return math.sqrt(averagePower)

# Statistics of continuous signals

def averageContinuous(coeff, x, y):
    return computeIntegral(x, y)*coeff

def absoluteAverageContinuous(coeff, x, y):
    return computeIntegral(x, [abs(y) for y in y])*coeff  
    
def averagePowerContinuous(coeff, x, y):
    return computeIntegral(x, [y**2 for y in y])*coeff  

def standardDeviationContinuous(coeff, x, y, averageValue):
    return computeIntegral(x, [(abs(y-averageValue))**2 for y in y])*coeff  

def effectiveValueContinuous(averagePower):
    return math.sqrt(averagePower)

def computeIntegral(x, y):
    h = abs(x[1] - x[0])
    data = 0
    for i, v in enumerate(y):
        data += v if (i != 0 and i != len(y) - 1) else v*2
    return (h/2)*data

def prepareSignalForIntegral(signal):
    params = signal["params"]
    t1 = params["t1"]
    if signal["isPeriodic"]:
        T = params["T"]
        return (t1, t1+T, np.linspace(t1, t1+T, n + 1))
    else:
        d = params["d"]
        return (t1, t1+d , np.linspace(t1, t1+d, int(fp*d)))

