# Allocate Memory Prototype 2

# end
# 
# block:
#     free
#     next
#     prev

class Memory:
    def __init__(self, size, allocation_start):
        self.size = size
        self.array = [None] * size
        self.start = allocation_start
        self.end = allocation_start

    def allocate(self, ammount):
        block = self.start
        prev = 0

        if not ammount:
            return True, 0

        while True:
            end = block + 3 + ammount
            if end > self.size:
                return True, 0
            elif block == self.end: # Make new block
                self.end = end
                self.array[block + 1] = self.end
                self.array[block + 2] = prev
                break
            elif self.array[block] and (self.array[block + 1] - block) >= (ammount + 3): # Block is free
                break
            else:
                prev = block
                block = self.array[block + 1]
                continue
                
        self.array[block] = 0 # Mark as not free / taken / allocated

        return False, block + 3

    def put(self, value, number):
        error, location = self.allocate(number)
        if error:
            print('No Room')
            return

        for i in range(0, number):
            self.array[location + i] = value

        return location

    def free(self, location):
        # A is the previous block
        # B is the block at the given location
        # C is the next block
        # D is the block after C

        block = B = location - 3

        if self.array[block] or block >= self.end: # Block is already free
            return True

        self.array[B] = 1

        # Look at the previous block
        A = self.array[B + 2]
        if B != self.start and self.array[A]:
            block = A

        # Look at the next block
        C = self.array[B + 1]
        if C == self.end:
            self.end = block
            return False
        next = C
        if self.array[C]:
            # Look at the block after C
            next = D = self.array[C + 1]
            if D != self.end:
                self.array[D + 2] = block
        else:
            self.array[C + 2] = block

        self.array[block + 1] = next

        return False

    def __repr__(self):
        rv = ''
        l = 0
        for i in range(0, self.size):
            if l == 0:
                rv += '{:>3}:    '.format(i)

            rv += '{:<10}'.format(repr(self.array[i]))

            if l == 0:
                rv += '\n'
                l = 0
            else:
                rv += '    '
                l = l + 1
                
        if rv[-1] != '\n':
            rv += '\n'

        return rv

    def __getitem__(self, key):
        return self.array[key]

    def __setitem__(self, key, value):
        self.array[key] = value

