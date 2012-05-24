PyPhaser -- A Lightweight Pipeline Framework for Phased Execution
=================================================================

Lightweight framework for **phased** execution of tasks. The term **phased**
means, that an application is split logically into distinct and possibly
dependent phases of execution. The key idea is that ``Phaser`` allows you to
execute **phases** from the command line and allows you to resume an
application from a given **phase**. This is particularly helpful in research
environments where the phases may be brittle such that sometimes manual
intervention and resuming a pipeline may be required.

A **phase** is implemented as a subclass of ``phaser.Phase``, where the
following methods two methods must be implemented::

    execute              <---- execute phase for a single item
    iter                 <---- returns a list of items for execute

The following methods can be implemented to provide for additional robustness::

    precondition         <---- check preconditions
    preexec              <---- things to execute before starting
    postexec             <---- things to execute after finishing
    postcondition        <---- check postconditions

Usage Example
-------------

See the ``phaser-hello-world`` which implements the famous ``Hello World!`` as
a phased application. It consists of two phases: ``Hello`` and ``World``, which
both print a part of the desired string. The two classes are implemented such
that they contain a list of characters to print, where ``execute`` will print a
character and ``iter`` will return each charter in turn.::

    zsh» ./phaser-hello-world -h
    Usage: phaser-hello-world [options]

    Options:
    -h, --help            show this help message and exit
    -d, --display-all     display all available phases, in order
    -a, --all             execute all available phases in order
    -s phase, --single=phase
                            execute a single phase

    zsh» ./phaser-hello-world -d
    Available Phases
    ----------------
    0) Hello:     Print 'Hello '
    1) World:     Print 'World!'
    2) File3:    Write 'Hello World!' to a file 3 times

    zsh» ./phaser-hello-world -a
    Hello World!
    zsh» cat hello.txt
    Hello World!
    Hello World!
    Hello World!

    zsh» ./phaser-hello-world -s Hello
    Hello

    zsh» ./phaser-hello-world -s World
    World!

API for ``phaser.Phase``
------------------------

Here is the basic API::

    phaser.Phase = class Phase(__builtin__.object)
    |  Abstract class for a phase
    |
    |  Methods defined here:
    |
    |  __call__(self, *args)
    |
    |  __iter__(self)
    |
    |  execute(self, *args)
    |      Implement this with the code that should be executed.
    |
    |  iter(self)
    |      Implement this to return an iterator for the items to execute.
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