from allocate import Memory
m = Memory(100, 0)

# Chunk contists of size, next, followed by the elements

MAX_CHUNK_CAPACITY = 10
chunk_size = 0
no_chunks = 1
error, chunk_head = m.allocate(MAX_CHUNK_CAPACITY + 2)
current_chunk = chunk_head
if error:
    print('ERROR')
else:
    for i in range(0, 70):
        if chunk_size == MAX_CHUNK_CAPACITY:
            m[current_chunk] = chunk_size
            prev = current_chunk
            error, current_chunk = m.allocate(MAX_CHUNK_CAPACITY + 2)
            if error:
                print('ERROR')
                break
            m[prev + 1] = current_chunk
            chunk_size = 0
            no_chunks += 1
        m[current_chunk + 2 + chunk_size] = i
        chunk_size += 1
m[current_chunk] = chunk_size
m[current_chunk + 1] = 0

current_chunk = chunk_head
for i in range(0, no_chunks):
    no_elements = m[current_chunk]
    for i in range(0, no_elements):
        print(m[current_chunk + 2 + i])
    current_chunk = m[current_chunk + 1]
