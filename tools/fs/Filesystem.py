from Disk import Disk
from nodes import *

class Filesystem:
    VERSION = 1
    MAGIC_NUMBER = 'georgios;filesytem;;\n'

    def __init__(self, disk, block_size = 2**7, word_size = 16):
        self.disk = disk
        self.size = disk.size
        self.word_size = word_size
        self.block_size = block_size

        self.size_in_blocks = disk.size // block_size
        self.size = disk.size - disk.size % block_size
        self.block_allocation_words = self.size_in_blocks // self.word_size + 1

        self.node_context = Node_Context(disk, block_size)

        # These are set on format or load
        self.header_size = None
        self.header_table = None
        self.root = None

    def format(self):
        ''' Write new filesytem to disk by creating a new master block.
        This will also reset the Filesystem instance and probably invalidate
        any external references to the contents.
        '''
        l = 0
        self.header_table = {}

        # Magic Number
        self.header_table['MAGIC_NUMBER'] = l
        l += self.disk.insert(l, self.MAGIC_NUMBER,
            fixed=True, max_size=len(self.MAGIC_NUMBER)
        )

        # Version
        self.header_table['VERSION'] = l
        l += self.disk.insert(l, self.VERSION)

        # Size
        self.header_table['size'] = l
        l += self.disk.insert(l, self.size)

        # Block Size
        self.header_table['block_size'] = l
        l += self.disk.insert(l, self.block_size)

        # Number of Blocks
        self.header_table['size_in_blocks'] = l
        l += self.disk.insert(l, self.size_in_blocks)

        # Block Allocation
        self.header_table['block_allocation'] = l
        l += self.disk.insert(l,
            (0,) * (self.block_allocation_words)
        )

        # Root Node
        self.root = Root_Node(self.node_context, l)
        self.root.save()
        self.header_size = l
        l += Root_Node.TYPE_SIZE

        self.header_size = l

        # Allocate Master Block
        self.block_allocated(0, True)

    def load(self):
        pass

    def get_block(self, block):
        return self.block_size * block

    def start_of_block(self, location):
        return location - location % self.block_size

    def block_allocated(self, block, mark = None):
        location = self.header_table['block_allocation']
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

    def allocate_block(self):
        for i in range(1, self.size_in_blocks):
            if not self.block_allocated(i):
                # Reserve Bloack and get location
                self.block_allocated(i, True)
                block = self.get_block(i) 
                return block
        raise ValueError('No Room')

    def resolve_path(self, path):
        elements = path.rstrip('/').lstrip('/').split('/')
        last = len(elements) - 1
        node = self.root
        if last == 0 and elements[0] == '':
            return node, True
        for index, element in enumerate(elements):
            if isinstance(node, Directory_Node):
                if element in node:
                    node = node[element]
                    if index == last:
                        return node, True
                    continue
                return node, False
            return node, index == last

    def new_directory_node(self, parent_node, name):
        c = self.root.ctx
        directory_node = Subdirectory_Node(c, name, self.allocate_block())
        parent_node.add_entry(directory_node)
        directory_node.save()
        parent_node.save()
        return directory_node

    def new_file_node(self, parent_node, name):
        c = self.root.ctx
        file_node = File_Node(c, name, self.allocate_block())
        parent_node.add_entry(file_node)
        file_node.save()
        parent_node.save()
        return file_node
