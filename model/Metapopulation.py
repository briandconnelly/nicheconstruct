# -*- coding: utf-8 -*-

"""Functions for working with Metapopulations"""

import numpy as np
from numpy import bitwise_xor, where
from numpy.random import binomial, multinomial, random_integers
import pandas as pd

from misc import stress_colnames
from Topology import random_neighbor


def create_metapopulation(config, topology, initial_state='populated'):
    """Create a metapopulation"""
    size = len(topology)
    assert size > 0

    capacity_min = config['Population']['capacity_min']
    capacity_max = config['Population']['capacity_max']
    assert capacity_min <= capacity_max

    initial_cooperator_proportion = config['Population']['initial_cooperator_proportion']

    genome_length_min = config['Population']['genome_length_min']
    genome_length_max = config['Population']['genome_length_max']
    assert genome_length_min <= genome_length_max

    stress_columns = stress_colnames(L=genome_length_max)

    stress_alleles = config['Population']['stress_alleles']

    if initial_state == 'populated':
        initial_popsize = capacity_min + \
                      (initial_cooperator_proportion * (capacity_max - capacity_min))

        data = {'Time': 0,
                'Population': np.repeat(np.arange(size), initial_popsize).tolist(),
                'Coop': (binomial(1, initial_cooperator_proportion, size * initial_popsize) == 1).tolist(),
                'Fitness': 0}
        data.update({sc: np.zeros(size * initial_popsize, dtype=np.int).tolist() for sc in stress_columns})

        M = pd.DataFrame(data,
                         columns=['Time', 'Population', 'Coop'] + ["S{0:02d}".format(i) for i in np.arange(1,genome_length_max+1)] + ['Fitness'])

    elif initial_state == 'cooperator_invade':
        coop_popid = int(size/2)

        defector_pops = np.repeat(np.delete(np.arange(size), coop_popid), capacity_min)
        cooperator_pop = np.repeat(coop_popid, capacity_max)

        # Make the metapopulation with all zeros at adaptive loci
        data = {'Time': 0,
                'Population': np.append(defector_pops, cooperator_pop).tolist(),
                'Coop': np.append(np.zeros(len(defector_pops))==1, np.ones(len(cooperator_pop))==1).tolist(),
                'Fitness': 0}
        data.update({sc: np.zeros(len(data['Population']), dtype=np.int).tolist() for sc in stress_columns})

        M = pd.DataFrame(data,
                         columns=['Time', 'Population', 'Coop'] + ["S{0:02d}".format(i) for i in np.arange(1,genome_length_max+1)] + ['Fitness'])

        # Set fully-adapted genotypes for both types
        cgenotype = np.tile(np.arange(stress_alleles)+1, np.ceil(genome_length_max/stress_alleles))[:genome_length_max]
        # But change the allelic state of defectors so that there is mismatch
        dgenotype = np.roll(cgenotype, 1)
        cgenotype = np.array([1,2,3,4,6])
        dgenotype = np.array([1,2,3,4,5])
        print('C: {c}, D: {d}'.format(c=cgenotype, d=dgenotype))
        #dgenotype = cgenotype
        defector_genotypes = np.repeat([dgenotype], len(defector_pops), axis=0)
        cooperator_genotypes = np.repeat([cgenotype], len(cooperator_pop), axis=0)
        M[stress_columns] = np.append(defector_genotypes, cooperator_genotypes, axis=0)

    elif initial_state == 'defector_invade':
        rare_popid = int(size/2)

        cooperator_pop = np.repeat(np.delete(np.arange(size), rare_popid), capacity_max)
        defector_pop = np.repeat(rare_popid, capacity_min)

        # Make the metapopulation with all zeros at adaptive loci
        data = {'Time': 0,
                'Population': np.append(defector_pop, cooperator_pop).tolist(),
                'Coop': np.append(np.zeros(len(defector_pop))==1, np.ones(len(cooperator_pop))==1).tolist(),
                'Fitness': 0}
        data.update({sc: np.zeros(len(data['Population']), dtype=np.int).tolist() for sc in stress_columns})

        M = pd.DataFrame(data,
                         columns=['Time', 'Population', 'Coop'] + ["S{0:02d}".format(i) for i in np.arange(1,genome_length_max+1)] + ['Fitness'])

        # Set fully-adapted genotypes for both types
        # Here, genotypes are matched
        cgenotype = np.tile(np.arange(stress_alleles)+1, np.ceil(genome_length_max/stress_alleles))[:genome_length_max]
        dgenotype = cgenotype
        defector_genotypes = np.repeat([dgenotype], len(defector_pop), axis=0)
        cooperator_genotypes = np.repeat([cgenotype], len(cooperator_pop), axis=0)

        # Randomize individual cooperator genotypes
        #cooperator_genotypes = np.array([cgenotype])
        #shifts = np.random.binomial(1, 0.1, len(cooperator_pop)-1)
        #for i in range(len(cooperator_pop)-1):
        #    print('looping',i/448000.0)
        #    cooperator_genotypes = np.vstack((cooperator_genotypes, np.roll(cgenotype, shifts[i])))

        M[stress_columns] = np.append(defector_genotypes, cooperator_genotypes, axis=0)

        # Randomize cooperator population genotypes
        #for p in M.loc[M.Coop==True].Population.unique():
        #    print('setting thing for pop', p)
        #    do_roll = np.random.binomial(1, 0.60)
        #    M.loc[M.Population==p, stress_columns] = np.roll(M.loc[M.Population==p, stress_columns], do_roll, axis=1)


    M = assign_fitness(M=M, Lmin=config['Population']['genome_length_min'],
                       Lmax=config['Population']['genome_length_max'],
                       num_stress_alleles=config['Population']['stress_alleles'],
                       base_fitness=config['Population']['base_fitness'],
                       cost_cooperation=config['Population']['cost_cooperation'],
                       benefit_nonzero=config['Population']['benefit_nonzero'],
                       benefit_ordered=config['Population']['benefit_ordered'])


    return M


def reset_stress_loci(M, Lmax):
    """Reset all stress loci in the population
    
    Resetting a stress locus sets its allelic state to 0.
    """

    M[stress_colnames(L=Lmax)] = 0
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


def mutate(M, mu_stress, mu_cooperation, Lmax, num_stress_alleles, config):
    """Mutate individuals in the metapopulation"""
    assert 0 <= mu_stress <= 1
    assert 0 <= mu_cooperation <= 1
    assert Lmax >= 0
    assert num_stress_alleles >= 0

    Mcopy = M.copy(deep=True)

    # Cooperation mutations - flip the cooperation bit 0->1 or 1->0
    Mcopy.Coop = bitwise_xor(Mcopy.Coop, binomial(n=1, p=mu_cooperation,
                                                  size=Mcopy.Coop.shape))==1

    # Mutations at stress loci
    # Alleles to mutate are chosen from a binomial distrubution, and these
    # alleles are modified by adding a random amount
    if Lmax > 0:
        s = stress_colnames(L=Lmax)
        if num_stress_alleles == 1:
            Mcopy[s] = bitwise_xor(Mcopy[s], binomial(n=1, p=mu_stress,
                                                      size=Mcopy[s].shape))
        else:
            # Technically, an allele could mutate to itself.
            astates = Mcopy[s].values
            mutants = binomial(n=1, p=mu_stress, size=Mcopy[s].shape)==1
            new_alleles = random_integers(low=0, high=num_stress_alleles,
                                          size=Mcopy[s].shape)
            astates[mutants] = new_alleles[mutants]
            Mcopy[s] = astates


    Mcopy = assign_fitness(M=Mcopy,
                           Lmin=config['Population']['genome_length_min'],
                           Lmax=config['Population']['genome_length_max'],
                           num_stress_alleles=config['Population']['stress_alleles'],
                           base_fitness=config['Population']['base_fitness'],
                           cost_cooperation=config['Population']['cost_cooperation'],
                           benefit_nonzero=config['Population']['benefit_nonzero'],
                           benefit_ordered=config['Population']['benefit_ordered'])

    return Mcopy


def grow(M, genome_lengths, config):
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
                          mu_stress=config['Population']['mutation_rate_stress'],
                          mu_cooperation=config['Population']['mutation_rate_cooperation'],
                          Lmax=config['Population']['genome_length_max'],
                          num_stress_alleles=config['Population']['stress_alleles'],
                          config=config)

    # Merge in the offspring
    M = M.append(mu_offspring)

    # Reindex the metapopulation
    M.index = np.arange(len(M))

    return M


def assign_fitness(M, Lmin, Lmax, num_stress_alleles, base_fitness,
                   cost_cooperation, benefit_nonzero, benefit_ordered):

    assert Lmin >= 0
    assert Lmax >= 0
    assert Lmin <= Lmax
    assert num_stress_alleles > 0

    stress_columns = stress_colnames(L=Lmax)

    for popid, P in M.groupby('Population'):
        Px = P.copy(deep=True)

        Px.Fitness = base_fitness - (Px.Coop * cost_cooperation)

        if Lmin > 0:
            stress_alleles = P.loc[:, stress_columns]

            Px.Fitness += np.sum(Px[stress_columns] > 0, axis=1) * benefit_nonzero

            if num_stress_alleles > 1 and benefit_ordered != 0:
                # Fitness is proportional to the number of individuals in the
                # population with the same allele at each locus. Get the
                # distribution of alleles in the population (per locus). Since
                # the 0 allele is the absence of adaptation, it does not
                # contribute to fitness.
                allele_dist = np.apply_along_axis(lambda x: np.bincount(x, minlength=num_stress_alleles+1),
                                                  axis=0, arr=stress_alleles)
                allele_dist[0] = np.zeros(allele_dist.shape[1])

                # Add gamma times the number of individuals with matching first allele
                # TODO: remove this. Benefit of first allelic state is number at last locus that is 1 less.
                #Px.Fitness += allele_dist[stress_alleles[stress_columns[0]], 0] * benefit_ordered

                # Add gamma times the number of individuals with increasing allele value
                #stress_alleles_next = (1 + (stress_alleles % num_stress_alleles)).values[:,:-1]
                #allele_dist_next = allele_dist[:,1:]
                #Px.Fitness += allele_dist_next[stress_alleles_next, range(Lmax-1)].sum(axis=1) * benefit_ordered

                stress_alleles_next = (1 + (stress_alleles % num_stress_alleles)).values
                allele_dist_next = np.roll(a=allele_dist, shift=-1, axis=1)

                Px.Fitness += allele_dist_next[stress_alleles_next, range(Lmax)].sum(axis=1) * benefit_ordered

        M.loc[M.Population==popid, 'Fitness'] = Px.Fitness

    return M

