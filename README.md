# Georgios
My explorations in computer design. Currently simulated with
[Icarus Verilog](http://iverilog.icarus.com/) with schematics
in [gschem](http://wiki.geda-project.org/geda:gaf).
Georgios 1 and the initial work on 2 were done in
[Logicism](http://www.cburch.com/logisim/download.html)
but a bug in how registers update forced me to other means of design and
simulation.

The current iteration is Georgios 2 which consists of 8 bit data size, 8
instructions, and by default 16 registers. It only has instructions for
changing register values, adding and subtracting, each by a value or a
register, along with nop and halt instructions. It takes its instructions
from the `image` binary file made by a very simple assembler:
`scripts/assembler.py`.

Flow control (Jumps) and logical operations are being planned for the
next iteration, Georgios 3.
