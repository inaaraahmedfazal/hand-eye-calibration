import numpy as np
    
def MAD(rmag: np.ndarray) -> float:
    """Calculates median absolute deviation of 1D data"""
    n = len(rmag)
    med = np.median(rmag)
    data_med_diff = np.empty((n,))
    for i in range(n):
        data_med_diff[i] = abs(rmag[i] - med)
    return np.median(data_med_diff)

def TukeyWeights(rmag: np.ndarray, rmagMedian: float, MAD: float) -> np.ndarray:
    n = len(rmag)
    weights = np.empty((n,))
    sigma = 1.4826 * MAD
    s = sigma * sigma
    for i in range(n):
        rMedDiff = rmag[i] - rmagMedian
        if abs(rMedDiff) <= sigma:
            t = rMedDiff * rMedDiff / s
            weights[i] = (1.0 - t) * (1.0 - t)
        else:
            weights[i] = 0.0

    return weights

def residualMag3D(data: np.ndarray, dataMean: np.ndarray) -> np.ndarray:
    """Calculates residual magnitude of 3D data"""
    n = len(data)
    rmag = np.empty((n,))
    for i in range(n):
        rmag[i] = np.linalg.norm(data[i]-dataMean)
    return rmag

def residualMag1D(data: np.ndarray, dataMean: float) -> np.ndarray:
    """Calculates residual magnitude of 1D data"""
    n = len(data)
    rmag = np.empty((n,))
    for i in range(n):
        rmag[i] = abs(data[i] - dataMean)
    return rmag

def weightedAvg3D(data: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Calculates weighted average from 3D data and a 1D set of corresponding weights"""
    n = len(data)
    weightedSum = np.zeros((3,))
    for i in range(n):
        weightedSum[0] += data[i, 0] * weights[i]
        weightedSum[1] += data[i, 1] * weights[i]
        weightedSum[2] += data[i, 2] * weights[i]
    div = np.sum(weights)
    ret = weightedSum/div
    return ret

def weightedAvg1D(data: np.ndarray, weights: np.array) -> np.ndarray:
    """Calculates weighted average from 1D data and a 1D set of corresponding weights"""
    n = len(data)
    weightedSum = 0
    for i in range(n):
        weightedSum += data[i] * weights[i]
    ret = weightedSum / np.sum(weights)
    return ret

def robustAverage3D(data: np.ndarray) -> np.ndarray:
    """Calculates robust average of 3D data based on Tukey bi-weight function:
    https://ieeexplore.ieee.org/document/661192
    """

    threshold = 1e-6

    # initial dataMean and dataMeanNew calculation:
    dataMean = np.mean(data, 0)
    rmag = residualMag3D(data, dataMean)
    rmagMedian = np.median(rmag)
    mad = MAD(rmag)
    weights = TukeyWeights(rmag, rmagMedian, mad)
    dataMeanNew = weightedAvg3D(data, weights)

    # iterations
    iterCount = 0
    while np.linalg.norm(dataMean-dataMeanNew) > threshold and iterCount < 1000:
        dataMean = dataMeanNew
        rmag = residualMag3D(data, dataMean)
        rmagMedian = np.median(rmag)
        mad = MAD(rmag)
        weights = TukeyWeights(rmag, rmagMedian, mad)
        dataMeanNew = weightedAvg3D(data, weights)
        iterCount += 1
    if iterCount >= 1000:
        print("Robust average did not converge to a threshold of 1e-6 after 1000 iterations")
    return dataMeanNew

def robustAverage1D(data: np.ndarray) -> float:
    """Calculates robust average of 3D data based on Tukey bi-weight function:
    https://ieeexplore.ieee.org/document/661192
    """
    threshold = 1e-6

    # initial dataMean and dataMeanNew calculation
    dataMean = np.mean(data)
    rmag = residualMag1D(data, dataMean)
    rmagMedian = np.median(rmag)
    mad = MAD(rmag)
    weights = TukeyWeights(rmag, rmagMedian, mad)
    dataMeanNew = weightedAvg1D(data, weights)

    # iterations
    iterCount = 0
    while abs(dataMean - dataMeanNew) > threshold and iterCount < 1000:
        dataMean = dataMeanNew
        rmag = residualMag1D(data, dataMean)
        rmagMedian = np.median(rmag)
        mad = MAD(rmag)
        weights = TukeyWeights(rmag, rmagMedian, mad)
        dataMeanNew = weightedAvg1D(data, weights)
        iterCount += 1

    if iterCount >= 1000:
        print("Robust average did not converge to a threshold of 1e-6 after 1000 iterations")
    return dataMeanNew