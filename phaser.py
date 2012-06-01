""" PyPhaser -- A lightweight Pipeline framework for phased execution """

from __future__ import print_function
import abc
from optparse import OptionParser


class Phase(object):
    """ Abstract class for a phase """

    __metaclass__ = abc.ABCMeta

    def precondition(self):
        """ Override this to implement checking preconditions. """
        pass

    def preexec(self):
        """ Override this to execute things before phase execution """
        pass

    def __call__(self, *args):
        return self.execute(*args)

    @abc.abstractmethod
    def execute(self, *args):
        """ Implement this with the code that should be executed. """
        pass

    def postexec(self):
        """ Override this to execute things before phase execution """
        pass

    def postcondition(self):
        """ Override this to implement checking postconditions. """
        pass

    def description(self):
        """ Override or set as an attribute. """
        return self.__class__.__name__

    def __str__(self):
        if isinstance(self.description, str):
            return self.description
        else:
            return self.description()

class IterPhase(Phase):
    """ Abstract class for an iterating phase. """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def iter(self):
        """ Implement this to return an iterator for the items to execute. """
        pass

    def execute(self):
        """ Override this with alternative execution mechanisms. """
        for args in self:
            self.function(args)

    @abc.abstractmethod
    def function(self, arg):
        """ Implement this to run on each argument """
        pass

    def __iter__(self):
        return self.iter()

class Phaser(object):
    """ Class for phase execution.

    Parameters
    ----------
    phases : list
        list of instances of objects which inherit from Phase
    """

    def __init__(self, phases=None):
        self.phases = [] if not phases else phases
        self.phases_dict = None
        self.parser = Phaser.create_parser()

    def execute_all_phases(self):
        """ Execute all phases. """
        self.execute_sequence(self.phases)

    def execute_sequence(self, sequence):
        """ Execute a sequence of phases """
        for phase in sequence:
            self.execute_single(phase)

    @staticmethod
    def execute_single(phase):
        """ Execute a single phases.

        Parameters
        ----------
        phase : phase instance
            the phase to execute
        """
        phase.precondition()
        phase.preexec()
        phase.execute()
        phase.postexec()
        phase.postcondition()

    def print_available_phases(self):
        """ Print all available phases. """
        print("Available Phases")
        print("----------------")
        indices = []
        phases = []
        descriptions = []
        for index, phase in enumerate(self.phases):
            indices.append(str(index).strip())
            phases.append(str(phase).strip())
            descriptions.append(str(phase.__doc__).strip())
        def align(seq):
            max_ = max(map(len, seq))
            return [i.ljust(max_) for i in seq]
        indices = align(indices)
        phases = align(phases)
        descriptions = align(descriptions)
        for i in range(len(indices)):
            print ("%s) %s: %s" %
                (indices[i], phases[i], descriptions[i]))

    @staticmethod
    def create_parser():
        parser = OptionParser()
        parser.add_option('-d', '--display-all',
                action='store_true',
                dest='display',
                help='display all available phases, in order')
        parser.add_option('-a', '--all',
                action='store_true',
                dest='all',
                help='execute all available phases in order')
        parser.add_option('-s', '--single',
                action='store',
                type='string',
                dest='single',
                metavar='phase',
                help='execute a single phase')
        parser.add_option('-u', '--until',
                action='store',
                type='string',
                dest='until',
                metavar='phase',
                help='execute until phase')
        return parser

    def check_user_opts(self):
        """ Check user supplied args exist before executing any phase. """
        pass

    def __call__(self):
        self.opts, self.args = self.parser.parse_args()
        self.phases_dict = dict((phase.__class__.__name__, phase) for phase in
            self.phases)
        self.check_user_opts()
        if self.opts.display:
            self.print_available_phases()
        elif self.opts.single:
            self.execute_single(self.phases_dict[self.opts.single])
        elif self.opts.until:
            result = []
            for phase in self.phases:
                if str(phase) == self.opts.until:
                    break
                else:
                    result.append(phase)
            self.execute_sequence(result)
        elif self.opts.all:
            self.execute_all_phases()
        else:
            self.parser.print_help()

