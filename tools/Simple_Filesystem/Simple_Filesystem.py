from Disk import Disk
from prefix_string import prefix_string

'''
Structures:

Master Block:
    MAGIC_NUMBER
    VERSION
    size
    block_size
    size_in_blocks
    block_allocation
    file_table_max
    file_table_size
    file_table

File Table Entry:
    Allocated
    Head Block
    Tail Block
    Size of File
    Prefixed String of Name

Data Block:
    Next
    Size
    [Data ...]
'''

class Simple_Filesystem:
    MAGIC_NUMBER = 'georgios;filesytem;;\n'
    VERSION = 1

    def __init__(self, disk, name_size = 32, table_size = 1, block_size = 2**10, word_size = 16):
        self.disk = disk
        self.size = disk.size
        self.word_size = word_size
        self.block_size = block_size

        self.size_in_blocks = disk.size // block_size
        self.size = disk.size - disk.size % block_size
        self.block_allocation_words = self.size_in_blocks // self.word_size + 1
        self.name_size = name_size
        self.file_row_size = 5 + name_size
        self.file_table_max = (self.block_size - len(self.MAGIC_NUMBER) - 7) // (5 + self.name_size)

        magic_len = len(self.MAGIC_NUMBER)
        self.offsets = dict(
            magic_number = 0,
            version = magic_len,
            size = magic_len + 1,
            block_size = magic_len + 2,
            size_in_blocks = magic_len + 3,
            block_allocation = magic_len + 4,
            file_table_max = magic_len + 4 + self.block_allocation_words,
            file_table_size = magic_len + 4 + self.block_allocation_words + 1,
            file_table = magic_len + 4 + self.block_allocation_words + 2,
            file_allocated = 0,
            file_head = 1,
            file_tail = 2,
            file_size = 3,
            file_name = 4
        )

    def format(self):
        # Basic Values =======================================================

        # Magic Number
        self.disk.insert(self.offsets['magic_number'], self.MAGIC_NUMBER,
            fixed=True, max_size=len(self.MAGIC_NUMBER)
        )

        # Version
        self.disk.insert(self.offsets['version'], self.VERSION)

        # Size
        self.disk.insert(self.offsets['size'], self.size)

        # Block Size
        self.disk.insert(self.offsets['block_size'], self.block_size)

        # Number of Blocks
        self.disk.insert(self.offsets['size_in_blocks'], self.size_in_blocks)

        # Block Allocation
        self.disk.insert(self.offsets['block_allocation'],
            (0,) * (self.block_allocation_words)
        )

        # File Table
        self.disk.insert(
            self.offsets['file_table_max'], self.file_table_max
        )
        self.disk.insert(self.offsets['file_table_size'], 0)

        # Allocate Master Block
        self.block_allocated(0, True)

        for i in range(0, self.file_table_max):
            location = self.offsets['file_table'] + i * self.file_row_size
            self.disk[location] = 0

    def get_block(self, block):
        return self.block_size * block

    def start_of_block(self, location):
        return location - location % self.block_size

    def block_allocated(self, block, mark = None):
        location = self.offsets['block_allocation']
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

# FILE OPERATIONS ============================================================

    def get_free_table_entry(self):
        file_entries = self.file_table_max
        file_table = self.offsets['file_table']
        for i in range(0, file_entries):
            location = file_table + i * self.file_row_size
            if not self.disk[location]:
                return location
        return None

    def valid_file_entry(self, entry):
        file_entries = self.file_table_max
        file_table = self.offsets['file_table']
        if entry < file_table or entry >= file_table + file_entries * self.file_table_max:
            return False
        if (entry - file_table) % self.file_row_size:
            return False
        return bool(self.disk[entry])

    def get_files(self):
        number_of_files = self.disk[self.offsets['file_table_size']]
        file_entries = self.file_table_max
        file_table = self.offsets['file_table']
        r = {}
        for i in range(0, file_entries):
            location = file_table + i * self.file_row_size
            if self.disk[location]:
                r[prefix_string(self.disk, location + self.offsets['file_name'])] = location
        return number_of_files, r

    def _set_file_name(self, file_entry, name):
        prefix_string(self.disk, file_entry + self.offsets['file_name'], name)

    def rename_file(self, file_entry, name):
        if not self.valid_file_entry(file_entry):
            raise ValueError("Invalid File Entry Pointer")
        no_files, files = self.get_files()
        if name in files:
            raise ValueError('File %s alreay exists' % repr(name))
        self._set_file_name(file_entry, name)

    def create_file(self, name):
        no_files, files = self.get_files()
        if name in files:
            raise ValueError('File alreay exists')
        max_files = self.file_table_max
        if no_files == max_files:
            raise ValueError('File table is full: %d out of %d' % (no_files, max_files))
        if len(name) > self.name_size:
            raise ValueError('File name is longer than max file name size')
        self.disk[self.offsets['file_table_size']] = no_files + 1
        row = self.get_free_table_entry()
        self.disk[row+self.offsets['file_allocated']] = 123
        self.disk[row+self.offsets['file_head']] = 0
        self.disk[row+self.offsets['file_tail']] = 0
        self.disk[row+self.offsets['file_size']] = 0
        self._set_file_name(row, name)
        return row

    def delete_file_data(self, file_entry):
        if not self.valid_file_entry(file_entry):
            raise ValueError("Invalid File Entry Pointer")
        file_size = self.disk[file_entry + self.offsets['file_size']]
        if file_size == 0:
            return
        head = self.disk[file_entry + self.offsets['file_head']]
        tail = self.disk[file_entry + self.offsets['file_tail']]
        while True:
            self.block_allocated(head // self.block_size, False)
            if head == tail:
                break
            head = self.disk[head]

    def delete_file(self, file_entry):
        self.delete_file_data(file_entry) # Delete Data
        self.disk[file_entry] = 0 # Deallocate File Entry
        self.disk[self.offsets['file_table_size']] -= 1 # Decrment File Count

    def read_from_file(self, file_entry):
        if not self.valid_file_entry(file_entry):
            raise ValueError("Invalid File Entry Pointer")

        data = []
        file_size = self.disk[file_entry + self.offsets['file_size']]

        if file_size > 0:
            current = head = self.disk[file_entry + self.offsets['file_head']]
            tail = self.disk[file_entry + self.offsets['file_tail']]
            while True:
                current_size = self.disk[current + 1]
                for i in range(0, current_size):
                    data.append(self.disk[current + 2 + i])
                if current == tail:
                    break
                current = self.disk[current]

        return data

    def append_to_file(self, file_entry, data):
        if not self.valid_file_entry(file_entry):
            raise ValueError("Invalid File Entry Pointer")

        size = len(data)
        if size == 0:
            return
        file_size = self.disk[file_entry + self.offsets['file_size']]
        head = tail = None
        tail_size = 0
        if file_size == 0:
            head = tail = self.allocate_block()
        else:
            head = self.disk[file_entry + self.offsets['file_head']]
            tail = self.disk[file_entry + self.offsets['file_tail']]
            tail_size = self.disk[tail + 1]

        for i in range(0, size):
            if tail_size == self.block_size - 2:
                new_tail = self.allocate_block()
                self.disk[tail] = new_tail
                self.disk[tail + 1] = tail_size
                tail = new_tail
                tail_size = 0
            self.disk[tail + 2 + tail_size] = data[i]
            tail_size += 1
        self.disk[tail + 1] = tail_size

        self.disk[file_entry + self.offsets['file_size']] = file_size + size
        self.disk[file_entry + self.offsets['file_head']] = head
        self.disk[file_entry + self.offsets['file_tail']] = tail

    def write_to_file(self, file_entry, data):
        self.delete_file_data(file_entry)
        self.append_to_file(file_entry, data)
