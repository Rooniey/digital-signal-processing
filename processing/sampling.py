import numpy as np
from constants import signals

def sample(signal, fp):
    maxX = max(signal['x'])
    minX = min(signal['x'])
    signalLength = maxX - minX
    samplesCount = (signalLength) * fp

    newX = np.linspace(minX, maxX, samplesCount + 1) 
    newY = signals[signal['name']]['fn'](newX, signal['params'])

    return { 
        'name': signal['name'],
        'displayName': f"sampled: fp={fp} - {signal['name']}", 
        'isDiscrete': True,
        'isPeriodic': False,
        'isComplex': False,
        'x': newX,
        'y': newY,
        'params': signal['params'] 
    }
