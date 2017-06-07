# Filesystem Prototype v1
from array import array
from enum import IntFlag

class Disk:
    def __init__(self, size):
        self.size = size
        self.data = array('L', (0,) * self.size)

    def insert(self, place, item, fixed = False, max_size = None):
        if fixed:
            if max_size is None:
                raise ValueError(
                    'max_size must be supplied if fixed is set to true'
                )

        written = 0

        if isinstance(item, int):
            self.data[place] = item
            written = 1

        elif isinstance(item, tuple):
            for index, subitem in enumerate(item):
                written += self.insert(place + index, subitem)

        elif isinstance(item, list): # Same as tuple except include size
            self.data[place] = len(item)
            written = 1
            place += 1
            for index, subitem in enumerate(item):
                written += self.insert(place + index, subitem)

        elif isinstance(item, str): # Same as list except convert characters
            self.data[place] = len(item)
            written = 1
            place += 1
            for index, subitem in enumerate(item):
                written += self.insert(place + index, ord(subitem))

        if max_size is not None and written > max_size:
            raise ValueError('Size inserted is greater than max size')

        if fixed:
            return max_size
        else:
            return written

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def get_string(self, place):
        size = self.data[place]
        s = ""
        for i in range(place + 1, place + 1 + size):
            s += chr(self.data[i])
        return s

# Node Types
class Node_Type(IntFlag):
    NONE = 0
    ROOT = 1
    FILE = 2
    SUBDIRECTORY = 4
    DIRECTORY = ROOT | SUBDIRECTORY
    ENTRY = FILE | SUBDIRECTORY
    LIST = ROOT | ENTRY
    DATA = 8
    VALID = LIST | DATA

# Node Offsets
class Node_Offset(IntFlag):
    TYPE = 0
    SIZE = 1

    # Data Node Offsets
    NEXT = 2

    # List (Root, Subdirectory and File) Node Offsets
    HEAD = 2
    TAIL = 3

    # Entry Node Offsets
    PARENT = 4
    SIBLING = 5
    NAME = 6

class Node:
    ROOT_SIZE = 4
    NAME_MAX_SIZE = 16
    ENTRY_SIZE = 7 + NAME_MAX_SIZE
    DATA_SIZE = 3

    def __init__(self, fs, **kw):
        '''If location is set, Node is loaded from fs.disk, expecting any
        valid node if note_type isn't set or that type if it is set.
        If location isn't set a new Node structure will be created.
        '''
        self.fs = fs

        # Process kwargs
        node_type = None
        location = None
        for k, v in kw.items():
            if k == 'node_type':
                node_type = v
            elif k == 'location':
                location = v
        
        if node_type is None:
            if location is None:
                raise ValueError('node_type AND location can not be None')
            node_type = Node_Type.VALID

        if location is not None:
            loaded_node_type = Node_Type(fs.disk[location])
            if not node_type & loaded_node_type:
                raise ValueError(
                    'Expected Node Type: "{}", got Node Type: "{}"'.format(
                        node_type, loaded_node_type
                    )
                )
            node_type = loaded_node_type

        struct_size = 0
        if node_type == Node_Type.ROOT:
            struct_size = self.ROOT_SIZE
        elif node_type & Node_Type.ENTRY:
            struct_size = self.ENTRY_SIZE
        elif node_type == Node_Type.DATA:
            struct_size = self.DATA_SIZE
        else:
            raise ValueError('Invalid Node Type: {}', node_type)

        self.struct_size = struct_size
        struct = [0] * struct_size
        struct[Node_Offset.TYPE] = node_type
        self.type = Node_Type(node_type)

        # Load rest of the node from disk if applicable
        if location is not None:
            for i in range(1, struct_size):
                struct[i] = fs.disk[location + i]

        self.location = location
        self.struct = struct

    @classmethod
    def root(cls, fs):
        return cls(fs, location = fs.ROOT, node_type = Node_Type.ROOT)

    def assert_type(self, node_type, message):
        if not self.type & node_type:
            raise ValueError(
                'Node must have type "{}", not "{}": {}'.format(
                    Node_Type.DATA,
                    self.type,
                    message,
                )
            )

# SIZE

    def size(self, value = None):
        if value is None:
            return self.struct[Node_Offset.SIZE]
        self.struct[Node_Offset.SIZE] = value

# NEXT

    def next_value(self, value = None):
        self.assert_type(Node_Type.DATA, "Next is only part of Data Nodes")
        if value is None:
            return self.struct[Node_Offset.NEXT]
        self.struct[Node_Offset.NEXT] = value

    def next(self, value = None):
        if value is None:
            return self.__class__(
                self.fs,
                location = self.next_value(),
                node_type = Node_Type.DATA,
            )
        value.assert_type(Node_Type.DATA,
            "Next value can only be another Data Node"
        )
        self.next_value(value.location)

# HEAD
    def head_value(self, value = None):
        self.assert_type(Node_Type.LIST, "Head is only part of List Nodes")
        if value is None:
            return self.struct[Node_Offset.HEAD]
        self.struct[Node_Offset.HEAD] = value

    def head(self, value = None):
        if value is None:
            return self.__class__(
                self.fs,
                location = self.head_value(),
                node_type = Node_Type.ENTRY,
            )
        value.assert_type(Node_Type.ENTRY,
            "The value of Head can only be a Entry Node"
        )
        self.head_value(value.location)

# TAIL
    def tail_value(self, value = None):
        self.assert_type(Node_Type.LIST, "Tail is only part of List Nodes")
        if value is None:
            return self.struct[Node_Offset.TAIL]
        self.struct[Node_Offset.TAIL] = value

    def tail(self, value = None):
        if value is None:
            return self.__class__(
                self.fs,
                location = self.tail_value(),
                node_type = Node_Type.ENTRY,
            )
        value.assert_type(Node_Type.ENTRY,
            "The value of tail can only be a Entry Node"
        )
        self.tail_value(value.location)

# PARENT
    def parent_value(self, value = None):
        self.assert_type(Node_Type.ENTRY, "Parent is only part of Entry Nodes")
        if value is None:
            return self.struct[Node_Offset.PARENT]
        self.struct[Node_Offset.PARENT] = value

    def parent(self, value = None):
        if value is None:
            return self.__class__(
                self.fs,
                location = self.parent_value(),
                node_type = Node_Type.DIRECTORY,
            )
        value.assert_type(Node_Type.DIRECTORY,
            "Parents must be Directory Nodes"
        )
        self.parent_value(value.location)

# SIBLING
    def sibling_value(self, value = None):
        self.assert_type(Node_Type.ENTRY, "Sibling is only part of Entry Nodes")
        if value is None:
            return self.struct[Node_Offset.SIBLING]
        self.struct[Node_Offset.SIBLING] = value

    def sibling(self, value = None):
        if value is None:
            return self.__class__(
                self.fs,
                location = self.sibling_value(),
                node_type = Node_Type.ENTRY,
            )
        value.assert_type(Node_Type.ENTRY,
            "Siblings must be other Entry Nodes"
        )
        self.sibling_value(value.location)

# NAME
    def name(self, value = None):
        self.assert_type(Node_Type.ENTRY, "Only Entry Nodes have names")
        if value is None:
            size = self.struct[Node_Offset.NAME]
            s = ""
            for i in range(1, size + 1):
                s += self.struct[Node_Offset.NAME + i]
            return s
        size = len(value)
        if size > self.NAME_MAX_SIZE:
            raise ValueError('Name too Big!')
        self.struct[Node_Offset.NAME] = size
        for i in range(0, size):
            self.struct[Node_Offset.NAME + 1 + i] = value[i]

    def is_a(self, node_type):
        return self.type & node_type

    def __eq__(self, other):
        if self.location is None:
            return False
        return self.location == other.location

    def write_to_disk(self, location = None):
        if location is None:
            if self.location is None:
                raise ValueError(
                    'Can\'t write Node to disk without a location'
                )
            location = self.location
        else:
            self.location = location

        for i in range(0, self.struct_size):
            self.fs.disk[location + i] = self.struct[i]

    def insert_entry(self, entry):
        entry.parent(self)
        size = self.size() 
        if size:
            entry.sibling(self.head())
        else:
            self.tail(entry)
        self.head(entry)
        self.size(size + 1)
        self.write_to_disk()
        entry.write_to_disk()

    def remove_entry(self, entry):
        pass

    def get_entries(self):
        rv = []
        size = self.size()
        if size:
            node = head = self.head()
            tail = self.tail()
            while True:
                rv.append(node)
                if node == tail:
                    break
                node = node.sibling()
        return rv

    def __str__(self):
        s = '<'
        if self.is_a(Node_Type.VALID):
            if self.is_a(Node_Type.ENTRY):
                s += '"' + self.name() + '"'
            s += self.type.name + ' size: ' + str(self.size())
        else:
            s += 'INVALID NODE'
        if self.location is not None:
            s += ' @ ' + str(location)
        return s + '>'

    def __repr__(self):
        return str(self)

class Filesystem:
    HEADER_SIZE = 7 # EXCLUDING BLOCK ALLOCATION WORDS
    ROOT = 3

    def __init__(self, disk, block_size = 2**6, word_size = 16):
        self.disk = disk
        self.size = disk.size
        self.word_size = word_size
        self.block_size = block_size
        self.size_in_blocks = disk.size // block_size
        self.size = disk.size - disk.size % block_size
        self.entries_per_block = block_size // Node.ENTRY_SIZE
        self.block_allocation_words = self.size_in_blocks // self.word_size + 1
        self.header_size = self.HEADER_SIZE + 2 * self.block_allocation_words

        if self.header_size > block_size:
            raise ValueError(
                'Blocks are too small ({}) to hold Filesystem Header '\
                '({})'.format(
                    block_size, self.header_size
                )
            )

        if Node.ENTRY_SIZE > block_size:
            raise ValueError(
                'Blocks are too small ({}) to hold entry node '\
                '({})'.format(
                    block_size, Node.ENTRY_SIZE
                )
            )

    def get_block(self, block):
        return self.block_size * block

    def block_location(self, location):
        return location - location % self.block_size

    def block_allocated(self, block, mark = None):
        location = self.HEADER_SIZE
        if not 0 <= block < self.size_in_blocks:
            raise ValueError('Invalid Block')
        word_location = location + block // self.word_size
        word = self.disk.data[word_location]
        mask = 1 << (block % self.block_size)
        if mark is None:
            return bool(mask & word)
        if mark:
            self.disk.data[word_location] = mask | word
        else:
            self.disk.data[word_location] = mask ^ word

    def format(self):
        self.disk.insert(0, (
        # Disk Header
            self.size,
            self.block_size,
            self.size_in_blocks,
            1, # Type Root
            0, # Number of child entries
            0, # Head Child Entry Node Pointer
            0, # Tail Child Entry Node Pointer
            # Block Allocation
            (0,) * (self.block_allocation_words),
        ))
        self.block_allocated(0, True)

    def allocate_block(self):
        for i in range(1, self.size_in_blocks):
            if not self.block_allocated(i):
                print('BLOCK:', i)
                # Reserve Bloack and get location
                self.block_allocated(i, True)
                block = self.get_block(i) 

                return block
        raise ValueError('No Room')

    def make_entry(self, parent, node_type, name):
        parent.assert_type(Node_Type.DIRECTORY,
            "Parents must be a Directory Node"
        )
        entry = Node(self, node_type = node_type)
        entry.assert_type(Node_Type.ENTRY,
            "Entry Node are the only thing that can be inserted into"\
            "Directories"
        )
        entry.location = self.allocate_block()
        parent.insert_entry(entry)

        return entry

    def resolve_path(self, path):
        '''Returns a list and a Node.
        If list is empty, the node is the path fully resolved,
        otherwise its the first parent in the path that exists,
        and the list is the list of items left in the path.
        '''
        if len(path) == 0 or path[0] != '/':
            raise ValueError('Invalid Path')
        path = path[1:]
        if len(path) > 1 and path[-1] == '/':
            path = path[:-1]
        path_list = path.split('/')

        node = Node.root(self)
        no_items = len(path)
        if no_items == 0: # Root
            return [], node
        for index, item in enumerate(path_list):
            found = False
            for entry in node.get_entries():
                if item == entry.name():
                    node = entry
                    found = True
                    break
            if not found:
                return path_list[-no_items-index:], node
        return [], node

    def make_directory(self, path, parents = False):
        leftovers, node = self.resolve_path(path)
        if leftovers:
            if parents:
                while len(leftovers) > 0:
                    self.make_entry(node, Node_Type.SUBDIRECTORY, leftovers[0])
                    leftovers, node = self.resolve_path(path)
            elif len(leftovers) == 1:
                self.make_entry(node, Node_Type.SUBDIRECTORY, leftovers[0])
            else:
                raise ValueError('Parent doesnt exist')
        else:
            if node.type == Node_Type.FILE:
                raise ValueError('Directory already exists: ' + path)
            elif node.type == Node_Type.SUBDIRECTORY:
                raise ValueError('Directory already exists: ' + path)
            raise ValueError('Invalid Node Type: ' + str(node))

    def list(self, path):
        leftover, node = self.resolve_path(path)
        if leftover:
            raise ValueError('Coundn\'t find: ' + path)
        return node.get_entries()

d = Disk(2**8)
fs = Filesystem(d)
fs.format()
#fs.make_directory("/directory/")
