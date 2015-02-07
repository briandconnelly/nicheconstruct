# -*- coding: utf-8 -*-

"""Functions for working with configuration files"""


def write_configfile(config, filename='configuration.cfg'):
    """Write the configuration to a file"""

    with open(filename, 'w') as configfile:
        config.write(configfile)


def is_integer(x):
    try:
        fv = float(x)
        iv = int(x)
        return fv == iv
    except ValueError:
        return False

def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def is_in_range(x, low, high):
    assert low <= high
    return low <= float(x) <= high

def is_gt(x, val):
    return float(x) > val

def is_ge(x, val):
    return float(x) >= val

def validate_configfile(config):
    """Validate a configuration file"""

    # Functions for checking the given configuration
    has_section = lambda s: config.has_section(s)
    has_parameter = lambda s, p: config.has_option(s, p)
    has_int_value = lambda s, p: is_integer(config[s][p])
    has_float_value = lambda s, p: is_float(config[s][p])
    value_gt0 = lambda s, p: is_gt(config[s][p], 0)
    value_ge0 = lambda s, p: is_ge(config[s][p], 0)
    value_01 = lambda s, p: is_in_range(config[s][p], 0, 1)

    def require_section(s):
        if not has_section(s):
            raise Exception("Missing section '{s}'".format(s=s))
    def require_param(s, p):
        if not has_parameter(s, p):
            raise Exception("Section '{s}' missing value for parameter '{p}'".format(s=s, p=p))
    def require_float(s, p):
        if not has_float_value(s, p):
            raise ValueError("Value for '{p}' in section '{s}' must be numeric".format(s=s, p=p))
    def require_int(s, p):
        if not has_int_value(s, p):
            raise ValueError("Value for '{p}' in section '{s}' must be an integer".format(s=s, p=p))
    def require_gt0(s, p):
        if not value_gt0(s, p):
            raise ValueError("Value for '{p}' in section '{s}' must be greater than 0".format(s=s, p=p))
    def require_ge0(s, p):
        if not value_ge0(s, p):
            raise ValueError("Value for '{p}' in section '{s}' must be greater than or equal to 0".format(s=s, p=p))
    def require_01(s, p):
        if not value_01(s, p):
            raise ValueError("Value for '{p}' in section '{s}' must be between 0 and 1, inclusive".format(s=s, p=p))
    def require_oneof(s, p, vals):
        if not config[s][p] in vals:
            raise ValueError("Value for '{p}' in section '{s}' must be one of {v}".format(s=s, p=p, v=', '.join(vals)))
    def require_oneof_str(s, p, vals):
        if not config[s][p] in vals:
            raise ValueError("Value for '{p}' in section '{s}' must be one of {v}".format(s=s, p=p, v=', '.join(["'{}'".format(v) for v in vals])))

    required_sections = ['Simulation', 'Metapopulation', 'Population']
    for sec in required_sections:
        require_section(sec)

    require_param('Simulation', 'num_cycles')
    require_int('Simulation', 'num_cycles')
    require_gt0('Simulation', 'num_cycles')

    require_param('Simulation', 'environment_change')
    require_oneof_str('Simulation', 'environment_change', ['none', 'metapopulation', 'population'])

    # TODO: rest of simulation

    require_oneof_str('Metapopulation', 'topology', ['moore', 'vonneumann', 'smallworld', 'complete', 'regular'])

    if config['Metapopulation']['topology'].lower() == 'moore':
        # TODO - check section
        # TODO - check params
        pass

    elif config['Metapopulation']['topology'].lower() == 'vonneumann':
        # TODO - check section
        # TODO - check params
        pass

    elif config['Metapopulation']['topology'].lower() == 'smallworld':
        # TODO - check section
        # TODO - check params
        pass

    elif config['Metapopulation']['topology'].lower() == 'complete':
        # TODO - check section
        # TODO - check params
        pass

    elif config['Metapopulation']['topology'].lower() == 'regular':
        # TODO - check section
        # TODO - check params
        pass

    require_param('Metapopulation', 'migration_rate')
    require_float('Metapopulation', 'migration_rate')
    require_01('Metapopulation', 'migration_rate')

    require_param('Metapopulation', 'mix_frequency')
    require_int('Metapopulation', 'mix_frequency')
    require_ge0('Metapopulation', 'mix_frequency')

    # TODO Density threshold stuff (int, ge0), or do that in simulation??
    #assert int(config['Metapopulation']['density_threshold']) >= 0, 'Metapopulation density_threshold must be >= 0'

    require_param('Population', 'genome_length_min')
    require_int('Population', 'genome_length_min')
    require_ge0('Population', 'genome_length_min')
    #require(sec, param, props=['param', 'int', 'ge0'])

    require_param('Population', 'genome_length_max')
    require_int('Population', 'genome_length_max')
    require_ge0('Population', 'genome_length_max')

    if int(config['Population']['genome_length_max']) < int(config['Population']['genome_length_min']):
        raise ValueError("Value for 'genome_length_max' in section '{s}' must greater than or equal to value of 'genome_length_min'".format(s='Population'))

    require_param('Population', 'stress_alleles')
    require_int('Population', 'stress_alleles')
    require_gt0('Population', 'stress_alleles')

    require_param('Population', 'capacity_min')
    require_int('Population', 'capacity_min')
    require_ge0('Population', 'capacity_min')

    require_param('Population', 'capacity_max')
    require_int('Population', 'capacity_max')
    require_ge0('Population', 'capacity_max')

    if int(config['Population']['capacity_max']) < int(config['Population']['capacity_min']):
        raise ValueError("Value for 'capacity_max' in section '{s}' must greater than or equal to value of 'capacity_min'".format(s='Population'))


    # Move this to the density detection stuff
    assert int(config['Population']['density_threshold']) >= 0, 'Population density_threshold must be >= 0'

    require_param('Population', 'initial_cooperator_proportion')
    require_float('Population', 'initial_cooperator_proportion')
    require_01('Population', 'initial_cooperator_proportion')

    require_param('Population', 'mutation_rate_stress')
    require_float('Population', 'mutation_rate_stress')
    require_01('Population', 'mutation_rate_stress')

    require_param('Population', 'mutation_rate_cooperation')
    require_float('Population', 'mutation_rate_cooperation')
    require_01('Population', 'mutation_rate_cooperation')

    require_param('Population', 'mutation_rate_tolerance')
    require_float('Population', 'mutation_rate_tolerance')
    require_01('Population', 'mutation_rate_tolerance')

    require_param('Population', 'dilution_factor')
    require_float('Population', 'dilution_factor')
    require_01('Population', 'dilution_factor')

    require_param('Population', 'base_fitness')
    require_param('Population', 'cost_cooperation')
    require_param('Population', 'benefit_nonzero')
    require_param('Population', 'benefit_ordered')

