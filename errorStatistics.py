from math import log10

def calculateErrorStatistics(xPredicted, xActual):
    lenP = len(xPredicted)
    lenA = len(xActual)
    if(lenP != lenA): 
        raise Exception(f"To calculate mean squared error the same dimensions are needed {lenP} != {lenA}")
    return {
        "meanSquaredError": meanSquaredError(xPredicted, xActual),
        "maxDifferent": maxDifferenceError(xPredicted, xActual),
        "psnr": psnr(xPredicted, xActual),
        "snr": snr(xPredicted, xActual)
    }

def meanSquaredError(xPredicted, xActual):
    squareDiffs = list(map(lambda pair: (pair[1] - pair[0])**2, zip(xPredicted, xActual)))
    return sum(squareDiffs) / len(xPredicted)

def maxDifferenceError(xPredicted, xActual):
    diffs = list(map(lambda pair: abs(pair[1] - pair[0]), zip(xPredicted, xActual)))
    return max(diffs)

def psnr(xPredicted, xActual, precomputedMSE = None):
    maxActual = max(xActual)
    mse = precomputedMSE if precomputedMSE != None else meanSquaredError(xPredicted, xActual)
    return 10 * log10(maxActual/mse)

def snr(xPredicted, xActual):
    actualSquareSum = sum(list(map(lambda x: x**2, xActual)))
    squareDiffsSum = sum(list(map(lambda pair: (pair[1] - pair[0])**2, zip(xPredicted, xActual))))
    return 10 * log10(actualSquareSum/squareDiffsSum)
