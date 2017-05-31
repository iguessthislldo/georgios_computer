# Georgios Prototype Assemmbler

import sys
from pathlib import Path
from argparse import ArgumentParser

def fixed(size, string):
    '''Create fixed size string for Memory class
    '''
    l = len(string)
    if l > size:
        sys.exit("String too big for fixed sized string")
    return tuple([string] + ([ None ] * (size - l)))

class Memory:
    ''' Simulation of linear memory space
    '''

    def __init__(self, size):
        self.size = size
        self.data = [None] * size
        self.edge = 0
        self.labels = {}

    def add_value(self, value):
        '''Add a single value to the memory, push edge back.
        '''
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
        '''Shortcut for getting label values
        '''
        return self.labels[label]

    def get_string(self, key):
        '''Build georgios string located at key and return python string
        '''
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
            if key == 509:
                print('============================ m[509] =', value)
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
        '''Print Memory space, skips uninitiated space
        '''
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

# Constants ==================================================================
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
m['NO_GENERAL_REGISTERS'] = m['TOTAL_NO_REGISTERS'] - m['SPECIAL_REGISTERS']

# OPS
max_op_size = 5
op_element_size = 1 + max_op_size + 4
m['OPS'] = [
# String Value, Op Code, Number of arguments, Indirection Offset,
                                                    #Forced Register Mask
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

IMAGE_MAX_CONTENT = 5
IMAGE_CHUNK_SIZE = 2 + IMAGE_MAX_CONTENT # includes metadata and content

# Variables ==================================================================

state = STATE_NEW_WORD # Should stay in registers

m['line'] = 1

# OP Searching
m['word_index'] = 0
m['op_index'] = 0
m['op_matched'] = False

# Current Word
m['word'] = [ None ] * (m['MAX_WORD_SIZE'] + 1)
m['word'] = 0
m['add_to_word'] = False

# Current Array
m['array_start'] = 0
m['array_size'] = 0
m['set_array_start'] = False
m['got_character'] = 0
m['character'] = 0
m['escape'] = False

# Current Instruction
m['instruction'] = False
m['arguments'] = 0
m['no_arguments'] = 0 # Number of arguments the current instruction needs
m['indirection_offset'] = 0
m['register_mask'] = 0
m['register_value'] = 0

# Product Image
m['set_inst_start'] = False
m['inst_start'] = 0
# Image list format is NEXT, [SIZE, CONTENT]
m['image_head'] = 0
m['image_tail'] = 0
m['image_size'] = 0

# Label Definitions
# NEXT, LOCATION, [SIZE, CONTENT]
m['label_head'] = 0
m['label_tail'] = 0

# Label Inserts
# NEXT, LOCATION, [SIZE, CONTENT]
m['insert_head'] = 0
m['insert_tail'] = 0

def add_to_image(m, value):
    new_chunk = False
    prev = 0
    if m['image_head'] == 0:
        # No Chunks, create inital head
        m['image_tail'] = m['image_head'] = m.edge
        new_chunk = True
    elif m[m['image_tail'] + 1] == IMAGE_MAX_CONTENT:
        # Chunk is full, create new chunk
        prev = m['image_tail']
        m[m['image_tail']] = m.edge # Set Current Next to the next chunk
        m['image_tail'] = m.edge
        new_chunk = True

    if new_chunk: # Create New chunk
        m.edge += IMAGE_CHUNK_SIZE
        m[m['image_tail']] = 0
        m[m['image_tail'] + 1] = 0
    
    # Add value to chunk
    m['image_size'] += 1
    size = m[m['image_tail'] + 1]
    place = m['image_tail'] + 2 + size
    m[place] = value
    m[m['image_tail'] + 1] = size + 1

    if m['set_array_start']:
        m['array_start'] = place
        m['set_array_start'] = False

    if m['set_inst_start']:
        m['inst_start'] = place
        m['set_inst_start'] = False

# Main Loop ==================================================================
c = 1
running = True
stream_index = 20
while True:
    word_states = True
    if stream_index < stream_legnth:
        c = stream[stream_index]
        stream_index += 1
    else:
        c = '\0'

    if c == '\n':
        m['line'] += 1
        
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
        elif c == '#': # Direct Insert Hex Value
            state = STATE_HEX_VALUE
            m['add_to_word'] = True
            if m['instruction']:
                m['arguments'] += 1
            continue
        elif c == '%' and m['instruction']: # Register
            state = STATE_REGISTER
            m['add_to_word'] = True
            if m['instruction']:
                m['arguments'] += 1
            continue
        elif c == '"' and not m['instruction']: # Begin String
            state = STATE_STRING
            m['array_size'] = 0
            m['set_array_start'] = True
            add_to_image(m, 0)
            word_states = False
        elif c == '\'' and not m['instruction']: # Begin Character
            state = STATE_CHARACTER
            character = 0
            continue
        elif c == ';': # Comment
            state = STATE_IGNORE_TO_END_LINE
            continue
        else: # Uncertain if OP, label, or invalid character(s)
            state = STATE_UNCERTAIN
            m['add_to_word'] = True

# Word States ================================================================

    if word_states:
    # LABEL INSERT
        if state == STATE_LABEL_INSERT:
            if c == ' ' or c == '\n' or c == '\0':
                print('LABEL INSERT:', repr(m.get_string('word')))
                # NEXT, LOCATION, SIZE, CHAR0, ...
                if m['insert_head'] == 0:
                    m['insert_head'] = m.edge
                else:
                    m[m['insert_tail']] = m.edge
                m['insert_tail'] = m.edge
                m[m['insert_tail'] + 1] = m['image_size']
                size = m['word']
                m[m['insert_tail'] + 2] = size
                for i in range(0, size):
                    m[m['insert_tail'] + 3 + i] = m[m.l('word') + 1 + i]
                m.edge += (3 + size)

                # Placeholder value
                m['set_array_start'] = True
                add_to_image(m, 0)

                state = STATE_END_WORD
            elif c.isalnum() or c == '_':
                m['add_to_word'] = True
            else:
                print('Invalid character in label insert: {}'.format(repr(c)))
                break

    # VALUE
        elif state == STATE_VALUE:
            if c == ' ' or c == '\n' or c == '\0':
                print('VALUE:', repr(m.get_string('word')))
                # Convert word to value
                value = 0
                factor = 1
                done = m.l('word')
                pointer = done + m['word']
                while True:
                    if pointer == done:
                        break
                    value += factor * (ord(m[pointer]) - ord('0'))
                    factor *= 10
                    pointer -= 1
                add_to_image(m, value)
                state = STATE_END_WORD
            elif c.isdigit():
                m['add_to_word'] = True
            else:
                print('Invalid character in value: {}'.format(repr(c)))
                break

    # HEX VALUE
        elif state == STATE_HEX_VALUE:
            zero = ord('0')
            nine = ord('9')
            a = ord('a')
            f = ord('f')
            A = ord('A')
            F = ord('F')
            case = A - a
            if c == ' ' or c == '\n' or c == '\0':
                print('HEX VALUE:', repr(m.get_string('word')))
                # Convert word to value
                value = 0
                factor = 1
                done = m.l('word')
                pointer = done + m['word']
                while True:
                    if pointer == done:
                        break
                    char = m[pointer]
                    digit = 0
                    if zero <= ord(char) <= nine:
                        digit = ord(char) - zero
                    else:
                        digit = 10 + ord(char) - a
                    value += factor * digit
                    factor *= 16
                    pointer -= 1
                add_to_image(m, value)
                state = STATE_END_WORD
            else:
                if zero <= ord(c) <= nine or a <= ord(c) <= f:
                    m['add_to_word'] = True
                elif A <= ord(c) <= F:
                    c = c.lower()
                    m['add_to_word'] = True
                else:
                    print('Invalid character in hex: {}'.format(repr(c)))
                    break

    # REGISTER
        elif state == STATE_REGISTER:
            m['register_value'] |= 8 >> m['arguments']
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
                m['add_to_word'] = True
            else:
                print('Invalid character in special register: {}'.format(repr(c)))
                break

    # GENERAL REGISTER
        elif state == STATE_GENERAL_REGISTER:
            if c == ' ' or c == '\n':
                print('GENERAL REGISTER:', repr(m.get_string('word')))
                # Convert word to value
                value = 0
                factor = 1
                done = m.l('word')
                pointer = done + m['word']
                while True:
                    if pointer == done:
                        break
                    value += factor * (ord(m[pointer]) - ord('0'))
                    factor *= 10
                    pointer -= 1
                add_to_image(m, value + m['SPECIAL_REGISTERS'])
                state = STATE_END_WORD
            elif c.isdigit():
                m['add_to_word'] = True
            else:
                sys.exit('Line {}: Invalid character in general register: {}'.format(m['line'], repr(c)))

    # STRING
        elif state == STATE_STRING:
            if m['escape']:
                m['escape'] = False
                m['array_size'] += 1
                if c == '\\':
                    add_to_image(m, '\\')
                elif c == 'n':
                    add_to_image(m, '\n')
                elif c == '"':
                    add_to_image(m, '"')
                else:
                    sys.exit('Line {}: Invalid escaped character in string: {}'.format(m['line'], repr(c)))
            elif c == '\\':
                m['escape'] = True
            elif c == '"':
                m[m['array_start']] = m['array_size']
                print('STRING with', m['array_size'], 'elements')
                state = STATE_END_WORD
            else:
                m['array_size'] += 1
                add_to_image(m, c)

    # CHARACTER
        elif state == STATE_CHARACTER:
            if m['got_character']:
                if c == '\'':
                    print('CHARACTER:', repr(m['character']))
                    add_to_image(m, m['character'])
                    state = STATE_END_WORD
                else:
                    sys.exit('Line {}: Invalid character literal: {}'.format(m['line'], repr(c)))
            else:
                if m['escape']:
                    m['escape'] = False
                    m['got_character'] = True
                    if c == '\\':
                        m['character'] = '\\'
                    elif c == 'n':
                        m['character'] = '\n'
                    elif c == '\'':
                        m['character'] = '\''
                    else:
                        sys.exit('Line {}: Invalid escaped character literal: {}'.format(m['line'], repr(c)))
                elif c == '\\':
                    m['escape'] = True
                else:
                    m['got_character'] = True
                    m['character'] = c

    # Single Line Comment
        elif state == STATE_IGNORE_TO_END_LINE:
            if c == '\n' or c == '\0':
                state = STATE_END_LINE
            else:
                continue

    # Uncertain if op or label
    # Add characters to word until ':', ' ', '\n' or '\0'
        elif state == STATE_UNCERTAIN:

            if c == '\n' or c == '\0' or c == ' ': # Match word to OP
                m['op_index'] = 0
                op_pointer = None
                while True: # Iterate OPS
                    m['word_index'] = 0
                    m['op_matched'] = False
                    while True: # Iterate Characters
                        word_char = m[m.l('word') + m['word_index']]
                        op_pointer = m.l('OPS') + 1 + op_element_size * m['op_index']
                        op_char = m[op_pointer + m['word_index']]
                        if word_char != op_char: # Failure on this op
                            break
                        m['word_index'] += 1
                        if m['word_index'] > m['word']: # Sucess on this op
                            m['op_matched'] = True
                            break
                    if m['op_matched']: # Sucess on search
                        break
                    m['op_index'] += 1
                    if m['op_index'] == m['OPS']: # Failure on search
                        print('NOT AN OP')
                        sys.exit()
                    
                m['instruction'] = True
                print('OP:', repr(m.get_string('word')))

                op_pointer += max_op_size + 1
                m['set_inst_start'] = True
                add_to_image(m, m[op_pointer])

                op_pointer += 1
                m['no_arguments'] = m[op_pointer]
                op_pointer += 1
                m['indirection_offset'] = m[op_pointer]
                op_pointer += 1
                m['register_mask'] = m[op_pointer]
                m['register_value'] = 0

                state = STATE_END_WORD

            elif c == ':': # Define Label
                # NEXT, LOCATION, SIZE, CHAR0, ...
                print('LABEL DEFINED:', repr(m.get_string('word')))
                if m['label_head'] == 0:
                    m['label_head'] = m.edge
                else:
                    m[m['label_tail']] = m.edge
                m['label_tail'] = m.edge
                m[m['label_tail'] + 1] = m['image_size']
                size = m['word']
                m[m['label_tail'] + 2] = size
                for i in range(0, size):
                    m[m['label_tail'] + 3 + i] = m[m.l('word') + 1 + i]
                m.edge += (3 + size)
                state = STATE_END_WORD

# End Word State =============================================================
    if state == STATE_END_WORD:
        m['word'] = 0
        m['add_to_word'] = False
        if m['instruction'] and m['arguments']:
            print('    is Argument {}'.format(m['arguments']))
        if c == ' ':
            state = STATE_NEW_WORD
        else:
            state = STATE_END_LINE

# End Line State =============================================================
    if state == STATE_END_LINE:
        if m['instruction']:
            print('END INSTRUCTION')
            if m['arguments'] != m['no_arguments']:
                sys.exit('Line {}: Invalid Number of arguments'.format(m['line'], repr(c)))

            print('    Register Value:', m['register_value'] & 1, end='')
            print((m['register_value'] >> 1) & 1, end='')
            print((m['register_value'] >> 2) & 1)

            print('    Indireciton Offset:', m['indirection_offset'])

            op = m[m['inst_start']]
            full_op = op << 2
            value = m['register_value']
            if not m['indirection_offset']:
                value = value >> 1
            value = value & 3
            print('    Registers Arguments:', bin(value))
            print('    OP:', bin(op))
            full_op = full_op | value

            print('    Put {} at {}'.format(bin(full_op), m['inst_start']))
            m[m['inst_start']] = full_op

            m['instruction'] = False
            m['arguments'] = 0
        state = STATE_NEW_WORD

        if c == '\0':
            running = False

# Add character to current word ==============================================
    if m['add_to_word']:
        if m['word'] == m['MAX_WORD_SIZE']:
            sys.exit('Line {}: Word is too big'.format(m['line']))
        m['word'] += 1
        m[m.l('word') + m['word']] = c

#  Exit loop
    if not running:
        break

if verbose:
    print('===============================================================================\n')
    print('Image:')

current_chunk = m['image_head']
image_array = m.edge
while True:
    size = m[current_chunk + 1]
    for i in range(0, size):
        m[m.edge] = m[current_chunk + 2 + i]
        m.edge += 1
    if current_chunk == m['image_tail']:
        break
    else:
        current_chunk = m[current_chunk]

insert_head = m['insert_head']
insert_tail = m['insert_tail']
label_head = m['label_head']
label_tail = m['label_tail']
if not (insert_head == insert_tail == 0):
    current_insert = insert_head
    while True: # Iterate Label Inserts
        current_label = label_head
        size = m[current_label + 2]
        match = False
        while True: # Iterate Labels Defs
            index = 0
            location = m[current_label + 1]
            while True: # Iterate Characters
                label_char = m[current_label + 2 + index]
                insert_char = m[current_insert + 2 + index]
                if insert_char != label_char: # Failure on this label
                    break
                index += 1
                if index > size: # Success on this label
                    if verbose:
                        print('Insert {} @ {}'.format(location, m[current_insert + 1]))
                    m[image_array + m[current_insert + 1]] = location
                    match = True
                    break
            if current_insert == insert_tail:
                if not match:
                    sys.exit('Line {}: Label "{}" has no definition',
                        m['line'],
                        m.get_string(m[current_insert + 2])
                    )
                break
            else:
                current_insert = m[current_insert]
        if current_label == label_tail:
            break
        else:
            current_label = m[current_label]
if verbose:
    m.print()
    print('Final Image ===================================')

with binary.open('bw') as f:
    i = 0
    size = m['BINARY_MAGIC_NUMBER'] - 1
    while True:
        value = m[m.l('BINARY_MAGIC_NUMBER') + 1 + i]
        if verbose:
            print(repr(value))
        if isinstance(value, str):
            value = ord(value)
        f.write(bytes([value]))
        i += 1
        if i > size:
            break

    i = 0
    size = m['image_size'] - 1
    while True:
        value = m[image_array + i]
        if verbose:
            print(repr(value))
        if isinstance(value, str):
            value = ord(value)
        f.write(bytes([value, 0]))
        i += 1
        if i > size:
            break

