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
        if isinstance(value, tuple):
            for i in value:
                self.add_value(i)
        elif isinstance(value, list):
            l = len(value)
            self.add_value(l)
            for i in range(0, l):
                self.add_value(value[i])
        elif isinstance(value, str):
            l = len(value)
            self.add_value(l)
            for i in range(0, l):
                self.data[self.edge] = value[i]
                self.edge += 1
        else:
            self.data[self.edge] = value
            self.edge += 1

    def l(self, label):
        return self.labels[label]

    def get_string(self, key):
        location = None
        if isinstance(key, int):
            location = key
        elif isinstance(key, str):
            location = self.labels[key]

        length = self.data[location]
        s = ""
        for i in range(1, length + 1):
            s += self.data[location + i]
        return s

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.data[key]
        elif isinstance(key, str):
            return self.data[self.labels[key]]
        raise TypeError('Key must be int or str')

    def __setitem__(self, key, value):
        if isinstance(key, int):
            if key >= self.size:
                raise IndexError
            self.data[key] = value
        elif isinstance(key, str):
            if key in self.labels:
                self.data[self.labels[key]] = value
            else:
                self.labels[key] = self.edge
                self.add_value(value)

    def print(self):
        label_max_size = 0
        for k, v in self.labels.items():
            l = len(k)
            if l > label_max_size:
                label_max_size = l

        number_size = len(str(self.size))
        string = " {:" + str(number_size) + "}  =  {}"
        label_string = "{:<" + str(label_max_size) + "} :" + string
        no_label_string = " " * (label_max_size + 2) + string
        last_value_was_none = False

        for i in range(0, self.size):
            label = None
            for k, v in self.labels.items():
                if v == i:
                    label = k

            value = self.data[i]
            if value is not None:
                last_value_was_none = False
                if label is None:
                    print(no_label_string.format(i, repr(value)))
                else:
                    print(label_string.format(label, i, repr(value)))
            else:
                if not last_value_was_none:
                    print(' ..................................')
                last_value_was_none = True
                    

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

# Constants
m['MAX_WORD_SIZE'] = 32
m['MAX_ARGUMENTS'] = 3

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

def fixed(size, string):
    l = len(string)
    if l > size:
        sys.exit("String too big for fixed sized string")
    return tuple([string] + ([ None ] * (size - l)))

# OPS
max_op_size = 5
op_element_size = 1 + max_op_size + 4
m['OPS'] = [
    (fixed(max_op_size, "nop"), 0x00, 0, 0, 0),
    (fixed(max_op_size, "="), 0x01, 2, 1, 4),
    (fixed(max_op_size, "save"), 0x02, 2, 0, 0),
    (fixed(max_op_size, "load"), 0x03, 2, 1, 4),
    (fixed(max_op_size, "if"), 0x04, 2, 1, 4),
    (fixed(max_op_size, "goto"), 0x05, 1, 0, 0),
    (fixed(max_op_size, "if!"), 0x06, 2, 1, 4),
    (fixed(max_op_size, "in"), 0x08, 3, 0, 7),
    (fixed(max_op_size, "out"), 0x09, 3, 0, 3),
    (fixed(max_op_size, "+"), 0x20, 3, 1, 4),
    (fixed(max_op_size, "-"), 0x21, 3, 1, 4),
    (fixed(max_op_size, "++"), 0x22, 1, 0, 4),
    (fixed(max_op_size, "--"), 0x23, 1, 0, 4),
    (fixed(max_op_size, "*u"), 0x24, 3, 1, 4),
    (fixed(max_op_size, "/u"), 0x25, 3, 1, 4),
    (fixed(max_op_size, "*s"), 0x26, 3, 1, 4),
    (fixed(max_op_size, "/s"), 0x27, 3, 1, 4),
    (fixed(max_op_size, "&&"), 0x28, 3, 1, 4),
    (fixed(max_op_size, "||"), 0x29, 3, 1, 4),
    (fixed(max_op_size, "<<"), 0x2A, 3, 1, 4),
    (fixed(max_op_size, ">>"), 0x2B, 3, 1, 4),
    (fixed(max_op_size, ">>>"), 0x2C, 3, 1, 4),
    (fixed(max_op_size, "&"), 0x2D, 3, 1, 4),
    (fixed(max_op_size, "|"), 0x2E, 3, 1, 4),
    (fixed(max_op_size, "^"), 0x2F, 3, 1, 4),
    (fixed(max_op_size, "=="), 0x30, 3, 1, 4),
    (fixed(max_op_size, "!="), 0x31, 3, 1, 4),
    (fixed(max_op_size, ">"), 0x32, 3, 1, 4),
    (fixed(max_op_size, ">="), 0x33, 3, 1, 4),
    (fixed(max_op_size, "<"), 0x34, 3, 1, 4),
    (fixed(max_op_size, "<="), 0x35, 3, 1, 4),
    (fixed(max_op_size, "~"), 0x36, 2, 1, 4),
    (fixed(max_op_size, "!"), 0x37, 2, 1, 4),
    (fixed(max_op_size, "halt"), 0x3f, 0, 0, 0),
]
m['word_index'] = 0
m['op_index'] = 0
m['op_matched'] = False

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
STATE_UNCERTAIN = 16
STATE_MATCH_OP = 17

state = STATE_NEW_WORD

# Current Word
word_size = m['MAX_WORD_SIZE'] + 1
word_list = [ None ] * word_size
m['word'] = word_list
m['word'] = 0
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
        elif c.isdigit(): # Direct Insert Value
            state = STATE_VALUE
            m['add_to_word'] = True
            if m['instruction']:
                m['arguments'] += 1
        elif c == '@' and m['instruction']: # Label Insert
            state = STATE_LABEL_INSERT
            m['add_to_word'] = True
            if m['instruction']:
                m['arguments'] += 1
            continue
        elif c == '#': # Direct Insert Value
            state = STATE_HEX_VALUE
            m['add_to_word'] = True
            if m['instruction']:
                m['arguments'] += 1
            continue
        elif c == '%' and m['instruction']:
            state = STATE_REGISTER
            m['add_to_word'] = True
            if m['instruction']:
                m['arguments'] += 1
            continue
        elif c == '"' and not m['instruction']: # Begin String
            state = STATE_STRING
            array_list_head = m.allocate(2)
            array_list_size = 0
            image.append(0)
            continue
        elif c == '\'' and not m['instruction']: # Begin Character
            state = STATE_CHARACTER
            character = 0
            continue
        elif c == ';':
            state = STATE_IGNORE_TO_END_LINE
            continue
        else:
            state = STATE_UNCERTAIN
            m['add_to_word'] = True
# Word States ================================================================

# LABEL INSERT
    if state == STATE_LABEL_INSERT:
        if c == ' ' or c == '\n' or c == '\0':
            print('LABEL INSERT:', repr(m.get_string('word')))
            state = STATE_END_WORD
        elif c.isalnum() or c == '_':
            pass
        else:
            print('Invalid character in label insert: {}'.format(repr(c)))
            break

# VALUE
    elif state == STATE_VALUE:
        if c == ' ' or c == '\n' or c == '\0':
            print('VALUE:', repr(m.get_string('word')))
            state = STATE_END_WORD
        elif c.isdigit():
            pass
        else:
            print('Invalid character in value: {}'.format(repr(c)))
            break

# HEX VALUE
    elif state == STATE_HEX_VALUE:
        if c == ' ' or c == '\n' or c == '\0':
            print('HEX VALUE:', repr(m.get_string('word')))
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
            print('GENERAL REGISTER:', repr(m.get_string('word')))
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
    elif state == STATE_IGNORE_TO_END_LINE:
        if c == '\n' or c == '\0':
            state = STATE_END_LINE
        else:
            continue

# Add characters to word until ':', ' ', '\n' or '\0'
    elif state == STATE_UNCERTAIN:
        if c == '\n' or c == '\0' or c == ' ':
            #m.print()
            #sys.exit()
            m['op_index'] = 0
            while True: # Iterate OPS
                    
                m['word_index'] = 0
                m['op_matched'] = False
                while True: # Iterate Characters
                    word_char = m[m.l('word') + m['word_index']]
                    op_char = m[m.l('OPS') + 1 + op_element_size * m['op_index'] + m['word_index']]
                    if word_char != op_char:
                        break
                    m['word_index'] += 1
                    if m['word_index'] == m['word']:
                        m['op_matched'] = True
                        break

                if m['op_matched']:
                    break
                    
                m['op_index'] += 1

                if m['op_index'] == m['OPS']:
                    print('NOT AN OP')
                    sys.exit()
                
            m['instruction'] = True
            print('OP:', repr(m.get_string('word')))
            state = STATE_END_WORD
        elif c == ':':
            print('LABEL DEFINED:', repr(m.get_string('word')))
            state = STATE_END_WORD

# End Word State =============================================================
    if state == STATE_END_WORD:
        m['word'] = 0
        m['add_to_word'] = False
        if m['instruction'] and m['arguments']:
            print('   is Argument {}'.format(m['arguments']))

        if c == ' ':
            state = STATE_NEW_WORD
        else:
            state = STATE_END_LINE

# End Line State =============================================================
    if state == STATE_END_LINE:
        if m['instruction']:
            print('END INSTRUCTION, fill:', m['MAX_ARGUMENTS'] - m['arguments'])
            m['instruction'] = False
            m['arguments'] = 0
        state = STATE_NEW_WORD

        if c == '\0':
            running = False

# Add character to current word
    if m['add_to_word']:
        if m['word'] == m['MAX_WORD_SIZE']:
            print('WORD TOO BIG')
            sys.exit(1)
        m['word'] += 1
        m[m.l('word') + m['word']] = c
        
    if not running:
        break

print('===============================================================================\n')

#m.print()
