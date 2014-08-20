# -*- coding: utf-8 -*-

from Action import Action

class ChangeEnvironment(Action):

    def __init__(self, metapopulation): 
        super(ChangeEnvironment, self).__init__(metapopulation=metapopulation)
        self.frequency = self.config.getint(section='ChangeEnvironment',
                                            option='frequency')

        assert self.frequency >= 0

    def update(self, time):
        if self.frequency > 0 and time % self.frequency == 0:
            self.metapopulation.change_environment()

