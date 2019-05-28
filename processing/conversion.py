from numpy import linspace, sinc, tile, dot, newaxis
from math import floor
from commons.validators import try_float, try_int
import PySimpleGUI as sg

def reconstruct(signal, params):
    fe = try_float(params['fe'])
    if fe == None:
        sg.Popup('Error!', 'Specify reconstruct frequency!')
        return None

    x_values, y_values = None, None
    methodName = None
    if not params['Sinc?']:
        x_values, y_values = extrapolationZOH(signal['x'], signal['y'], fe)
        methodName = 'ZOH'
    if params['Sinc?']:
        n = try_int(params['sincNeighbors'])
        if n == None:
            sg.Popup('Error!', 'Specify reconstruct frequency!')
            return None
        x_values, y_values = extrapolationSinc(signal['x'], signal['y'], fe, n)
        methodName = 'sinc'

    return { 
        **signal,
        'name': signal['name'],
        'displayName': f"reconstructed w/ {methodName} fe={params['fe']} ({signal['displayName']})", 
        'isDiscrete': True,
        'displayContinuous': True,
        'isPeriodic': False,
        'x': x_values,
        'y': y_values
    }



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
        
    return (tValues, newYValues)

def sinc_interp(x, s, u):
    """
    Interpolates x, sampled at "s" instants
    Output y is sampled at "u" instants ("u" for "upsampled")
    
    from Matlab:
    http://phaseportrait.blogspot.com/2008/06/sinc-interpolation-in-matlab.html        
    """
    
    if len(x) != len(s):
        raise Exception('x and s must be the same length')
    
    # Find the period    
    T = s[1] - s[0]
    print(s[:, newaxis])
    print("/n")
    sincM = tile(u, (len(s), 1)) - tile(s[:, newaxis], (1, len(u)))
    print(f"sincM: {sincM}")
    y = dot(x, sinc(sincM/T))
    return y

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
        if t % T == 0:
            newYValues.append(yValues[int(t/T)])
            continue

        oneStepBack = floor( abs(t - t0) / T)
        
        potentialLeftmost = oneStepBack - (n - 1)
        potentialRightmost = oneStepBack + n

        leftmostPoint = potentialLeftmost if potentialLeftmost > - 1 else 0
        rightmostPoint = potentialRightmost if potentialRightmost < tnmax else tnmax
        tmp = yValues[leftmostPoint:rightmostPoint + 1]
        aggragate = 0

        for index, value in enumerate(tmp):
            aggragate += value * sinc( (t / T) - (leftmostPoint + index))

        newYValues.append(aggragate)
    # newYValues = sinc_interp(yValues, xValues, tValues)

    return (tValues, newYValues)
