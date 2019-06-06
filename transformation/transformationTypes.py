from transformation.utility import iexp
from commons.utility import try_get
import convolution.convolutionStrategies as cs
import math
import time
import pywt
import numpy as np

def perform_transformation(transformation_type, signal):

    transformation_function = TRANSFORMATIONS[transformation_type]
    y = signal["y"] if not try_get(signal, "isIrrational") else [complex(signal["y"][i], signal["iy"][i]) for i in range(len(signal["x"]))]

    t_start = time.perf_counter()
    transformation_result = transformation_function(y)
    t_end = time.perf_counter()

    elapsed = t_end - t_start
    
    returned_signals = []

    if transformation_type == 'DB4':
        x1, x2 = transformation_result
        returned_signals.append({
            'name': 'transformated(DB4) x1 ' + signal["name"],
            'displayName': 'transformated(DB4) x1 ' + signal["displayName"],
            'isDiscrete': True,
            'isPeriodic': False,
            'isComplex': False,
            'displayContinuous': True,
            'x': [n for n in range(len(x1))],
            'y': x1,
            'params': signal["params"],
        })

        returned_signals.append({
            'name': 'transformated(DB4) x2 ' + signal["name"],
            'displayName': 'transformated(DB4) x2 ' + signal["displayName"],
            'isDiscrete': True,
            'isPeriodic': False,
            'isComplex': False,
            'displayContinuous': True,
            'x': [n for n in range(len(x2))],
            'y': x2,
            'params': signal["params"],
        })
    elif transformation_type == 'INV_DFT':
        returned_signals.append({
            'name': f"inv transformated {transformation_type} " + signal["name"],
            'displayName': f"inv transformated {transformation_type} " + signal["displayName"],
            'isDiscrete': False,
            'isPeriodic': False,
            'isComplex': False,
            'x': signal["time_domain"],
            'y': [c.real for c in transformation_result],
            'params': signal["params"],
            'isIrrational': False
        })
    else:
        f0 = signal["params"]["fp"] / signal["params"]["n"]
        x = [m * f0 for m in range(len(transformation_result))]
        returned_signals.append({
            'name': f"transformated {transformation_type} " + signal["name"],
            'displayName': f"transformated {transformation_type} " + signal["displayName"],
            'isDiscrete': True,
            'isPeriodic': False,
            'isComplex': False,
            'x': x,
            'y': [c.real for c in transformation_result],
            'params': signal["params"],
            'isIrrational': True,
            'ix': x,
            'iy': [c.imag for c in transformation_result],
            'time_domain': signal["x"]
        })

    return (returned_signals, elapsed)


def dft(xs):
    N = np.size(xs)
    X = np.zeros((N,), dtype=np.complex128)
    for m in range(0, N):
        for n in range(0, N):
            X[m] += xs[n]*np.exp(-np.pi*2j*m*n/N)
    return X

def dft_inv(xs):
    N = np.size(xs)
    X = np.zeros((N,), dtype=np.complex128)
    for m in range(0, N):
        for n in range(0, N):
            X[m] += xs[n]*np.exp(np.pi*2j*m*n/N)
    return X/N

# recursive version of fast fourier transform
def fft(X):
    N = len(X)
    half = N // 2
    if N > 1:
        X = fft(X[::2]) + fft(X[1::2])
        for k in range(N//2):
            xk = X[k]
            kernel = iexp(-2*math.pi*k/N)
            c = kernel * X[k+half]
            X[k] = xk + c
            X[k+half] = xk - c
    return X

# vectorized version of fast fourier transform
def fft_vectorized(x):
    x = np.asarray(x, dtype=float)
    N = x.shape[0]

    if np.log2(N) % 1 > 0:
        raise ValueError("size of x must be a power of 2")

    N_min = min(N, 32)

    n = np.arange(N_min)
    k = n[:, None]
    M = np.exp(-2j * np.pi * n * k / N_min)
    X = np.dot(M, x.reshape((N_min, -1)))

    while X.shape[0] < N:
        X_even = X[:, :X.shape[1] // 2]
        X_odd = X[:, X.shape[1] // 2:]
        factor = np.exp(-1j * np.pi * np.arange(X.shape[0])/ X.shape[0])[:, None]
        X = np.vstack([X_even + factor * X_odd,
                       X_even - factor * X_odd])

    return X.ravel()

denom = 4 * math.sqrt(2)
sqrt3 = math.sqrt(3)
h = [(1 + sqrt3) / denom, (3 + sqrt3) / denom,(3 - sqrt3) / denom, (1 - sqrt3) / denom]
g = [h[3], -h[2], h[1], -h[0]]
# ih = [h[2], g[2], h[0], g[0]]
# ig = [h[3], g[3], h[1], g[1]]

def db4(xs):
	H = cs.scipyConvolve(xs, h)
	G = cs.scipyConvolve(xs, g)
	x1 = [x for i, x in enumerate(H) if i % 2 == 0]
	x2 = [x for i, x in enumerate(G) if i % 2 == 1]
	return (x1, x2)

TRANSFORMATIONS = {
    'DFT': dft,
    'INV_DFT': dft_inv,
    'FFT': fft,
    'FFT_VECT': fft_vectorized,
    'DB4': db4
}
