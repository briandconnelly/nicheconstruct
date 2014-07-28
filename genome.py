import numpy as np

def bitstring_as_base10(a):
    return np.sum(a * 2**np.arange(len(a))[::-1])

