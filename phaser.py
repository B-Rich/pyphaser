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

    def description(self):
        """ Override or set as an attribute. """
        return self.__class__.__name__

    def __str__(self):
        if isinstance(self.description, str):
            return self.description
        else:
            return self.description()


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
                    (index, str(phase), phase.__doc__))

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

    def check_user_args(self):
        """ Check user supplied args exist before executing any phase. """
        pass

    def __call__(self):
        opts, args = self.parser.parse_args()
        self.phases_dict = dict((phase.__class__.__name__, phase) for phase in
            self.phases)
        self.check_user_args()
        if opts.display:
            self.print_available_phases()
        elif opts.single:
            self.execute_single(self.phases_dict[opts.single])
        elif opts.until:
            result = []
            for phase in self.phases:
                if str(phase) == opts.until:
                    break
                else:
                    result.append(phase)
            self.execute_sequence(result)
        elif opts.all:
            self.execute_all_phases()
        else:
            self.parser.print_help()

