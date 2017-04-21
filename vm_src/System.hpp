#ifndef SYSTEM_HEADER
#define SYSTEM_HEADER

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include <unistd.h>

#include "Registers.hpp"

#define MAGIC_NUMBER "georgios;binary;;\n"

class System {
public:
    typedef uint16_t word_t;
    typedef int16_t signed_word_t;
    typedef Register<word_t> Reg;

    // Status
    bool running = true;
    uint32_t cycle = 0;

    // Special Registers indices
    unsigned
        rcflags, rpc, ri0, ri1, ri2, ri3,
        raop, raflags, rahi, rmem;
        

    const word_t INCREMENT_PC = 0x01;

    // Registers
    Registers<word_t> registers;

    size_t memory_size;
    word_t * memory;

    System(const string & path, size_t memory_size) {
        // Registers
        rcflags = registers.add_ro_reg("cflags");
        rpc = registers.add_ro_reg("pc");
        ri0 = registers.add_ro_reg("i0");
        ri1 = registers.add_ro_reg("i1");
        ri2 = registers.add_ro_reg("i2");
        ri3 = registers.add_ro_reg("i3");
        raop = registers.add_ro_reg("aop");
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

    void execute(word_t i0, word_t i1, word_t i2, word_t i3);

    int run() {
        //printf("= Start ===========\n");
        while (running) {
            //printf("--------- Cycle: %u\n", cycle);

            word_t pc = registers[rpc].value();
            //printf("PC: %u\n", pc);

            word_t i0 = registers[ri0].value(memory[4 * pc]);
            word_t i1 = registers[ri1].value(memory[4 * pc + 1]);
            word_t i2 = registers[ri2].value(memory[4 * pc + 2]);
            word_t i3 = registers[ri3].value(memory[4 * pc + 3]);

            //printf("- Execute ------\n");
            execute(i0, i1, i2, i3);

            if (!(registers[rcflags].value() & INCREMENT_PC))
                registers[rpc].value(pc + 1);

            cycle++;
            //sleep(1);
        }
        //printf("= End =============\n");
    }

    ~System() {
        free(memory);
    }

    size_t read_image(const string & path, size_t memory_size) {
        //printf("\"%s\"\n", path.c_str());
        FILE * file = fopen(path.c_str(), "rb");

        unsigned magic_size = sizeof(MAGIC_NUMBER) - 1;
        const char * magic_number = MAGIC_NUMBER;
        for (unsigned i = 0; i < magic_size; i++) {
            if(magic_number[i] != fgetc(file)) {
                fprintf(stderr, "Not a valid Georgios binary file\n");
                exit(1);
            }
        }

        size_t i = 0;
        while (!feof(file)) {
            fread(&memory[i], sizeof(word_t), 1, file);
            //printf("%lu\n", memory[i]);
            i++;
        }
        fclose(file);
        return i;
    }
};

#endif
