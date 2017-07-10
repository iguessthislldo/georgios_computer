/*
 * Memory Class Source
 */
#include <stdlib.h>
#include <stdio.h>

#include "magic.h"
#include "Memory.hpp"

Memory::Memory() {
    this->size = 0;
}

Memory::Memory(word size) {
    this->size = size;
    contents = (half_word *) malloc(sizeof(half_word) * size);
    if (contents == NULL) {
        fprintf(stderr, "Couldn't allocate memory of size: %u\n", size);
        exit(100);
    }
}

Memory::~Memory() {
    free(contents);
}

word Memory::load(const char * file_path) {
    // Open File
    FILE * file = fopen(file_path, "rb");
    if (file == NULL) {
        perror("Couldn't open binary file for loading");
        exit(1);
    }

    // Check for Magic number
    for (unsigned i = 0; i < BINARY_MAGIC_SIZE; i++) {
        if (BINARY_MAGIC[i] != fgetc(file) || feof(file)) {
            fprintf(stderr, "Not a valid Georgios binary file\n");
            exit(1);
        }
    }

    // Get Size
    word image_size;
    // Ensure it is little endianness
    half_word image_size_array[2] = {0, 0};
    fread(image_size_array, sizeof(half_word), 2, file);
    half_to_full(&image_size, image_size_array);
    // Check size
    if (image_size > size) {
        fprintf(stderr, "Warning: file says that image size is larger than memory, will not be able to get entire image.\n");
    }

    // Read Image into contents
    word i = 0;
    while (!feof(file)) {
        if (i > size) {
            fprintf(stderr, "Warning: Image in file is larger than memory, was not able to get entire image.\n");
            i--;
            break;
        }
        fread(&contents[i], sizeof(half_word), 1, file);
        i++;
    }

    // Close and return ammount loaded
    fclose(file);
    return i;
}

void Memory::save(const char * file_path) {
    // Open file
    FILE * file = fopen(file_path, "wb");
    if (file == NULL) {
        perror("Couldn't open file for dumping memory");
        exit(1);
    }

    // Write magic number
    for (unsigned i = 0; i < BINARY_MAGIC_SIZE; i++) {
        fputc(BINARY_MAGIC[i], file);
    }

    // Write Memory Size
    half_word image_size_array[2] = {0, 0};
    full_to_half(&image_size_array[0], &size);
    fwrite(&image_size_array, sizeof(half_word), 2, file);

    // Write contents of memory
    fwrite(contents, sizeof(half_word), size, file);
    
    // Close File
    fclose(file);
}

word Memory::full(word address) {
    if (address > (size - 2)) {
        fprintf(stderr,
            "Invalid 2B memory read: %u\n", address
        );
        exit(200);
    }
    word value;
    half_to_full(&value, &contents[address]);
    return value;
}

void Memory::full(word address, word value) {
    if (address > (size - 2)) {
        fprintf(stderr,
            "Invalid 2B memory write: %u\n", address
        );
        exit(201);
    }
    full_to_half(&contents[address], &value);
}

half_word Memory::half(word address) {
    if (address > size - 1) {
        fprintf(stderr,
            "Invalid 1B memory read: %u\n", address
        );
        exit(202);
    }
    return contents[address];
}

void Memory::half(half_word address, half_word value) {
    if (address > size - 1) {
        fprintf(stderr,
            "Invalid 1B memory write: %u\n", address
        );
        exit(203);
    }
    contents[address] = value;
}
