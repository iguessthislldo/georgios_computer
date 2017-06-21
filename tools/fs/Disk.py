from array import array

from prefix_string import prefix_string

class Disk:
    ARRAY_DATA_TYPE = 'H'

    def __init__(self, size):
        self.size = size
        self.data = array(self.ARRAY_DATA_TYPE, (0,) * self.size)

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

        elif isinstance(item, str):
            kw = {}
            if fixed:
                kw['fixed_size'] = max_size
            written = prefix_string(self.data, place, item, **kw)

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

    def load(self, filename):
        with open(filename, 'rb') as f:
            self.data = array(self.ARRAY_DATA_TYPE)
            self.data.fromfile(f, self.size)

    def save(self, filename):
        with open(filename, 'wb') as f:
            self.data.tofile(f)

