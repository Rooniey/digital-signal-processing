import numpy as np
import math



def uniform_noise(n, A, t1, d):
    y_values = list(map(lambda v: 2*A*v - A, np.random.rand(n)))
    x_values = np.linspace(t1, t1+d, n)
    return [x_values, y_values]
    
def gaussian_noise(n, A, t1, d):
    y_values = list(map(lambda v: 2*A*v - A, np.random.randn(n)))
    x_values = np.linspace(t1, t1+d, n)
    return [x_values, y_values]
    
def sin(n, A, t1, T, d):
    x_values = np.linspace(t1, t1+d, n)
    y_values = list(map(lambda t: A*sin_helper(t, t1, T), x_values))
    return [x_values, y_values]

def sin_half_rectified(n, A, t1, T, d):
    x_values = np.linspace(t1, t1+d, n)
    y_values = list(map(lambda t: 0.5*A*(sin_helper(t, t1, T) + abs(sin_helper(t, t1, T))), x_values))
    return [x_values, y_values]

def sin_full_rectified(n, A, t1, T, d):
    x_values = np.linspace(t1, t1+d, n)
    y_values = list(map(lambda t: A*abs(sin_helper(t, t1, T)), x_values))
    return [x_values, y_values]

def rectangular(n, A, t1, T, d, kw):
    x_values = np.linspace(t1, t1+d, n)
    y_values = list(map(lambda t: 0 if rect_helper(t, t1, T, kw, A) == -1 else A, x_values))
    return [x_values, y_values]

def rectangular_symmetrical(n, A, t1, T, d, kw):
    x_values = np.linspace(t1, t1+d, n)
    y_values = list(map(lambda t: -A if rect_helper(t, t1, T, kw, A) == -1 else A, x_values))
    return [x_values, y_values]

def sawtooth(n, A, t1, T, d, kw):
    x_values = np.linspace(t1, t1+d, n)
    y_values = list(map(lambda t: sawtooth_helper(t, t1, T, kw, A), x_values))
    return [x_values, y_values]

def unit_step(n, A, t1, d, ts):
    x_values = np.linspace(t1, t1+d, n)
    y_values = list(map(lambda t: unit_step_helper(t, A, ts), x_values))
    return [x_values, y_values]
  
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
