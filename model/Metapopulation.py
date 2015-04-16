# -*- coding: utf-8 -*-

"""Functions for working with Metapopulations"""

import numpy as np
from numpy import bitwise_xor, where
from numpy.random import binomial, multinomial, random_integers
import pandas as pd

from misc import adaptive_colnames
from Topology import random_neighbor


def create_metapopulation(config, topology, initial_state='populated'):
    """Create a metapopulation"""
    size = len(topology)
    assert size > 0

    capacity_min = config['Population']['capacity_min']
    capacity_max = config['Population']['capacity_max']
    assert capacity_min <= capacity_max

    initial_cooperator_proportion = config['Population']['initial_cooperator_proportion']
    genome_length = config['Population']['genome_length']
    adaptive_columns = adaptive_colnames(L=genome_length)
    num_adaptive_alleles = config['Population']['adaptive_alleles']

    # Start with a fully populated metapopulation, where each population is
    # filled with the configured initial_cooperator_proportion
    if initial_state == 'populated':
        initial_popsize = capacity_min + \
                      (initial_cooperator_proportion * (capacity_max - capacity_min))

        data = {'Time': 0,
                'Population': np.repeat(np.arange(size), initial_popsize).tolist(),
                'Coop': (binomial(1, initial_cooperator_proportion, size * initial_popsize) == 1).tolist(),
                'Fitness': 0}
        data.update({sc: np.zeros(size * initial_popsize, dtype=np.int).tolist() for sc in adaptive_columns})

        M = pd.DataFrame(data,
                         columns=['Time', 'Population', 'Coop'] + ["A{0:02d}".format(i) for i in np.arange(1,genome_length+1)] + ['Fitness'])

    # Start with a population of isogenic defector populations, where a single
    # patch contains an adapted cooperator population
    elif initial_state == 'cooperator_invade':
        coop_popid = int(size/2)

        defector_pops = np.repeat(np.delete(np.arange(size), coop_popid), capacity_min)
        cooperator_pop = np.repeat(coop_popid, capacity_max)

        # Make the metapopulation with all zeros at adaptive loci
        data = {'Time': 0,
                'Population': np.append(defector_pops, cooperator_pop).tolist(),
                'Coop': np.append(np.zeros(len(defector_pops))==1, np.ones(len(cooperator_pop))==1).tolist(),
                'Fitness': 0}
        data.update({sc: np.zeros(len(data['Population']), dtype=np.int).tolist() for sc in adaptive_columns})

        M = pd.DataFrame(data,
                         columns=['Time', 'Population', 'Coop'] + ["A{0:02d}".format(i) for i in np.arange(1,genome_length+1)] + ['Fitness'])

        # Set fully-adapted genotypes for both types
        dgenotype = np.tile(np.arange(num_adaptive_alleles)+1, np.ceil(genome_length/num_adaptive_alleles))[:genome_length]
        cgenotype = np.copy(dgenotype)
        cgenotype[-1] += 1

        defector_genotypes = np.repeat([dgenotype], len(defector_pops), axis=0)
        cooperator_genotypes = np.repeat([cgenotype], len(cooperator_pop), axis=0)
        M[adaptive_columns] = np.append(defector_genotypes, cooperator_genotypes, axis=0)

    # Start with a population of isogenic cooperator populations, where a single
    # patch contains defectors
    elif initial_state == 'defector_invade':
        rare_popid = int(size/2)

        cooperator_pop = np.repeat(np.delete(np.arange(size), rare_popid), capacity_max)
        defector_pop = np.repeat(rare_popid, capacity_min)

        # Make the metapopulation with all zeros at adaptive loci
        data = {'Time': 0,
                'Population': np.append(defector_pop, cooperator_pop).tolist(),
                'Coop': np.append(np.zeros(len(defector_pop))==1, np.ones(len(cooperator_pop))==1).tolist(),
                'Fitness': 0}
        data.update({sc: np.zeros(len(data['Population']), dtype=np.int).tolist() for sc in adaptive_columns})

        M = pd.DataFrame(data,
                         columns=['Time', 'Population', 'Coop'] + ["A{0:02d}".format(i) for i in np.arange(1,genome_length+1)] + ['Fitness'])

        # Set fully-adapted genotypes for both types
        # Here, genotypes are matched
        cgenotype = np.tile(np.arange(num_adaptive_alleles)+1, np.ceil(genome_length/num_adaptive_alleles))[:genome_length]
        dgenotype = np.copy(cgenotype)

        defector_genotypes = np.repeat([dgenotype], len(defector_pop), axis=0)
        cooperator_genotypes = np.repeat([cgenotype], len(cooperator_pop), axis=0)
        M[adaptive_columns] = np.append(defector_genotypes, cooperator_genotypes, axis=0)


    M = assign_fitness(M=M, genome_length=config['Population']['genome_length'],
                       num_adaptive_alleles=config['Population']['adaptive_alleles'],
                       base_fitness=config['Population']['base_fitness'],
                       cost_cooperation=config['Population']['cost_cooperation'],
                       benefit_nonzero=config['Population']['benefit_nonzero'],
                       benefit_ordered=config['Population']['benefit_ordered'])


    return M


def reset_adaptive_loci(M, genome_length):
    """Reset all adaptive loci in the population
    
    Resetting a adaptive locus sets its allelic state to 0.
    """

    M[adaptive_colnames(L=genome_length)] = 0
    return M


def mix(M, topology):
    """Mix the metapopulation

    Mixing creates the individuals in a metapopulation to be re-distributed
    evenly among the populations
    """

    M.Population = random_integers(low=0, high=len(topology)-1,
                                   size=M.shape[0])
    return M


def migrate(M, topology, rate):
    """Migrate individuals among subpopulations"""
    assert 0 <= rate <= 1

    # Don't do migration when there's only one population
    if len(topology) == 1:
        return

    emigrants_ix = M.index[where(binomial(n=1, p=rate,
                                          size=M.index.shape[0]) == 1)]

    if emigrants_ix.shape[0] > 0:
        targets = {p: random_neighbor(p, topology) for p in M.Population.unique()}
        get_target = np.vectorize(lambda t: targets[t])
        M.loc[emigrants_ix, 'Population'] = get_target(M.loc[emigrants_ix, 'Population'].values)

    return M


def mutate(M, mu_adaptation, mu_cooperation, genome_length, num_adaptive_alleles, config):
    """Mutate individuals in the metapopulation"""
    assert 0 <= mu_adaptation <= 1
    assert 0 <= mu_cooperation <= 1
    assert genome_length >= 0
    assert num_adaptive_alleles >= 0

    Mcopy = M.copy(deep=True)

    # Cooperation mutations - flip the cooperation bit 0->1 or 1->0
    Mcopy.Coop = bitwise_xor(Mcopy.Coop, binomial(n=1, p=mu_cooperation,
                                                  size=Mcopy.Coop.shape))==1

    # Mutations at adaptive loci
    # Alleles to mutate are chosen from a binomial distrubution, and these
    # alleles are modified by adding a random amount
    if genome_length > 0:
        s = adaptive_colnames(L=genome_length)
        if num_adaptive_alleles == 1:
            Mcopy[s] = bitwise_xor(Mcopy[s], binomial(n=1, p=mu_adaptation,
                                                      size=Mcopy[s].shape))
        else:
            # Technically, an allele could mutate to itself.
            astates = Mcopy[s].values
            mutants = binomial(n=1, p=mu_adaptation, size=Mcopy[s].shape)==1
            new_alleles = random_integers(low=0, high=num_adaptive_alleles,
                                          size=Mcopy[s].shape)
            astates[mutants] = new_alleles[mutants]
            Mcopy[s] = astates


    Mcopy = assign_fitness(M=Mcopy,
                           genome_length=config['Population']['genome_length'],
                           num_adaptive_alleles=config['Population']['adaptive_alleles'],
                           base_fitness=config['Population']['base_fitness'],
                           cost_cooperation=config['Population']['cost_cooperation'],
                           benefit_nonzero=config['Population']['benefit_nonzero'],
                           benefit_ordered=config['Population']['benefit_ordered'])

    return Mcopy


def grow(M, config):
    """Grow the population"""

    smin = config['Population']['capacity_min']
    smax = config['Population']['capacity_max']
    assert smin <= smax

    # Keep track of the indices of offspring
    offspring_ix = np.array([], dtype=np.int)

    # Get a list of parent individual indices
    for popid, subpop in M.groupby('Population'):
        # Get the number of offspring to produce (carrying capacity - current)
        num_offspring = smin + round(subpop.Coop.mean() * (smax - smin)) - len(subpop)

        # Select the number of offspring to produce for each parent
        parent_num_offspring = multinomial(n=num_offspring,
                                           pvals=subpop.Fitness/subpop.Fitness.sum())

        # Get a list of the global index values for each parent
        parent_ix = subpop.iloc[np.repeat(np.arange(len(parent_num_offspring)),
                                          parent_num_offspring)].index.values

        offspring_ix = np.append(offspring_ix, parent_ix)

    # Mutate the offspring
    mu_offspring = mutate(M=M.loc[offspring_ix],
                          mu_adaptation=config['Population']['mutation_rate_adaptation'],
                          mu_cooperation=config['Population']['mutation_rate_cooperation'],
                          genome_length=config['Population']['genome_length'],
                          num_adaptive_alleles=config['Population']['adaptive_alleles'],
                          config=config)

    # Merge in the offspring
    M = M.append(mu_offspring)

    # Reindex the metapopulation
    M.index = np.arange(len(M))

    return M


def assign_fitness(M, genome_length, num_adaptive_alleles, base_fitness,
                   cost_cooperation, benefit_nonzero, benefit_ordered):

    assert num_adaptive_alleles > 0

    adaptive_columns = adaptive_colnames(L=genome_length)

    for popid, P in M.groupby('Population'):
        Px = P.copy(deep=True)

        Px.Fitness = base_fitness - (Px.Coop * cost_cooperation)

        if genome_length > 0:
            adaptive_alleles = P.loc[:, adaptive_columns]

            Px.Fitness += np.sum(Px[adaptive_columns] > 0, axis=1) * benefit_nonzero

            if num_adaptive_alleles > 1 and benefit_ordered != 0:
                # Fitness is proportional to the number of individuals in the
                # population with the same allele at each locus. Get the
                # distribution of alleles in the population (per locus). Since
                # the 0 allele is the absence of adaptation, it does not
                # contribute to fitness.
                allele_dist = np.apply_along_axis(lambda x: np.bincount(x, minlength=num_adaptive_alleles+1),
                                                  axis=0, arr=adaptive_alleles)
                allele_dist[0] = np.zeros(allele_dist.shape[1])

                # Get the next allelic state for everything and the distribution of alleles at the next locus (here we "roll" the matrix representing the allelic states in the population)
                adaptive_alleles_next = (1 + (adaptive_alleles  % num_adaptive_alleles)).values
                allele_dist_next = np.roll(a=allele_dist, shift=-1, axis=1)

                # Here, the fitness at each allele is proportional to the number of individuals with allele a+1 at the next locus.
                # NOTE: this is slightly different than described in the text, where this relationship is described as the fitness of an allele increases with the number of individuals with allele a-1 at the previous locus
                Px.Fitness += allele_dist_next[adaptive_alleles_next, range(genome_length)].sum(axis=1) * benefit_ordered

        M.loc[M.Population==popid, 'Fitness'] = Px.Fitness

    return M

