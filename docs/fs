# Georgios Filesystem
This is currently just implemented as a python prototype and has the goal
of getting to a minimum working state for the time being. Currently it
is grossly inefficient. Every node takes a block so if word size is in bytes
and blocks are 256 bytes, for every file or directory, 218 bytes are wasted.
Ignoring the disk header, and assuming a filesystem consists only of files
with a single full data node, that's about 42 percent wasted space.
After minimum functionality is achieved I hope to sub allocate multiple
of the fixed size entry nodes on blocks dynamically. This of course isn't
absolutely perfect, but it much more acceptable.

## Blocks
Right now data is organized into blocks. The first block is permanently
allocated for the filesystem header, which contains the root node and
block allocation data. The other blocks can be free or contain a node.

# Nodes
Nodes contain the metadata for the filesystem. All nodes contain two
pieces of information: The node type and the size. What the size means
and what the rest of the node are depends on what kind of node it is.

## Types
- ROOT = 1
- FILE = 2
- SUBDIRECTORY = 4
- DATA = 8

There are also type values that help filter the real types:
- NONE = 0
    - Matches No Node.
- DIRECTORY = ROOT | SUBDIRECTORY = 5
    - Has the Head and Tail pointers that point to ENTRY Nodes. Size is the
    number of entries in that list.
- ENTRY = FILE | SUBDIRECTORY = 6
    - Has a parent that is a DIRECTORY, a Sibling might be invalid or another
    ENTERY, and, a Name.
- LIST = ROOT | ENTRY = 7
    - Has head and tail pointers that define a linked list.
- VALID = LIST | DATA = 15
    - Matches any valid node type value.

## Root Node and the Disk Header
The Root node is embedded in the disk header and is a DIRECTORY node.

### Structure
0. Size of disk in words
1. Block Size in words
2. Number of Blocks on the disk
3. Type = 1, Root Type (Start of Root Node)
4. Number of Children of Root Node
5. Head Root Child
6. Tail Root Child (End of the Root Node)
7. [ Block Allocation Data ]

## File Entry Node
Is a ENTRY and LIST node.

### Structure
0. Type = 2, File Type
1. Total Data Size
2. Head Data Node Pointer
3. Tail Data Node Pointer
4. Parent Node Pointer
5. Next Sibling Node Pointer
6. [ Name String ]

## Subdirectory Entry Node
Is a DIRECTORY, ENTRY and LIST node.
Represents all directories except for the root directory.
### Structure
0. Type = 4, Subdirectory Type
1. Number of child entries
2. Head Child Entry Node Pointer
3. Tail Child Entry Node Pointer
4. Parent Node Pointer
5. Next Sibling Node Pointer
6. [ Name String ]

## File Data Node
Hold the file data in a linked list.
### Structure
0. Type = 8, Data Type
1. Data Size
2. Next Data Node Pointer
3. [ Contents ]

# Operations

## Low Level Operations
- Block Allocation Getting and Setting
- Resolve Path as Node Location or Parent
- Make Entry
- Remove Entry

## High Level Operations
- List Directory Contents
- Make Directory
- Remove Directory
- Make Empty File
- Remove File
- Read from and Write to Files

