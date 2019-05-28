import math 

def hammingWindow(n, M):
    return 0.53836 - 0.46164 * math.cos( (2 * math.pi * n) / M)

def hanningWindow(n, M):
    return 0.5 - 0.5 * math.cos( (2 * math.pi * n) / M)

def blackmanWindow(n, M):
    return 0.42 - 0.5 * math.cos( (2 * math.pi * n) / M) + 0.08 * math.cos( (4 * math.pi * n) / M)