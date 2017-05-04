def make_memory(size):
    return dict(
        size = size,
        array = [0]*size,
        point = 0,
    )

def allocate(memory, ammount):
    new = memory['point'] + ammount
    if new > memory['size']:
        return True, memory, 0
    else:
        location = memory['point']
        memory['point'] = new
        return False, memory, location

def put(memory, size, value):
    error, memory, location = allocate(memory, size)
    if error:
        print('Out of Room')
        return memory

    for i in range(location, location+size):
        memory['array'][i] = value

    return memory

memory = make_memory(32)
print(memory['array'])
put(memory, 14, 1)
print(memory['array'])
put(memory, 8, 2)
print(memory['array'])
put(memory, 9, 3)
print(memory['array'])
put(memory, 5, 4) # Out of Room
print(memory['array'])
