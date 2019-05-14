import convolution.windowFunctions as wf
import convolution.filterTypes as ft
import convolution.convolutionStrategies as cs
from convolution.filterCoefficient import transientResponse

import plotly.offline as py
import plotly.graph_objs as go
import numpy as np

WINDOW_FUNCTIONS = ['rectangular', 'hamming', 'hanning', 'blackman']
FILTER_TYPES = ['lowpass', 'bandpass', 'highpass']

def filterSignal(signal, filter, M, K, window):
    h = generateFilter(filter, M, K, window)
    return (h, cs.scipyConvolve(signal["y"], h))

def generateFilter(filter, M, K, window):
    h = transientResponse(M, K)

    if window != 'rectangular':
        w = getWindowFunction(window)
        h = [coeff * w(n, M) for n, coeff in enumerate(h)]
    
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