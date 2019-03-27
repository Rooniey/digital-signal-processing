import numpy as np
from constants import signals
from utility import pluck

def generate_signal(signalType, param_values):
    d, fp, t1 = pluck(param_values, 'd', 'fp', 't1')
    n = int(d * fp)
    param_values['n'] = n
    x_values = np.linspace(t1, t1+d, n + 1)
    return signals[signalType]['fn'](x_values, param_values)