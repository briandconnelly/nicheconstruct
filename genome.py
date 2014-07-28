import numpy as np

def bitstring_as_base10(a):
    return np.sum(a * 2**np.arange(len(a))[::-1])

def hamming_distance(a, b):
    """Compute the Hamming distance (number of bits that differ in the binary
    representation) between two integers"""

    return bin(a ^ b)[2:].count('1')

