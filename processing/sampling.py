import numpy as np
from signals.constants import signals
from signals.signalGenerator import computeSignal

def sample(signal, fp):
    maxX = max(signal['x'])
    minX = min(signal['x'])
    signalLength = signal['x'][-1] - signal['x'][0]
    samplesCount = (signalLength) * fp
    print(f"samplesCount: {samplesCount}")

    newX = np.linspace(signal['x'][0],  signal['x'][-1], samplesCount + 1) 
    newY = computeSignal(signal, newX)

    return { 
        'name': signal['name'],
        'displayName': f"sampled: fp={fp}({signal['displayName']})", 
        'isDiscrete': True,
        'isPeriodic': False,
        'isComplex': False,
        'x': newX,
        'y': newY,
        'params': signal['params'] 
    }
