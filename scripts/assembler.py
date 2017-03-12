import sys
from pathlib import Path

NUMBER_OF_ARGUMENTS = 3

if len(sys.argv) != 2:
    sys.exit('usage: {} INPUT_PATH'.format(sys.argv[0]))

input_path = Path(sys.argv[1])
output_path = Path("image")

ops = {
    "halt": 0,
    "nop":  1,
    "set":  2,
    "copy": 3,
    "addr": 4,
    "addv": 5,
    "subr": 6,
    "subv": 7,
}

image = []

for lineno, line in enumerate(input_path.read_text().split('\n')):
    if line and line.lstrip()[0] != '#':
        print("{}: \"{}\"".format(lineno, line))
        parts = line.split()
        op = ops[parts[0]]
        instruction = [op]
        arguments = [list(i) for i in parts[1:]]
        for i in range(0, NUMBER_OF_ARGUMENTS):
            if i < len(arguments):
                instruction.extend([int(n, 16) for n in arguments[i]])
            else:
                instruction.extend([0])
        print('   ', instruction)
        image.extend(instruction)

output_path.write_bytes(bytes(image))

