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
    y_values = list(map(lambda t: A*math.sin((2*math.pi/T)*(t - t1)), x_values))
    return [x_values, y_values]
