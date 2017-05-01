#!/usr/bin/env python3

import sys
from pathlib import Path
import re

assembly_magic_number = "georgios;assembly;;"
binary_magic_number = b'georgios;binary;;\n'

LINE_COMMENT_RE = re.compile(r'\/\/')

LABEL_RE = re.compile(
    r'^(\w+)\:'
)

STRING_RE = re.compile(
    r'\".*\"'
)

NUMBER_OF_ARGUMENTS = 3

LABEL_SYMBOL = '@'
HEX_SYMBOL = '#'
REGISTER_SYMBOL = "%"

REGISTERS = [
    "cflags",
    "pc",
    "i0",
    "i1",
    "i2",
    "i3",
    "aop",
    "aflags",
    "ahi"
]

OPS = {
    "nop":  0x00,
    "output": 0x01,
    "set":  0x02,
    "copy": 0x03,

    "savevv": 0x04,
    "savevr": 0x05,
    "saverv": 0x06,
    "saverr": 0x07,
    "loadv": 0x08,
    "loadr": 0x09,

    "in": 0x0a,
    "out": 0x0b,

    "gotov": 0x0c,
    "gotor": 0x0d,
    "ifv": 0x0e,
    "ifr": 0x0f,

    "addr": 0x20,
    "addv": 0x21,
    "subr": 0x22,
    "subv": 0x23,

    "ltv": 0x34,

    "halt": 0xff,
}

def treat(line):
    m = LINE_COMMENT_RE.search(line)
    if m:
        return line[:m.start()].rstrip()
    return line

def get_register(argument):
    value = argument.split(REGISTER_SYMBOL)[1]
    if value in REGISTERS: # Special Purpose Register
        return str(REGISTERS.index(value))
    elif value.isdecimal(): # General Purpose Register
        return str(int(value) + len(REGISTERS))

    sys.exit(1)

def convert(line):
    '''Convert instructions into numbers that fit into 
    correct sized list
    '''
    parts = line.split()
    instruction = [OPS[parts[0]]]

    label_inserts = {}

    for i, p in enumerate(parts):
        if p.startswith(REGISTER_SYMBOL):
            parts[i] = get_register(p)
        elif p.startswith(LABEL_SYMBOL):
            label = p.split(LABEL_SYMBOL)[1]
            if label in label_inserts:
                label_inserts[label].append(i)
            else:
                label_inserts[label] = [i]
            parts[i] = '0'

    arguments = [i for i in parts[1:]]
    for i in range(0, NUMBER_OF_ARGUMENTS):
        if i < len(arguments):
            instruction.append(int(arguments[i], 16))
        else:
            instruction.append(0)

    return instruction, label_inserts

def main(source, binary, verbose):

    image = []
    labels = {}
    label_inserts = {}

    lines = source.read_text().split('\n')
    if not lines[0].startswith(assembly_magic_number):
        sys.exit('Input files first line must be: "{}"'.format(
            assembly_magic_number
        ))

    for lineno, line in enumerate(lines[1:]):
        striped_line = line.strip()

        if not striped_line:
            continue

        if verbose:
            print("{}: \"{}\"".format(lineno, line))

        treated_line = treat(striped_line)

        if not treated_line:
            continue

        m = LABEL_RE.search(treated_line)
        if m:
            labels[m.groups()[0]] = len(image) // (NUMBER_OF_ARGUMENTS + 1)
            treated_line = treated_line[m.end():].lstrip()
            if not treated_line:
                continue

        instruction, line_label_inserts = convert(treated_line)

        for k, v in line_label_inserts.items():
            if k not in label_inserts:
                label_inserts[k] = []
            for i in v:
                label_inserts[k].append(len(image) + i)

        if verbose:
            print('   ', instruction)
        image.extend(instruction)

    if verbose:
        print('Labels:', labels)
        print('Label Inserts:', label_inserts)
        print('Semi Final Image:', image)

    for k, v in label_inserts.items():
        if k not in labels:
            sys.exit('Invalid Label')

        for i in v:
            image[i] = labels[k]

    new = []
    for i in image:
        new.extend([i, 0])
            
    image = new

    if verbose:
        print('Image:', image)

    binary.write_bytes(binary_magic_number + bytes(image))

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('binary', type=Path)
    parser.add_argument('-v', dest='verbose', action='store_true')

    args = parser.parse_args()

    main(args.source, args.binary, args.verbose)

