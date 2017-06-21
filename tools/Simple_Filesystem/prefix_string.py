def prefix_string(iterator, location, value = None, fixed_size = None):
    '''Using strings with the size as the first element, read or insert
    them as integers from or to an iterator starting at a location.
    '''

    # GET
    if value is None:
        if fixed_size is None:
            size = iterator[location]
            location += 1
        else:
            size = fixed_size

        return ''.join([
            chr(iterator[i]) for i in range(
                location, location + size
            )
        ])

    # SET
    size = None
    if fixed_size is None:
        size = len(value)
        iterator[location] = size
        location += 1
    else:
        size = fixed_size

    for i in range(0, size):
        iterator[location + i] = ord(value[i])

    return size
