# Georgios Assembly

Georgios Assembly consists of `georgios;assembly;;` on the first line followed
by lines that can contain space seperated data literals, one instruction,
or nothing.
Each line can also begin with a label and end with a comment.

## A Few Notes on Arrays and Strings
Many arrays are "prefixed", which means that the first element is the size of
the arrays.
This includes essentially all strings, so Georgios strings are NOT
null-terminated strings.

The character encoding for strings is ASCII and strings should be half word
arrays.

## Comments

```
nop ; This is a comment
```

Comments can go anywhere, but will take up the rest of the line (like a single
line comment `\\` in C languages).
An important thing to remember is an instruction can not span multiple lines,
so you can't put a comment in the middle of a instruction.

## Literals

All literals can be inserted into memory outside of instructions.
Decimals and hexadecimals are the only literals that can be used as operands
in an instruction.

### Decimals

```
0
1
-23
```

Decimal integers are represented simply as is.
They can be negative.
There is currently NO support for floating or "real" numbers such as 9.75.

### Hexadecimals

```
#1
#0A
#FFFF
```

Hexadecimal values begin with `#`.
They can not be negative and must be 1, 2, or 4 digits in length.

### Characters

```
'a'
'1'
'\''
'\n'
'\\'
```

Characters are half word ASCII encoded characters.

### Strings

```
""
"Hello Georgios!"
"This is a line\nThis is another line"
"\"This is a quote inside a string!\""
```

Strings are size prefixed, ASCII, half word arrays.

## Registers

[See registers for complete view of registers](registers.md)

```
%pc ; Special Register
%0 ; First General Register
```

Registers can only be used as instruction operands. There are special
registers, all of which are read only. There are also general use registers
which are numbered.

## Labels
### Label Definitions

Labels give names to places in memory.
Each label can only be defined once per file, two labels can't have the same
name in the same file.

```
zero: 0
zero_string: "ZERO"
goto_zero:
    goto 0
```

Labels are not accessible across files unless the colon is doubled as such:

```
goto_one::
    goto 1
```

Global and local labels are separate collections.
You can have a global label definition and a local label definition that have
the same name in the same file.

### Label Inserts

```
load %0 @zero
goto @@goto_one
```

## Instructions

[See Instructions Set for complete view of Instructions](Instruction_Set.md)

```
= %0 2     ; %0 = 2
= %1 3     ; %1 = 3
+ %2 %0 %1 ; %2 = %0 + %1 = 5
-- %2      ; %2 = %2 - 1 = 4
- %2 %2 4  ; %2 = %2 - 4 = 0
```

### Special/Signed Marker

Arithmatic operations followed by `$` are interpreted as signed operations.
<!-- Branching instructions (`goto`, `if`, and, `if!`) interpret it as an offset to
the current PC. 

```
* %0 %
goto 10 ; %pc = 10
goto 10 ; %pc = %pc + 10
```
-->

### Byte Markers

Operations followed by `'` or `"` interact only with the lower or upper bytes
of their operands respectively.

```
= %0 #7700
= %1 #FF33
add' %0 %1 #FF44 ; %0 = 0x7777
add" %0 %1 #0200 ; %0 = 0x0177
```
