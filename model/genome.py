import numpy as np

def bitstring_as_base10(a):
    return np.sum(a * 2**np.arange(len(a))[::-1])

def base10_as_bitarray(a):
    return np.array(map(int, bin(a)[2:]))

def hamming_distance(a, b):
    return bin(a ^ b)[2:].count('1')

def is_producer(g, bits):
    return g & 2**bits == 2**bits

