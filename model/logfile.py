# -*- coding: utf-8 -*-

"""Functions for writing data files"""

import numpy as np
import pandas as pd

from misc import adaptive_colnames

def write_metapop_data(writer, metapop, topology, cycle, config):
    """Write information about the metapopulation to a CSV writer"""

    # Here, diversity is only calculated based on adaptive loci. To add cooperation locus, use ['Coop'] + adaptive_columns
    if config['Population']['genome_length'] > 0:
        adaptive_columns = adaptive_colnames(L=config['Population']['genome_length'])
        genotype_props = np.array([group.shape[0]/metapop.shape[0] for genotype, group in metapop.groupby(adaptive_columns)])
        shannon = (genotype_props * np.log(genotype_props)).sum() * -1
        simpson = np.power(genotype_props, 2).sum()
    else:
        shannon = 0
        simpson = 0

    metapop_data = {'Time': cycle,
                    'PopulationSize': metapop.shape[0],
                    'CooperatorProportion': metapop.Coop.mean(),
                    'MinCooperatorFitness': metapop[metapop.Coop==1].Fitness.min(),
                    'MaxCooperatorFitness': metapop[metapop.Coop==1].Fitness.max(),
                    'MeanCooperatorFitness': metapop[metapop.Coop==1].Fitness.mean(),
                    'MinDefectorFitness': metapop[metapop.Coop==0].Fitness.min(),
                    'MaxDefectorFitness': metapop[metapop.Coop==0].Fitness.max(),
                    'MeanDefectorFitness': metapop[metapop.Coop==0].Fitness.mean(),
                    'ShannonIndex': shannon,
                    'SimpsonIndex': simpson}
    writer.writerow(metapop_data)


def write_population_data(writer, metapop, topology, cycle, config):
    """Write information about each population in the metapopulation to a CSV writer"""

    genome_length = config['Population']['genome_length']
    adaptive_columns = adaptive_colnames(L=genome_length)

    for popid, subpop in metapop.groupby('Population'):
        try:
            coords = topology.node[popid]['coords']
            pos_x = coords[0]
            pos_y = coords[1]
        except KeyError:
            pos_x = pos_y = np.nan

        if genome_length > 0:
            genotype_props = np.array([group.shape[0]/subpop.shape[0] for genotype, group in subpop.groupby(adaptive_columns)])
            shannon = (genotype_props * np.log(genotype_props)).sum() * -1
            simpson = np.power(genotype_props, 2).sum()
        else:
            shannon = 0
            simpson = 0

        pop_data = {'Time': cycle,
                    'Population': popid,
                    'X': pos_x,
                    'Y': pos_y,
                    'PopulationSize': subpop.shape[0],
                    'CooperatorProportion': subpop.Coop.mean(),
                    'MinCooperatorFitness': subpop[subpop.Coop==1].Fitness.min(),
                    'MaxCooperatorFitness': subpop[subpop.Coop==1].Fitness.max(),
                    'MeanCooperatorFitness': subpop[subpop.Coop==1].Fitness.mean(),
                    'MinDefectorFitness': subpop[subpop.Coop==0].Fitness.min(),
                    'MaxDefectorFitness': subpop[subpop.Coop==0].Fitness.max(),
                    'MeanDefectorFitness': subpop[subpop.Coop==0].Fitness.mean(),
                    'ShannonIndex': shannon,
                    'SimpsonIndex': simpson}

        writer.writerow(pop_data)

def write_population_genotypes(writer, metapop, topology, cycle, config):
    """Write information about each population in the metapopulation to a CSV writer"""

    genome_length = config['Population']['genome_length']
    adaptive_columns = adaptive_colnames(L=genome_length)

    for popid, subpop in metapop.groupby('Population'):
        try:
            coords = topology.node[popid]['coords']
            pos_x = coords[0]
            pos_y = coords[1]
        except KeyError:
            pos_x = pos_y = np.nan

        if genome_length > 0:
            genotype_props = np.array([group.shape[0]/subpop.shape[0] for genotype, group in subpop.groupby(adaptive_columns)])
            x = pd.DataFrame(subpop.groupby(adaptive_columns, sort=False).size(), columns=['abundance'])
            genotype_str = str(x[x.abundance==max(x.abundance)][0:1].reset_index().as_matrix()[0,0:-1])
            
            pop_data = {'Time': cycle,
                        'Population': popid,
                        'X': pos_x,
                        'Y': pos_y,
                        'Genotype': genotype_str}

            writer.writerow(pop_data)

