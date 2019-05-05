import math
import numpy as np

def transientResponse(M, K):
    if M % 2 == 0:
        raise Exception("M must be odd")

    nArray = np.linspace(0, M - 1, M)
    return list(map(lambda n: filterCoefficient(n, M, K) , nArray))

def filterCoefficient(n, M, K):
    mid = (M - 1.0) / 2
    if n == mid:
        return 2.0 / K
    else:
        n = n - mid
        numerator = math.sin( (2 * math.pi * n) / K)
        denominator = math.pi * n
        return numerator / denominator