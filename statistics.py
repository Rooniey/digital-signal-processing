from operations import computeSignal
from utility import pluck
import numpy as np
import math

n = 1000
fp = 1000

def calculateStatistics(signal):
    average = None 
    averageAbsolute = None
    averagePower = None 
    valueVariance = None 
    effectiveValue = None
    if(signal['isDiscrete'] == True):
        average = calculateAverageDiscrete(signal)
        averageAbsolute = calculateAverageAbsoluteDiscrete(signal)
        averagePower = calculateAveragePowerDiscrete(signal)
        valueVariance = calculateValueVarianceDiscrete(signal, average)
        effectiveValue = calculateEffectiveValueDiscrete(signal)
    else:
        t1, t2, x = prepareSignalForIntegral(signal)
        y = computeSignal(signal, x)
        coeff = 1 / (t2 - t1)

        average = calculateAverageContinuous(coeff, x, y)
        averageAbsolute = calculateAverageAbsoluteContinuous(coeff, x, y)
        averagePower = calculateAveragePowerContinuous(coeff, x, y)
        valueVariance = calculateValueVarianceContinuous(coeff, x, y, average)
        effectiveValue = calculateEffectiveValueContinuous(averagePower)

    return {
        'average': average,
        'averageAbsolute': averageAbsolute,
        'averagePower': averagePower,
        'valueVariance': valueVariance,
        'effectiveValue': effectiveValue
    }

def calculateAverageDiscrete(signal):
    l = len(signal['y'])
    return sum(signal['y'])/l

def calculateAverageAbsoluteDiscrete(signal):
    l = len(signal['y'])
    return sum([abs(y) for y in signal['y']])/l

def calculateAveragePowerDiscrete(signal):
    l = len(signal['y'])
    return sum([y**2 for y in signal['y']])/l

def calculateValueVarianceDiscrete(signal, averageValue):
    l = len(signal['y'])
    return sum([abs(y - averageValue)**2 for y in signal['y']])/l
    
def calculateEffectiveValueDiscrete(averagePower):
    return math.sqrt(averagePower)

def calculateAverageContinuous(coeff, x, y):
    return computeIntegral(x, y)*coeff

def calculateAverageAbsoluteContinuous(coeff, x, y):
    return computeIntegral(x, [abs(y) for y in y])*coeff  
    
def calculateAveragePowerContinuous(coeff, x, y):
    return computeIntegral(x, [y**2 for y in y])*coeff  

def calculateValueVarianceContinuous(coeff, x, y, averageValue):
    return computeIntegral(x, [(abs(y-averageValue))**2 for y in y])*coeff  

def calculateEffectiveValueContinuous(averagePower):
    return math.sqrt(averagePower)

def computeIntegral(x, y):
    h = x[1] - x[0]
    # print('xxxx')
    # print(h)
    h = abs(h)
    # print(h)
    data = 0
    # print('xxxx')
    for i, v in enumerate(y):
        print(f"{i} - {v}")
        # data += v if (i != 0 and i != len(y) - 1) else v*2
        if (i == 0 or i == len(y) - 1):
            data += v
        else:
            data += v*2
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

