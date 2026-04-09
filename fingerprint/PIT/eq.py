import numpy as np

def eq(set1: np.array, set2: np.array):
    p = 10**9 + 7
    k = 10
    n = len(set1)
    if n != len(set2):
        return False
    rx = np.random.randint(1, p, (k, 1), dtype=np.int64)

    def getfinger(s: np.array):
        res = np.mod(rx - s, p).astype(object)
        return np.prod(res, axis = 1) % p 
    
    return np.equal(getfinger(set1), getfinger(set2)) # bool矩阵