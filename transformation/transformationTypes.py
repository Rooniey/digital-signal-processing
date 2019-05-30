from transformation.utility import iexp
import convolution.convolutionStrategies as cs
import math
import time
import pywt

def perform_transformation(transformation_type, signal):

    transformation_function = TRANSFORMATIONS[transformation_type]
    y = signal["y"]

    t_start = time.perf_counter()
    result = transformation_function(y)
    t_end = time.perf_counter()

    elapsed = t_end - t_start

    f0 = signal["params"]["fp"] / len(result)
    x = [m * f0 for m in range(len(result))]

    return ({
        'name': 'transformated ' + signal["name"],
        'displayName': 'transformated ' + signal["displayName"],
        'isDiscrete': True,
            'isPeriodic': False,
            'isComplex': False,
            'x': x,
            'y': [c.real for c in result],
            'params': signal["params"],
            'isIrrational': True,
            'ix': x,
            'iy': [c.imag for c in result]
            }, elapsed)


def dft(xs):
    N = len(xs)
    return [sum((xs[n] * iexp(-2 * math.pi * m * n / N) for n in range(N)))
            for m in range(N)]


def dft_inv(xs):
    N = len(xs)
    return [sum((xs[k] * iexp(2 * math.pi * m * n / N) for n in range(N))) / N
            for m in range(N)]


def fft(X):
    n = len(X)
    if n > 1:
        X = fft(X[::2]) + fft(X[1::2])
        for k in range(n//2):
            xk = X[k]
            kernel = iexp(-2*math.pi*k/n)
            X[k] = xk + kernel*X[k+n//2]
            X[k+n//2] = xk - kernel*X[k+n//2]
    return X

TRANSFORMATIONS = {
    'DFT': dft,
    'FFT': fft
}

# denom = 4 * math.sqrt(2)
# sqrt3 = math.sqrt(3)

# h = [(1 + sqrt3) / denom, (3 + sqrt3) / denom, (3 - sqrt3) / denom, (1 - sqrt3) / denom]
# # h = [0.48, 0.84, 0.22, -0.13]
# g = [h[3], -h[2], h[1], -h[0]]

# ih = [h[2], g[2], h[0], g[0]]
# ig = [h[3], g[3], h[1], g[1]]


# def db4_kupa(xs):
# 	H = cs.scipyConvolve(xs, h)
# 	G = cs.scipyConvolve(xs, g)
# 	H2 = [x for i, x in enumerate(H) if i%2 == 0]
# 	G2 = [x for i, x in enumerate(G) if i % 2 == 1]
# 	return H2 + G2


# def db4(xs):
# 	N = len(xs)
# 	copy = xs[:]
# 	n = N
# 	while(n >= 4):
# 		db4_(copy, n)
# 		n = n // 2
# 	return copy


# def db4_(a, n):
# 	if n >= 4:
# 		half = n // 2
# 		tmp = n * [0]

# 		i = 0
# 		for  j in range(0, n - 3, 2):
# 			tmp[i]      = a[j]*h[0] + a[j+1]*h[1] + a[j+2]*h[2] + a[j+3]*h[3]
# 			tmp[i+half] = a[j]*g[0] + a[j+1]*g[1] + a[j+2]*g[2] + a[j+3]*g[3]
# 			i+=1

# 		tmp[i]      = a[n-2]*h[0] + a[n-1]*h[1] + a[0]*h[2] + a[1]*h[3]
# 		tmp[i+half] = a[n-2]*g[0] + a[n-1]*g[1] + a[0]*g[2] + a[1]*g[3]

# 		for k in range(0, n):
# 			a[k] = tmp[k]

# print(db4_kupa([1, 1, 4, 4, 0, 0, 1, 1]))
# print(pywt.dwt([1, 1, 4, 4, 0, 0, 1, 1], 'db4', mode='periodization'))
# print(db4([1, 1, 4, 4, 0, 0, 1, 1]))
