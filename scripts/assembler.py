import sys
from pathlib import Path
import re

LINE_COMMENT_RE = re.compile(r'\/\/')

LABEL_RE = re.compile(
    r'^(\w+)\:'
)

NUMBER_OF_ARGUMENTS = 3

OPS = {
    "halt": 0,
    "nop":  1,
    "set":  2,
    "copy": 3,
    "addr": 4,
    "addv": 5,
    "subr": 6,
    "subv": 7,
}

def treat(line):
    m = LINE_COMMENT_RE.search(line)
    if m:
        return line[:m.start()].rstrip()
    return line

def convert(line):
    '''Convert instructions into numbers that fit into 
    correct sized list
    '''
    parts = line.split()
    op = OPS[parts[0]]
    instruction = [op]
    arguments = [list(i) for i in parts[1:]]
    for i in range(0, NUMBER_OF_ARGUMENTS):
        if i < len(arguments):
            instruction.extend([int(n, 16) for n in arguments[i]])
        else:
            instruction.extend([0])
    return instruction

def main(source, verbose):

    output_path = Path("image")

    image = []
    labels = {}

    for lineno, line in enumerate(source.read_text().split('\n')):
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

        instruction = convert(treated_line)
        if verbose:
            print('   ', instruction)
        image.extend(instruction)

    print(labels)
    output_path.write_bytes(bytes(image))

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('-v', dest='verbose', action='store_true')

    args = parser.parse_args()

    main(args.source, args.verbose)

