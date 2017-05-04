from pathlib import Path
from argparse import ArgumentParser

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

# Build Applicaiton Data
appdata = []

# Magic Numbers
ASSEMBLY_MAGIC_NUMBER = "georgios;assembly;;\n",
BINARY_MAGIC_NUMBER = "georgios;binary;;\n",

# Registers
SPECIAL_REGISTERS = [
    "cflags",
    "pc",
    "aflags",
    "ahi",
    "amem",
]
TOTAL_NO_REGISTERS = 16
NO_GENRAL_REGISTERS = TOTAL_NO_REGISTERS - len(SPECIAL_REGISTERS)

# OPS
OPS = [
    "nop", 0x00,

    "set", 0x02,
    "copy", 0x03,

    "savevv", 0x04,
    "savevr", 0x05,
    "saverv", 0x06,
    "saverr", 0x07,
    "loadv", 0x08,
    "loadr", 0x09,

    "in", 0x0a,
    "out", 0x0b,

    "gotov", 0x0c,
    "gotor", 0x0d,
    "ifv", 0x0e,
    "ifr", 0x0f,

    "addr", 0x20,
    "addv", 0x21,
    "subr", 0x22,
    "subv", 0x23,

    "ltv", 0x34,

    "halt", 0xff,
]


# Constants
MAX_WORD_SIZE = 32
MAX_ARGUMENTS = 3

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
word_size = 0
word = ''
add_to_word = False

# Current Array
array_start = 0
array_size = 0
got_character = 0
character = 0
escape = False

# Current Instruction
instruction = False
arguments = 0
fill = 0

# Product
image_size = 0
image = []

# Main Loop
c = 1
running = True
stream_index = 20
while running:
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
            array_start = image_size
            array_size = 0
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


print('===============================================================================\n')

for i in image:
    print(repr(i))
