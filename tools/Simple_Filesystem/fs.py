import sys

from Disk import Disk
from Simple_Filesystem import Simple_Filesystem

disk = Disk(10000)
fs = Simple_Filesystem(disk)

no_args = len(sys.argv)
image_name = sys.argv[1]
command = sys.argv[2]
if command == "mkdisk":
    fs.format()
    disk.save(image_name)
elif command == "mkfile":
    disk.load(image_name)
    fs.create_file(sys.argv[3])
    disk.save(image_name)
elif command == "list":
    disk.load(image_name)
    number_of_files, files = fs.get_files()
    print('%d file(s)' % number_of_files)
    for filename in files.keys():
        print(filename)
elif command in 'remove':
    filename = sys.argv[3]
    disk.load(image_name)
    number_of_files, files = fs.get_files()
    if filename in files:
        fs.delete_file(files[filename])
    else:
        sys.exit(filename + ' is not a file')
    disk.save(image_name)
elif command == "read":
    filename = sys.argv[3]
    disk.load(image_name)
    number_of_files, files = fs.get_files()
    if filename in files:
        for word in fs.read_from_file(files[filename]):
            sys.stdout.buffer.write(int(word).to_bytes(2, sys.byteorder))
    else:
        sys.exit(filename + ' is not a file')
    disk.save(image_name)
elif command == "write":
    filename = sys.argv[3]
    disk.load(image_name)

    number_of_files, files = fs.get_files()
    file_entry = None
    if filename in files:
        file_entry = files[filename]
        fs.delete_file_data(file_entry)
    else:
        file_entry = fs.create_file(filename)

    c = sys.stdin.buffer.read(2)
    while c:
        fs.append_to_file(file_entry, [int.from_bytes(c, sys.byteorder)])
        c = sys.stdin.buffer.read(2)
    disk.save(image_name)
