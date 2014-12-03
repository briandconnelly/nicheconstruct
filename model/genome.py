"""Functions for working with bitstring genomes"""

from numpy import sum as nsum
from numpy import arange, array, vectorize

def bitstring_as_base10(bitstring):
    """Convert a bitstring to a base 10 number"""
    return nsum(bitstring * 2**arange(len(bitstring))[::-1])

def base10_as_bitarray(num):
    """Convert a base 10 number to a bit (NumPy) array"""
    # np.binary_repr has a width option, but it's slower.
    return array([int(b) for b in bin(num)[2:]])

def hamming_distance(genome1, genome2):
    """Calculate the Hamming distance between two genotypes"""
    return bin(genome1 ^ genome2).count('1')

hamming_distance_v = vectorize(hamming_distance)

def is_producer(genotype, bits):
    """Determine whether or not the given genotype is a producer"""
    return genotype & 2**bits == 2**bits

def num_ones(bitstring):
    """Return the number of 1s in the bitstring"""
    return bin(bitstring).count('1')

num_ones_v = vectorize(num_ones)

