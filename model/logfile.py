# -*- coding: utf-8 -*-

"""Functions for writing data files"""

import numpy as np

def write_metapop_data(writer, metapop, topology, cycle):
    """Write information about the metapopulation to a CSV writer"""
    metapop_data = {'Time': cycle,
                    'PopulationSize': metapop.shape[0],
                    'CooperatorProportion': metapop.Coop.mean(),
                    'MinCooperatorFitness': metapop[metapop.Coop==1].Fitness.min(),
                    'MaxCooperatorFitness': metapop[metapop.Coop==1].Fitness.max(),
                    'MeanCooperatorFitness': metapop[metapop.Coop==1].Fitness.mean(),
                    'MinDefectorFitness': metapop[metapop.Coop==0].Fitness.min(),
                    'MaxDefectorFitness': metapop[metapop.Coop==0].Fitness.max(),
                    'MeanDefectorFitness': metapop[metapop.Coop==0].Fitness.mean()}
    writer.writerow(metapop_data)


def write_population_data(writer, metapop, topology, cycle):
    """Write information about each population in the metapopulation to a CSV writer"""

    for popid, subpop in metapop.groupby('Population'):
        try:
            coords = topology.node[popid]['coords']
            pos_x = coords[0]
            pos_y = coords[1]
        except KeyError:
            pos_x = pos_y = np.nan

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
                    'MeanDefectorFitness': subpop[subpop.Coop==0].Fitness.mean()}

        writer.writerow(pop_data)

