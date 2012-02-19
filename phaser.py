from __future__ import print_function
from optparse import OptionParser

class Phase(object):
    """ Abstract class for a phase """

    def __init__(self):
        pass

    def precondition(self):
        pass

    def preexec(self):
        pass

    def __call__(self, *args):
        return self.execute(*args)

    def postexec(sefl):
        pass

    def postcondition(self):
        pass

    def __iter__(self):
        return self.iter()

class Phaser(object):
    """ Class for phase execution. """

    def __init__(self, phases=None):
        self.phases = [] if not phases else phases

    def add_phase(self, phase):
        self.phases.append(phase)

    def execute_all_phases(self):
        for phase in self.phases:
            self.execute_single(phase)

    def execute_single(self, phase):
        phase.precondition()
        phase.preexec()
        for args in phase:
            phase.execute(args)
        phase.postexec()
        phase.postcondition()

    def print_available_phases(self):
        print("Available Phases")
        print("----------------")
        for index,phase in enumerate(self.phases):
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

