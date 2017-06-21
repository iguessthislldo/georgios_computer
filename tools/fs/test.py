from Disk import Disk
from nodes import *
from Filesystem import Filesystem

# /
#     dir_A/
#         file_1
#         dir_B/
#             file_2
#     file_0

disk = Disk(1000)
fs = Filesystem(disk)
fs.format()
root = fs.root
c = root.ctx

file_0 = fs.new_file_node(root, "file_0")
dir_A = fs.new_directory_node(root, "dir_A")
file_1 = fs.new_file_node(dir_A, "file_1")
dir_B = fs.new_directory_node(dir_A, "dir_B")
file_2 = fs.new_file_node(dir_B, "file_2")

