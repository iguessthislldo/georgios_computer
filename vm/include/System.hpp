#ifndef SYSTEM_HEADER
#define SYSTEM_HEADER

#include <stdio.h>
#include <stdlib.h>

#include "word.h"
#include "Memory.hpp"
#include "Registers.hpp"

class System {
public:

    // Status
    bool running = true;
    bool verbose, instruction_pause;

    // Special Registers indices
    unsigned
        rcflags, rpc, raflags, rahi, rmem;
        
    const word INCREMENT_PC = 0x01;

    // Registers
    Registers registers;

    // Memory
    Memory memory;

    System(const string & path, size_t memory_size, bool verbose) {
        this->verbose = verbose;

        // Setup Registers
        rcflags = registers.add_ro_reg("cflags");
        rpc = registers.add_ro_reg("pc");
        raflags = registers.add_ro_reg("aflags");
        rahi = registers.add_ro_reg("ahi");
        rmem = registers.add_ro_reg("mem");

        registers.finalize(16);

        // Setup Memory
        memory = Memory(memory_size);
        registers[rmem].value(memory_size);
        memory.load(path.c_str());
    }

    word execute(word i0, word i1, word i2, word i3);

    int run() {
        if (verbose)
            fprintf(stderr, "Running\n");

        word pc = 0;
        while (running) {
            pc = registers[rpc].value();
            word rv = execute(
                memory.full(pc), memory.full(pc + 1),
                memory.full(pc + 2), memory.full(pc + 3)
            );
            registers[rpc].value(pc + rv);

            if (instruction_pause) {
                getchar();
            }
        }
    }

private:
    void alu_rri_verbose(const char * op_str, bool first, bool second, word & i1, word & i2, word & i3, word & value);
};

#endif
