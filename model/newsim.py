#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import SafeConfigParser

from Metapopulation import *

config = SafeConfigParser()
config.read('run.cfg')

metapop = create_metapopulation(config)
