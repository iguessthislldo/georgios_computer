# Georgios
My explorations in computer design. Currently simulated with custom VM
written in C++ with schematics in
[gschem](http://wiki.geda-project.org/geda:gaf).

## [Instruction Set](docs/Instruction_Set.md)
Instructions are 1 to 4 16 bit words. Includes branching, arithmetic, and,
logical instructions.

## [Assembly](docs/Assembly.md)
Georgios Assembly is somewhat inspired by AT&T Syntax, but does not follow
any external conventions for the most part and is mostly unstructured.

### Example
Print a String:

```
georgios;assembly;;

STRING: "Hello World!\n" ; String to print

= %0 @STRING
++ %0 ; %0 is the pointer, now at the beginning of the string
load %1 @STRING
+ %1 %0 %1 ; %1 is the end of the string

Loop:
    - %2 %1 %0 ; %2 is the number of characters left
    load %3 0 0
    out 0 0 %3 ; Output the current character
    if %2 @Loop ; Go back if there are characters left

halt ; Done
```
