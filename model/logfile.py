# -*- coding: utf-8 -*-

"""Functions for writing data files"""

import numpy as np

from misc import stress_colnames

def write_metapop_data(writer, metapop, topology, cycle, config):
    """Write information about the metapopulation to a CSV writer"""

    # Here, diversity is only calculated based on stress loci. To add cooperation locus, use ['Coop'] + stress_columns
    if config['Population']['genome_length_max'] > 0:
        stress_columns = stress_colnames(L=config['Population']['genome_length_max'])
        genotype_props = np.array([group.shape[0]/metapop.shape[0] for genotype, group in metapop.groupby(stress_columns)])
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

    Lmax = config['Population']['genome_length_max']
    stress_columns = stress_colnames(L=config['Population']['genome_length_max'])

    for popid, subpop in metapop.groupby('Population'):
        try:
            coords = topology.node[popid]['coords']
            pos_x = coords[0]
            pos_y = coords[1]
        except KeyError:
            pos_x = pos_y = np.nan

        if Lmax > 0:
            genotype_props = np.array([group.shape[0]/subpop.shape[0] for genotype, group in subpop.groupby(stress_columns)])
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

