import numpy as np
import math
from commons.utility import pluck

# Continuous Signals

def uniform_noise(x_values, params):
    A, n = pluck(params, 'A', 'n')
    return list(map(lambda v: 2*A*v - A, np.random.rand(n)))

def gaussian_noise(x_values, params):
    A, n = pluck(params, 'A', 'n')
    return np.random.normal(0, 2*A, n)

def sin(x_values, params):
    A, t1, T = pluck(params,'A', 't1', 'T')
    return list(map(lambda t: A*sin_helper(t, t1, T), x_values))

def sin_half_rectified(x_values, params):
    A, t1, T = pluck(params,'A', 't1', 'T')
    return list(map(lambda t: 0.5*A*(sin_helper(t, t1, T) + abs(sin_helper(t, t1, T))), x_values))

def sin_full_rectified(x_values, params):
    A, t1, T = pluck(params,'A', 't1', 'T')
    return list(map(lambda t: A*abs(sin_helper(t, t1, T)), x_values))

def rectangular(x_values, params):
    A, t1, T, kw = pluck(params,'A', 't1', 'T', 'kw')
    return list(map(lambda t: 0 if rect_helper(t, t1, T, kw, A) == -1 else A, x_values))
    
def rectangular_symmetrical(x_values, params):
    A, t1, T, kw = pluck(params,'A', 't1', 'T', 'kw')
    return list(map(lambda t: -A if rect_helper(t, t1, T, kw, A) == -1 else A, x_values))

def sawtooth(x_values, params):
    A, t1, T, kw = pluck(params,'A', 't1', 'T', 'kw')
    return list(map(lambda t: sawtooth_helper(t, t1, T, kw, A), x_values))

def unit_step(x_values, params):
    A, ts = pluck(params,'A', 'ts')
    return list(map(lambda t: unit_step_helper(t, A, ts), x_values))

# Discrete Signals

def unit_impulse(x_values, params):
    A, ts = pluck(params, 'A', 'ts')
    return list(map(lambda v: A if v == ts else 0, x_values))

def impulse_noise(x_values, params):
    A, p = pluck(params, 'A', 'p')
    return [A if np.random.rand() < p else 0 for x in range(len(x_values))]

# Helper Functions

def sin_helper(t, t1, T):
    return math.sin((2*math.pi/T)*(t - t1))

def rect_helper(t, t1, T, kw, A):
    k = math.floor((t - t1)/T)
    return -1 if t - t1 - k*T >= kw*T else 1

def sawtooth_helper(t, t1, T, kw, A):
    k = math.floor((t - t1)/T)
    if t - t1 - k*T >= kw*T:
        return (-A/(T*(1-kw)))*(t-k*T-t1) + (A/(1-kw))
    else:
        return (A/(kw*T))*(t-k*T-t1)

def unit_step_helper(t, A, ts):
    if t < ts:
        return 0
    elif t > ts:
        return A
    else:
        return 0.5*A 
