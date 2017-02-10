import sys

def default_dict(dictionary, key, default):
    if key not in dictionary:
        dictionary.update({key: default})

def append_unqiue(alist, item):
    if item not in alist:
        alist.append(item)

outputs = {}
def add_outputs(*names):
    for name in names:
        outputs.update({ name: {
            'demux': []
        }})

inputs = {}
def add_inputs(*names):
    for name in names:
        inputs.update({ name: {
            'mux': []
        }})

arguments = [
    'I1',
    'I2',
    'I3',
]

add_outputs(
    'XO',
    'YO',
    'R',
    *arguments
)

add_inputs(
    'XE',
    'XS',
    'YE',
    'YS',
    'ZI',
    'ZE',
    'ZS',
    'A',
    'B',
)

instuctions = {
    'halt': {'code': 0, 'desc': 'Halt the computer'},

    'nop': {'code': 1, 'desc': 'Do nothing'},

    'set': {'code': 2, 'desc': 'Set a register to a value', 'args': [
        {'desc': 'Destination Register', 'dest': 'ZS'},
        {'desc': 'Value to use', 'dest': 'ZI'},
    ]},

    'copy': {'code': 3, 'desc': 'Copy a value from one register to another', 'args': [
        {'desc': 'Destination Register', 'dest': 'ZS'},
        {'desc': 'Source Register', 'dest': 'XS'},
    ], 'routes': [
        ('XO', 'ZI'),
    ]},

    'addr': {'code': 4, 'desc': (
        'Add the values of two registers'
    ), 'args': [
        {'desc': 'Destination Register', 'dest': 'ZS'},
        {'desc': 'Source Register A', 'dest': 'XS'},
        {'desc': 'Source Register B', 'dest': 'YS'},
    ], 'routes': [
        ('XO', 'A'),
        ('YO', 'B'),
        ('R', 'ZI'),
    ]},

    'addv': {'code': 5, 'desc': (
        'Add the values of a register and a constant value'
    ), 'args': [
        {'desc': 'Destination Register', 'dest': 'ZS'},
        {'desc': 'Source Register', 'dest': 'XS'},
        {'desc': 'Value to add', 'dest': 'B'},
    ], 'routes': [
        ('XO', 'A'),
        ('R', 'ZI'),
    ]},

    'subr': {'code': 6, 'desc': (
        'Subtract the values of two registers'
    ), 'args': [
        {'desc': 'Destination Register', 'dest': 'ZS'},
        {'desc': 'Source Register A', 'dest': 'XS'},
        {'desc': 'Source Register B', 'dest': 'YS'},
    ], 'routes': [
        ('XO', 'A'),
        ('YO', 'B'),
        ('R', 'ZI'),
    ]},

    'subv': {'code': 7, 'desc': (
        'Subtract the values of a register and a constant value'
    ), 'args': [
        {'desc': 'Destination Register', 'dest': 'ZS'},
        {'desc': 'Source Register', 'dest': 'XS'},
        {'desc': 'Value to subtract', 'dest': 'B'},
    ], 'routes': [
        ('XO', 'A'),
        ('R', 'ZI'),
    ]},
}

ordred = [None]*len(instuctions)
for k, v in instuctions.items():
    default_dict(v, 'args', [])
    default_dict(v, 'routes', [])

    index = v['code']
    if ordred[index] is not None:
        sys.exit('Two codes have the same value')
    
    ordred[index] = v

    for i, arg in enumerate(v['args']):
        append_unqiue(outputs[arguments[i]]['demux'], arg['dest'])
        append_unqiue(inputs[arg['dest']]['mux'], arguments[i])

    for route in v['routes']:
        append_unqiue(outputs[route[0]]['demux'], route[1])
        append_unqiue(inputs[route[1]]['mux'], route[0])

if len(sys.argv) > 1 and sys.argv[1] == "codes":
    instuction_strings = []
    max_col = [0]*7
    for k, v in instuctions.items():
        nargs = len(v['args'])
        append = [
            "{0:#x}".format(v['code'])[2:],
            "{0:#b}".format(v['code'])[2:],
            k,
            v['desc'],
            v['args'][0]['desc'] if nargs >= 1 else '*',
            v['args'][1]['desc'] if nargs >= 2 else '*',
            v['args'][2]['desc'] if nargs >= 3 else '*',
        ]
        for i, val in enumerate(max_col):
            max_col[i] = max(val, len(append[i]))
        instuction_strings.append(append)

    for line in instuction_strings:
        for i, val in enumerate(line):
            align = '>' if i < 2 else '<'
            print(('{:' + align + str(max_col[i] + 4) + '}').format(val), end='')
            if i < len(line)-1:
                print('|', end='')
        print('')
else:
    for k, v in outputs.items():
        print(k)
        for i in v['demux']:
            print('   ', i)
    for k, v in inputs.items():
        print(k)
        for i in v['mux']:
            print('   ', i)

