from enum import IntFlag

from Disk import Disk
from prefix_string import prefix_string

class Node_Error(Exception):
    '''Rasied when an invalid value has been passed to this module
    or when values on disk are invalid.
    '''

class Node_Type(IntFlag):
    NONE = 0
    ROOT = 1
    FILE = 2
    SUBDIRECTORY = 4
    DIRECTORY = ROOT | SUBDIRECTORY # 5
    ENTRY = FILE | SUBDIRECTORY # 6
    LIST = ROOT | ENTRY # 7
    DATA = 8
    ELEMENT = ENTRY | DATA # 14
    VALID = LIST | DATA # 15

class Node_Offset(IntFlag):
    '''Offset of items in Node.struct
    '''
    # Basic Values
    TYPE = 0
    SIZE = 1

    # Data Node
    NEXT = 2

    # List (Root, Subdirectory and File) Node
    HEAD = 2
    TAIL = 3

    # Entry Node
    PARENT = 4
    SIBLING = 5
    NAME = 6

class Node_Context:
    def __init__(self, disk, max_node_size):
        if not isinstance(disk, Disk):
            raise TypeError((
                    'Must pass Disk to Node, not: {} which is type: {}'
                ).format(
                    repr(disk),
                    repr(disk.__class__),
                )
            )
        self.disk = disk
        self.max_node_size = max_node_size

class Node:
    '''Central Class for this module
    '''
    TYPE = Node_Type.NONE
    TYPE_SIZE = None

    def __init__(self, ctx, location = None, size = 0):
        self.ctx = ctx
        self.disk = ctx.disk
        self.location = location
        self.struct = [0] * self.TYPE_SIZE
        self.struct[Node_Offset.TYPE] = int(self.TYPE)
        self.size(size)

    @staticmethod
    def assert_type(expecting, got, message):
        if not expecting & got:
            raise TypeError((
                    'Expecting type: {}, got type: {}: {}',
                ).format(
                    Node_Type(expecting),
                    Node_Type(got),
                    message,
                )
            )

    def size(self, value = None):
        if value is None:
            return self.struct[Node_Offset.SIZE]
        self.struct[Node_Offset.SIZE] = value

    def load(self, location = None):
        if location is None:
            if self.location is None:
                raise Node_Error(
                    'Node.load() must have a location to load from! '\
                    'Node.location and location arguemnt are both missing.'
                )
            location = self.location

        for i in range(0, self.TYPE_SIZE):
            self.struct[i] = self.disk[location + i]

        if self.struct[Node_Offset.TYPE] != self.TYPE:
            raise Node_Error((
                    'Tried to load Node of type: {} at {}, Type ID: {}, '\
                    'was expecting: {}'
                ).format(
                    repr(self.__class__),
                    location,
                    struct[Node_Offset.TYPE],
                    self.TYPE,
                )
            )

    @classmethod
    def from_disk(cls, ctx, location):
        node = cls(ctx, location = location)
        node.load()
        return node

    def save(self, location = None):
        if location is None:
            if self.location is None:
                raise Node_Error(
                    'Node.save() must have a location to save to! '\
                    'Node.location and location arguemnt are both missing.'
                )
            location = self.location

        for i in range(0, self.TYPE_SIZE):
            self.disk[location + i] = self.struct[i]

    def __eq__(self, other):
        if self.location is None:
            return False
        return self.location == other.location

    def __int__(self):
        return self.location

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '<{} size={}>'.format(
            self.__class__.__name__, self.size()
        )
        
class List_Node(Node):
    TYPE = Node_Type.LIST
    TYPE_SIZE = 4
    ELEMENT_TYPE = Node_Type

    def __init__(self, ctx, location = None, size = 0, head = 0, tail = 0):
        super().__init__(ctx, location, size)
        self.head_value(head)
        self.tail_value(tail)

    def process_list_value(self, value):
        raise Node_Error('Should not be using List_Node')

    def head_value(self, value = None):
        if value is None:
            if not self.size():
                raise Node_Error('Head is invalid if size is zero')
            return self.struct[Node_Offset.HEAD]
        self.struct[Node_Offset.HEAD] = int(value)

    def tail_value(self, value = None):
        if value is None:
            if not self.size():
                raise Node_Error('Tail is invalid if size is zero')
            return self.struct[Node_Offset.TAIL]
        self.struct[Node_Offset.TAIL] = int(value)

    def iterator(self):
        if self.size():
            node_value = self.head_value()
            while True:
                node = self.process_list_value(node_value)
                yield node
                if node_value == self.tail_value():
                    break
                node_value = node.next_value()

    def __iter__(self):
        return self.iterator()

class Directory_Node(List_Node):
    TYPE = Node_Type.DIRECTORY

    def process_list_value(self, value):
        node_type = self.disk[int(value) + Node_Offset.TYPE]
        if node_type == Node_Type.SUBDIRECTORY:
            cls = Subdirectory_Node
        elif node_type == Node_Type.FILE:
            cls = File_Node
        else:
            raise Node_Error('Invalid attempt to read directory contents')

        return cls.from_disk(self.ctx, value)

    def __getitem__(self, key):
        for entry in self:
            if entry.name() == key:
                return entry
        raise KeyError(
            'Entry with name "{}" not in directory "{}"'.format(
                key, self.name()
            )
        )

    def add_entry(self, entry):
        if not isinstance(entry, Entry_Node):
            raise Node_Error(
                'Can only add Entry Nodes to Directory Nodes'
            )
        print('Added Entry: {} to {}'.format(entry, self))
        if self.size():
            print('Not new, set next entry')
            entry.next_value(self.head_value())
        else:
            print('Empty, setting tail value')
            self.tail_value(entry)
        self.head_value(entry)
        self.size(self.size() + 1)

    def __contains__(self, item):
        if isinstance(item, str):
            try:
                e = self[item]
                return True
            except KeyError:
                return False
        raise TypeError('contains only supports strings')

    def __str__(self):
        return (
            '<Directory name="{}" size={}>'
        ).format(self.name(), self.size())
    
class Root_Node(Directory_Node):
    TYPE = Node_Type.ROOT

    def name(self, value = None):
        if value is None:
            return "/"
        # For now just ignore attempts to rename root

class Entry_Node(List_Node):
    TYPE = Node_Type.ENTRY
    NAME_MAX_SIZE = 16
    TYPE_SIZE = 7 + NAME_MAX_SIZE

    def __init__(
        self, ctx, name = None, location = None, size = 0,
        head = 0, tail = 0, parent = 0, sibling = 0
    ):
        super().__init__(ctx, location, size, head, tail)
        if name is not None:
            self.name(name)
        self.parent_value(parent)
        self.next_value(sibling)

    def parent_value(self, value = None):
        if value is None:
            return self.struct[Node_Offset.PARENT]
        self.struct[Node_Offset.PARENT] = int(value)

    def next_value(self, value = None):
        if value is None:
            return self.struct[Node_Offset.SIBLING]
        self.struct[Node_Offset.SIBLING] = int(value)

    def name(self, value = None):
        if value is None:
            return prefix_string(
                self.struct, Node_Offset.NAME
            )
        if len(value) == 0:
            raise ValueError('Entry_Node can\'t have an empty name')
        prefix_string(
            self.struct, Node_Offset.NAME, value
        )

class Subdirectory_Node(Entry_Node, Directory_Node):
    TYPE = Node_Type.SUBDIRECTORY

class File_Node(Entry_Node):
    TYPE = Node_Type.FILE

    def process_list_value(self, value):
        node_type = self.disk[Node_Offset.TYPE]
        if node_type != Node_Type.DATA:
            raise Node_Error('Invalid attempt to read file contents')

        return Data_Node.from_disk(self.ctx, value)

    def tail_size(self):
        if size:
            tail = Data_Node.from_disk(self.ctx, self.tail_value())
            return tail.size()
        return 0

    def __str__(self):
        return '<File name="{}" size={}>'.format(self.name(), self.size())

class Data_Node(Node):
    TYPE = Node_Type.DATA
    TYPE_SIZE = 3

    def __init__(self, ctx, location = None, size = 0, next = 0):
        super().__init__(ctx, location, size)
        self.next_value(next)

    def next_value(self, value = None):
        if value is None:
            return self.struct[Node_Offset.NEXT]
        self.struct[Node_Offset.NEXT] = int(value)

