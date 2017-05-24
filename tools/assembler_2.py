import sys
from pathlib import Path
from argparse import ArgumentParser

class Memory:
    def __init__(self, size):
        self.size = size
        self.data = [None] * size
        self.edge = 0
        self.labels = {}

    def add_value(self, value):
        self.data[self.edge] = value
        self.edge += 1

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.data[key]
        elif isinstance(key, str):
            return self.labels[key]
        raise TypeError('Key must be int or str')

    def __setitem__(self, key, value):
        if isinstance(key, int):
            if key >= self.size:
                raise IndexError
            self.data[key] = value
        elif isinstance(key, str):
            self.labels[key] = self.edge
            if isinstance(value, str):
                l = len(value)
                self.add_value(l)
                for i in range(0, l):
                    self.add_value(value[i])
            elif isinstance(value, list):
                l = len(value)
                self.add_value(l)
                for i in range(0, l):
                    self[key] = value[i]
            elif isinstance(value, tuple):
                l = len(value)
                for i in range(0, l):
                    self[key] = value[i]
            else:
                self.add_value(value)

m = Memory(1024)

# Parse arguments
parser = ArgumentParser()
parser.add_argument('source', type=Path)
parser.add_argument('binary', type=Path)
parser.add_argument('-v', dest='verbose', action='store_true')

args = parser.parse_args()
source = args.source
binary = args.binary
verbose = args.verbose

# Read Source
stream = source.read_text()
stream_legnth = len(stream)

# Magic Numbers
m['ASSEMBLY_MAGIC_NUMBER'] = "georgios;assembly;;\n"
m['BINARY_MAGIC_NUMBER'] = "georgios;binary;;\n"

# Registers
m['SPECIAL_REGISTERS'] = [
    "cflags",
    "pc",
    "aflags",
    "ahi",
    "mem",
]
m['TOTAL_NO_REGISTERS'] = 16
m['NO_GENRAL_REGISTERS'] = m['TOTAL_NO_REGISTERS'] - m['SPECIAL_REGISTERS']

# OPS
m['OPS'] = [
    ("nop", 0x00, 0, 0, 0),
    ("=:", 0x01, 2, 1, 4),
    ("save", 0x02, 2, 0, 0),
    ("load", 0x03, 2, 1, 4),
    ("if", 0x04, 2, 1, 4),
    ("goto", 0x05, 1, 0, 0),
    ("if!", 0x06, 2, 1, 4),
    ("in", 0x08, 3, 0, 7),
    ("out", 0x09, 3, 0, 3),
    ("+", 0x20, 3, 1, 4),
    ("-", 0x21, 3, 1, 4),
    ("++", 0x22, 1, 0, 4),
    ("--", 0x23, 1, 0, 4),
    ("*u", 0x24, 3, 1, 4),
    ("/u", 0x25, 3, 1, 4),
    ("*s", 0x26, 3, 1, 4),
    ("/s", 0x27, 3, 1, 4),
    ("&&", 0x28, 3, 1, 4),
    ("||", 0x29, 3, 1, 4),
    ("<<", 0x2A, 3, 1, 4),
    (">>", 0x2B, 3, 1, 4),
    (">>>", 0x2C, 3, 1, 4),
    ("&", 0x2D, 3, 1, 4),
    ("|", 0x2E, 3, 1, 4),
    ("^", 0x2F, 3, 1, 4),
    ("==", 0x30, 3, 1, 4),
    ("!=", 0x31, 3, 1, 4),
    (">", 0x32, 3, 1, 4),
    (">=", 0x33, 3, 1, 4),
    ("<", 0x34, 3, 1, 4),
    ("<=", 0x35, 3, 1, 4),
    ("~", 0x36, 2, 0, 4),
    ("!", 0x37, 2, 0, 4),
    ("halt", 0x3f, 0, 0, 0),
]

# Constants
m['MAX_WORD_SIZE'] = 32
m['MAX_ARGUMENTS'] = 3

# States
STATE_NEW_WORD = 0
STATE_VALUE = 1
STATE_HEX_VALUE = 2
STATE_OP = 3
STATE_ARGUMENTS = 4
STATE_REGISTER = 5
STATE_SPECIAL_REGISTER = 6
STATE_GENERAL_REGISTER = 7
STATE_LABEL = 8
STATE_LABEL_INSERT = 9
STATE_STRING = 10
STATE_CHARACTER = 11
STATE_END_WORD = 12
STATE_END_LINE = 13
STATE_COMMENT = 14
STATE_IGNORE_TO_END_LINE = 15

state = STATE_NEW_WORD

# Current Word
m['word'] = [ None ] * m[m['MAX_WORD_SIZE']]
m[m['word']] = 0
m['add_to_word'] = False

# Array Building List
m['array_list_size'] = 0
m['array_list_head'] = 0
m['array_list_current'] = 0

# Current Array
array_start = 0
array_size = 0
got_character = 0
character = 0
escape = False

# Current Instruction
m['instruction'] = False
m['arguments'] = 0

# Product
m['image_size'] = 0
m['image'] = 0

print(m.data)
sys.exit(0)

# Main Loop
c = 1
running = True
stream_index = 20
while True:
    if stream_index < stream_legnth:
        c = stream[stream_index]
        stream_index += 1
    else:
        c = '\0'
        
# New Word State =============================================================

    if state == STATE_NEW_WORD:

        if c == '\n' or c == '\0':
            state = STATE_END_LINE
        elif c == ' ':
            pass
        elif c.isalpha() and not instruction: # OP
            state = STATE_OP
            instruction = True
            add_to_word = True
        elif c == ':' and not instruction: # Label
            state = STATE_LABEL
            add_to_word = True
            continue
        elif c == '@' and instruction: # Label Insert
            state = STATE_LABEL_INSERT
            add_to_word = True
            if instruction:
                arguments += 1
            continue
        elif c.isdigit(): # Direct Insert Value
            state = STATE_VALUE
            add_to_word = True
            if instruction:
                arguments += 1
        elif c == '#': # Direct Insert Value
            state = STATE_HEX_VALUE
            if instruction:
                arguments += 1
            add_to_word = True
            continue
        elif c == '%' and instruction:
            state = STATE_REGISTER
            if instruction:
                arguments += 1
            add_to_word = True
            continue
        elif c == '"' and not instruction: # Begin String
            state = STATE_STRING
            array_list_head = m.allocate(2)
            array_list_size = 0
            image.append(0)
            continue
        elif c == '\'' and not instruction: # Begin Character
            state = STATE_CHARACTER
            character = 0
            continue
        elif c == '/':
            state = STATE_COMMENT
            continue
        else:
            print('Invalid first character in word: {}'.format(repr(c)))
            break

# Word States ================================================================

# LABEL
    if state == STATE_LABEL:
        if c == ' ' or c == '\n' or c == '\0':
            print('LABEL:', repr(word))
            state = STATE_END_WORD
        elif c.isalnum() or c == '_':
            pass
        else:
            print('Invalid character in label: {}'.format(repr(c)))
            break

# LABEL INSERT
    elif state == STATE_LABEL_INSERT:
        if c == ' ' or c == '\n' or c == '\0':
            print('LABEL INSERT:', repr(word))
            state = STATE_END_WORD
        elif c.isalnum() or c == '_':
            pass
        else:
            print('Invalid character in label insert: {}'.format(repr(c)))
            break

# OP
    elif state == STATE_OP:
        if c == ' ' or c == '\n' or c == '\0':
            print('OP:', repr(word))
            state = STATE_END_WORD
        elif c.isalpha():
            pass
        else:
            print('Invalid character in op: {}'.format(repr(c)))
            break

# VALUE
    elif state == STATE_VALUE:
        if c == ' ' or c == '\n' or c == '\0':
            print('VALUE:', repr(word))
            state = STATE_END_WORD
        elif c.isdigit():
            pass
        else:
            print('Invalid character in value: {}'.format(repr(c)))
            break

# HEX VALUE
    elif state == STATE_HEX_VALUE:
        if c == ' ' or c == '\n' or c == '\0':
            print('HEX VALUE:', repr(word))
            state = STATE_END_WORD
        elif c.isdigit() or c in 'abcdefABCDEF':
            pass
        else:
            print('Invalid character in hex: {}'.format(repr(c)))
            break

# REGISTER
    elif state == STATE_REGISTER:
        if c.isalpha():
            state = STATE_SPECIAL_REGISTER
        elif c.isdigit():
            state = STATE_GENERAL_REGISTER
        else:
            print('Invalid character after register symbol: {}'.format(repr(c)))
            break

# SPECIAL REGISTER
    elif state == STATE_SPECIAL_REGISTER:
        if c == ' ' or c == '\n':
            print('SPECIAL REGISTER:', repr(word))
            state = STATE_END_WORD
        elif c.isalpha():
            pass
        else:
            print('Invalid character in special register: {}'.format(repr(c)))
            break

# GENERAL REGISTER
    elif state == STATE_GENERAL_REGISTER:
        if c == ' ' or c == '\n':
            print('GENERAL REGISTER:', repr(word))
            state = STATE_END_WORD
        elif c.isdigit():
            pass
        else:
            print('Invalid character in general register: {}'.format(repr(c)))
            break

# STRING
    elif state == STATE_STRING:
        if escape:
            escape = False
            array_size += 1
            if c == '\\':
                image.append('\\')
            elif c == 'n':
                image.append('\n')
            elif c == '"':
                image.append('"')
            else:
                print('Invalid escaped character in string: {}'.format(repr(c)))
                break
        elif c == '\\':
            escape = True
        elif c == '"':
            image[array_start] = array_size
            print('STRING with', array_size, 'elements')
            state = STATE_END_WORD
        else:
            array_size += 1
            image.append(c)

# CHARACTER
    elif state == STATE_CHARACTER:
        if got_character:
            if c == '\'':
                print('CHARACTER:', repr(character))
                state = STATE_END_WORD
            else:
                print('Invalid character in character literal: {}'.format(repr(c)))
                break
        else:
            if escape:
                escape = False
                got_character = True
                if c == '\\':
                    character = '\\'
                elif c == 'n':
                    character = '\n'
                elif c == '\'':
                    character = '\''
                else:
                    print('Invalid escaped character in character: {}'.format(repr(c)))
                    break
            elif c == '\\':
                escape = True
            else:
                got_character = True
                character = c

# Single Line Comment
    elif state == STATE_COMMENT:
        if c == '/':
            state = STATE_IGNORE_TO_END_LINE
        else:
            print('Invalid comment: {}'.format(repr(c)))
            break

    if state == STATE_IGNORE_TO_END_LINE:
        if c == '\n' or c == '\0':
            state = STATE_END_LINE
        else:
            continue

# End Word State =============================================================
    if state == STATE_END_WORD:
        word_size = 0
        word = ''
        add_to_word = False
        if instruction and arguments:
            print('   is Argument {}'.format(arguments))

        if c == ' ':
            state = STATE_NEW_WORD
        else:
            state = STATE_END_LINE


# End Line State =============================================================
    if state == STATE_END_LINE:
        if instruction:
            print('END INSTRUCTION, fill:', MAX_ARGUMENTS - arguments)
            instruction = False
            arguments = 0
        state = STATE_NEW_WORD

        if c == '\0':
            running = False

# Add character to current word
    if add_to_word:
        if word_size == MAX_WORD_SIZE:
            print('WORD TOO BIG')
            break
        word_size += 1
        word += c

    if not running:
        break

print('===============================================================================\n')

for i in image:
    print(repr(i))
