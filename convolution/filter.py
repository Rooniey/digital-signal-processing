import windowFunctions as wf
import filterTypes as ft
import convolutionStrategies as cs
from filterCoefficient import transientResponse

WINDOW_FUNCTIONS = ['rectangular', 'hamming', 'hanning', 'blackman']
FILTER_TYPES = ['lowpass', 'bandpass', 'lowpass']

def filterSignal(signal, filter, M, K, window):
    h = generateFilter(filter, M, K, window)
    return cs.scipyConvolve(signal.y, h)

def generateFilter(filter, M, K, window):
    h = transientResponse(M, K)
    
    if window != 'rectangular':
        w = getWindowFunction(window)
        h = [coeff * w(n) for n, coeff in enumerate(h)]
    
    if(filter != 'lowpass'):
        s = getFilterTypeMultiplierFunction(filter)
        h = [coeff * s(n) for n, coeff in enumerate(h)]

    return h 

def getWindowFunction(window):
    if window == 'hamming':
        return wf.hammingWindow
    if window == 'hanning':
        return wf.hanningWindow
    if window == 'blackman':
        return wf.blackmanWindow

    raise Exception(f"Unknown type ({window}) of window function")

def getFilterTypeMultiplierFunction(filter):
    if filter == 'bandpass':
        return ft.bandpassMultiplier
    if filter == 'highpass':
        return ft.highpassMultiplier