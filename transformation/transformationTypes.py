from utility import iexp
import math 

def dft(xs):
    N = len(xs)
    return [sum((xs[n] * iexp(-2 * math.pi * m * n / N) for n in range(N)))
        for m in range(N)]

def dft_inv(xs):
    N = len(xs)
    return [sum((xs[k] * iexp(2 * math.pi * m * n / N) for n in range(N))) / N
            for m in range(N)]


