"""Functions for working with bitstring genomes"""

import numpy as np

def bitstring_as_base10(bitstring):
    """Convert a bitstring to a base 10 number"""
    return np.sum(bitstring * 2**np.arange(len(bitstring))[::-1])

def base10_as_bitarray(num):
    """Convert a base 10 number to a bit (NumPy) array"""
    return np.array([int(b) for b in bin(num)[2:]])

def hamming_distance(genome1, genome2):
    """Calculate the Hamming distance between two genotypes"""
    return bin(genome1 ^ genome2)[2:].count('1')

hamming_distance_v = np.vectorize(hamming_distance)

def is_producer(genotype, bits):
    """Determine whether or not the given genotype is a producer"""
    return genotype & 2**bits == 2**bits

