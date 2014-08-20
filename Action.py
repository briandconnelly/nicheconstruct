# -*- coding: utf-8 -*-

class Action(object):

    def __init__(self, metapopulation): 
        self.metapopulation = metapopulation
        self.config = metapopulation.config

    def update(self, time):
        pass

