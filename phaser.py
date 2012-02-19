""" PyPhaser -- A lightweight Pipeline framework for phased execution """

from __future__ import print_function
from optparse import OptionParser


class Phase(object):
    """ Abstract class for a phase """

    def precondition(self):
        """ Override this to implement checking preconditions. """
        pass

    def preexec(self):
        """ Override this to execute things before phase execution """
        pass

    def __call__(self, *args):
        return self.execute(*args)

    def execute(self, *args):
        """ Implement this with the code that should be executed. """
        pass

    def postexec(self):
        """ Override this to execute things before phase execution """
        pass

    def postcondition(self):
        """ Override this to implement checking postconditions. """
        pass

    def iter(self):
        """ Implement this to return an iterator for the items to execute. """
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

    def execute_all_phases(self):
        """ Execute all phases. """
        for phase in self.phases:
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
        for args in phase:
            phase.execute(args)
        phase.postexec()
        phase.postcondition()

    def print_available_phases(self):
        """ Print all available phases. """
        print("Available Phases")
        print("----------------")
        for index, phase in enumerate(self.phases):
            print ("%i) %s:    %s" %
                    (index, phase.__class__.__name__, phase.__doc__))

    def __call__(self):
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
        opts, args = parser.parse_args()
        self.phases_dict = dict((phase.__class__.__name__, phase) for phase in
            self.phases)
        if opts.display:
            self.print_available_phases()
        elif opts.single:
            self.execute_single(self.phases_dict[opts.single])
        elif opts.all:
            self.execute_all_phases()
        else:
            parser.print_help()

