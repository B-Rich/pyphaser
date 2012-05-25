PyPhaser -- A Lightweight Pipeline Framework for Phased Execution
=================================================================

Lightweight framework for **phased** execution of tasks. The term **phased**
means, that an application is split logically into distinct and possibly
dependent phases of execution. The key idea is that ``Phaser`` allows you to
execute **phases** from the command line and allows you to resume an
application from a given **phase**. This is particularly helpful in research
environments where the phases may be brittle such that sometimes manual
intervention and resuming a pipeline may be required. One key benefit of
``PyPhaser`` is the embedded and extensible command line parser that gives you
convenient access to your pipeline.

A **phase** is implemented as a subclass of either ``phaser.Phase`` or
``iter.Phase``, depending on your needs. The first is a simple execution phase
where you implement a single method, ``execute`` to perform your task::

    class Hello(Phase):
        """ Print 'Hello ' """

        def execute(self):
            print('Hello ', end='')

The second is a MapReduce style phase where you implement both an ``iter``
which returns the objects you would like to operate on and a single
``function`` method that takes a single object and does the actual operation::

    class World(IterPhase):
        """ Print 'World!' """

        def __init__(self):
            self.characters = 'World!'

        def function(self, character):
            print(character, end='')

        def iter(self):
            return iter(self.characters)

The rational for providing these two types of phases is that the first is for
simple, sequential tasks and the second is for tasks that might prospectively
be parallelized in the future.

In addition, the following methods can be implemented to provide for additional
robustness, which give you a poor-mans
`design by contract <http://en.wikipedia.org/wiki/Design_by_contract>`_:

:precondition:
    check preconditions
:preexec:
    things to execute before starting
:postexec:
    things to execute after finishing
:postcondition:
    check postconditions
:description:
    override the default description (first line of docstring)


Usage Example
-------------

See the ``phaser-hello-world`` which implements the famous ``Hello World!`` as
a phased application. It consists of the two phases: ``Hello`` and ``World``, which
both print a part of the desired string. The two classes are implemented using
the standard ``Phase`` and the ``IterPhase`` respectively.

The ``World`` phase contains a list of characters to print, where ``function``
will print a character and ``iter`` will return each charter in turn. Now,
PyPhaser provides you with the aforementioned command-line interface to this
pipeline::

    zsh» ./phaser-hello-world -h
    Usage: phaser-hello-world [options]

    Options:
    -h, --help            show this help message and exit
    -d, --display-all     display all available phases, in order
    -a, --all             execute all available phases in order
    -s phase, --single=phase
                            execute a single phase

    zsh» ./phaser-hello-world --display-all
    Available Phases
    ----------------
    0) Hello: Print 'Hello '
    1) World: Print 'World!

    zsh» ./phaser-hello-world -a
    Hello World!

    zsh» ./phaser-hello-world -s Hello
    Hello

    zsh» ./phaser-hello-world -s World
    World!

API for ``phaser.Phase`` and ``phaser.IterPhase``
-------------------------------------------------

Here is the basic API

Phase::

    class Phase(object)
    |  Abstract class for a phase
    |
    |  Methods defined here:
    |
    |  __call__(self, *args)
    |
    |  __str__(self)
    |
    |  description(self)
    |      Override or set as an attribute.
    |
    |  execute(self, *args)
    |      Implement this with the code that should be executed.
    |
    |  postcondition(self)
    |      Override this to implement checking postconditions.
    |
    |  postexec(self)
    |      Override this to execute things before phase execution
    |
    |  precondition(self)
    |      Override this to implement checking preconditions.
    |
    |  preexec(self)
    |      Override this to execute things before phase execution

IterPhase::

    class IterPhase(Phase)
    |  Abstract class for an iterating phase.
    |
    |  Methods defined here:
    |
    |  __iter__(self)
    |
    |  execute(self)
    |
    |  function(self, arg)
    |      Implement this to run on each argument
    |
    |  iter(self)
    |      Implement this to return an iterator for the items to execute.

TODO
----

* automatic logging/tracing
* caching via joblib
* example of how to inject options into the Phaser class parser

Author, Copyright and License
-----------------------------

(C) 2012 Valentin Haenel <valentin.haenel@gmx.de>

PyPhaser is licensed under the terms of the MIT License.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
