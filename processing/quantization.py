from numpy import round

def quantize(signal, steps):
    maxY = max(signal['y'])
    minY = min(signal['y'])
    step = (maxY - minY) / (steps - 1)
    print(f"max: {maxY} min: {minY} step: {step}")

    quantizedSignalY = [minY + (round( (value - minY) / step) * step) for value in signal['y']]

    return { 
        'name': signal['name'],
        'displayName': f"quantized: s#={steps} - {signal['name']}", 
        'isDiscrete': True,
        'isPeriodic': False,
        'isComplex': False,
        'x': signal['x'], 
        'y': quantizedSignalY, 
        'params': signal['params'] 
    }
