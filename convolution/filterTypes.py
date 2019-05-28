import math

def bandpassMultiplier(n):
    return 2 * math.sin(math.pi * (n / 2.0))

def highpassMultiplier(n):
    return 1 if n % 2 == 0 else -1