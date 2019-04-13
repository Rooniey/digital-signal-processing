from numpy import linespace, sinc
from math import floor

# LEGEND
# xValues, yValues- set of oredred quantized values
# fe - extrapolation frequency
def extrapolationZOH(xValues, yValues, fe):
    T = xValues[1] - xValues[0]
    t0 = xValues[0]
    tk = xValues[-1]
    tnmax = len(xValues) - 1

    duration = tk - t0 
    N = fe * duration

    tValues = linspace(t0, tk, N + 1)
    newYValues = []
    n = 0
    for t in tValues:
        while n != tnmax and t > xValues[n+1]:
            n += 1
        newYValues.append(yValues[n])
        
    return {
        "x": tValues,
        "y": newYValues
    }

# LEGEND
# xValues, yValues- set of oredred quantized values
# fe - extrapolation frequency
# n - side neighbourhood count
def extrapolationSinc(xValues, yValues, fe, n):
    T = xValues[1] - xValues[0]
    t0 = xValues[0]
    tk = xValues[-1]
    tnmax = len(xValues) - 1

    duration = tk - t0 
    N = fe * duration

    tValues = linspace(t0, tk, N + 1)
    newYValues = []

    for t in tValues:
        oneStepBack = floor(t / T)
        potentialLeftmost = oneStepBack - (n - 1)
        potentialRightmost = oneStepBack + (n + 1)

        leftmostPoint = potentialLeftmost if potentialLeftmost > - 1 else 0
        rightmostPoint = potentialRightmost if potentialRightmost > tnmax else tnmax

        tmp = yValues[leftmostPoint:rightmostPoint]
        aggragate = 0

        for index, value in enumerate(tmp):
            aggragate += value * sinc( (t / T) - leftmostPoint + index)

        newYValues.append(aggregate)

    return {
        "x": tValues,
        "y": newYValues
    }
