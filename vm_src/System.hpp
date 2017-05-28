#ifndef SYSTEM_HEADER
#define SYSTEM_HEADER

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "Registers.hpp"

#define MAGIC_NUMBER "georgios;binary;;\n"

class System {
public:
    typedef uint16_t word_t;
    typedef int16_t signed_word_t;
    typedef Register<word_t> Reg;

    // Status
    bool running = true;
    bool verbose;

    // Special Registers indices
    unsigned
        rcflags, rpc, raflags, rahi, rmem;
        
    const word_t INCREMENT_PC = 0x01;

    // Registers
    Registers<word_t> registers;

    size_t memory_size;
    word_t * memory;

    System(const string & path, size_t memory_size, bool verbose) {
        this->verbose = verbose;

        // Registers
        rcflags = registers.add_ro_reg("cflags");
        rpc = registers.add_ro_reg("pc");
        raflags = registers.add_ro_reg("aflags");
        rahi = registers.add_ro_reg("ahi");
        rmem = registers.add_ro_reg("mem");

        registers.finalize(16);

        // Setup Memory
        this->memory_size = memory_size;
        memory = (word_t *) malloc(sizeof(word_t) * memory_size);
        if (memory == NULL) {
            fprintf(stderr, "Couldn't allocate memory\n");
            exit(1);
        }

        registers[rmem].value(read_image(path, memory_size));
    }

    word_t execute(word_t i0, word_t i1, word_t i2, word_t i3);

    int run() {
        if (verbose)
            fprintf(stderr, "Running\n");

        word_t pc = 0;
        while (running) {
            pc = registers[rpc].value();
            word_t rv = execute(memory[pc], memory[pc + 1], memory[pc + 2], memory[pc + 3]);
            if (rv)
                registers[rpc].value(pc + rv);

            if (verbose) {
                fprintf(stderr, "Hit Enter to run next Instruction...\n");
                getchar();
            }
        }
    }

    ~System() {
        free(memory);
    }

    size_t read_image(const string & path, size_t memory_size) {
        FILE * file = fopen(path.c_str(), "rb");

        unsigned magic_size = sizeof(MAGIC_NUMBER) - 1;
        const char * magic_number = MAGIC_NUMBER;
        for (unsigned i = 0; i < magic_size; i++) {
            if (magic_number[i] != fgetc(file) || feof(file)) {
                fprintf(stderr, "Not a valid Georgios binary file\n");
                exit(1);
            }
        }

        size_t i = 0;
        while (!feof(file)) {
            fread(&memory[i], sizeof(word_t), 1, file);
            if (verbose)
                fprintf(stderr, "%u\n", memory[i]);
            i++;
        }
        fclose(file);
        return i;
    }

private:
    void rii(bool first, bool second, word_t * b, word_t * c);
};

#endif
