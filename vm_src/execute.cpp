#include <stdio.h>

#include "System.hpp"

/*
 * TODO: shift ops
 * TODO: Overflow
 */

void System::execute(word_t i0, word_t i1, word_t i2, word_t i3) {
    word_t next_cflags = 0x00;
    fprintf(stderr,
        "Execute %u, %u, %u, %u\n", i0, i1, i2, i3
    );
    switch (i0) {
    case 0x00: // nop
        break;
    case 0x02: // set
        registers[i1].value(i2);
        break;
    case 0x03: // copy
        registers[i1].program_set_value(
            registers[i2].value()
        );
        break;
    case 0x04: //savevv
        memory[i1] = i2;
        break;
    case 0x05: // savevr
        memory[i1] = registers[i2].value();
        break;
    case 0x06: // saverv
        memory[registers[i1].value()] = i2;
        break;
    case 0x07: // saverr
        memory[registers[i1].value()] = registers[i2].value();
        break;
    case 0x08: // loadv
        registers[i1].program_set_value(i2);
        break;
    case 0x09: // loadr
        registers[i1].program_set_value(registers[i2].value());
        break;
    case 0x0A: // in
        registers[i3].value(fgetc(stdin));
        break;
    case 0x0B: // out
        fputc(registers[i3].value(), stdout);
        fflush(stdout);
        break;
    case 0x0C: // gotov
        registers[rpc].value(i1);
        next_cflags |= 0x01;
        break;
    case 0x0D: // gotor
        registers[rpc].value(registers[i1].value());
        next_cflags |= 0x01;
        break;
    case 0x0E: // ifv
        if(registers[i1].value()) {
            registers[rpc].value(i2);
            next_cflags |= 0x01;
        }
        break;
    case 0x0F: // ifr
        if(registers[i1].value() != 0) {
            registers[rpc].value(registers[i2].value());
            next_cflags |= 0x01;
        }
        break;
    case 0x20:
        //printf("addv\n");
        registers[i1].value(
            registers[i2].value() + i3
        );
        break;
    case 0x21:
        //printf("addr\n");
        registers[i1].value(
            registers[i2].value() + registers[i3].value()
        );
        break;
    case 0x22:
        //printf("subv\n");
        registers[i1].value(
            registers[i2].value() - i3
        );
        break;
    case 0x23:
        //printf("subr\n");
        registers[i1].value(
            registers[i2].value() - registers[i3].value()
        );
        break;
    case 0x24:
        //printf("andv\n");
        registers[i1].value(
            registers[i2].value() && i3
        );
        break;
    case 0x25:
        //printf("andr\n");
        registers[i1].value(
            registers[i2].value() && registers[i3].value()
        );
        break;
    case 0x26:
        //printf("orv\n");
        registers[i1].value(
            registers[i2].value() || i3
        );
        break;
    case 0x27:
        //printf("orr\n");
        registers[i1].value(
            registers[i2].value() || registers[i3].value()
        );
        break;
    case 0x2C:
        //printf("eqv\n");
        registers[i1].value(
            registers[i2].value() == i3
        );
        break;
    case 0x2D:
        //printf("eqr\n");
        registers[i1].value(
            registers[i2].value() == registers[i3].value()
        );
        break;
    case 0x2E:
        //printf("nev\n");
        registers[i1].value(
            registers[i2].value() != i3
        );
        break;
    case 0x2F:
        //printf("ner\n");
        registers[i1].value(
            registers[i2].value() != registers[i3].value()
        );
        break;
    case 0x30:
        //printf("gtv\n");
        registers[i1].value(
            registers[i2].value() > i3
        );
        break;
    case 0x31:
        //printf("gtr\n");
        registers[i1].value(
            registers[i2].value() > registers[i3].value()
        );
        break;
    case 0x32:
        //printf("gev\n");
        registers[i1].value(
            registers[i2].value() >= i3
        );
        break;
    case 0x33:
        //printf("ger\n");
        registers[i1].value(
            registers[i2].value() >= registers[i3].value()
        );
        break;
    case 0x34:
        //printf("ltv\n");
        registers[i1].value(
            registers[i2].value() < i3
        );
        break;
    case 0x35:
        //printf("ltr\n");
        registers[i1].value(
            registers[i2].value() < registers[i3].value()
        );
        break;
    case 0x36:
        //printf("lev\n");
        registers[i1].value(
            registers[i2].value() <= i3
        );
        break;
    case 0x37:
        //printf("ler\n");
        registers[i1].value(
            registers[i2].value() <= registers[i3].value()
        );
        break;
    case 0x3A:
        //printf("andbv\n");
        registers[i1].value(
            registers[i2].value() & i3
        );
        break;
    case 0x3B:
        //printf("andbr\n");
        registers[i1].value(
            registers[i2].value() & registers[i3].value()
        );
        break;
    case 0x3C:
        //printf("orbv\n");
        registers[i1].value(
            registers[i2].value() | i3
        );
        break;
    case 0x3D:
        //printf("orbr\n");
        registers[i1].value(
            registers[i2].value() | registers[i3].value()
        );
        break;
    case 0x3E:
        //printf("xorbv\n");
        registers[i1].value(
            registers[i2].value() ^ i3
        );
        break;
    case 0x3F:
        //printf("xorbr\n");
        registers[i1].value(
            registers[i2].value() ^ registers[i3].value()
        );
        break;
    case 0x40:
        //printf("comp\n");
        registers[i1].value(
            ~registers[i2].value()
        );
        break;
    case 0x42:
        //printf("not\n");
        registers[i1].value(
            !registers[i2].value()
        );
        break;
    // TODO: HI / Low results
    case 0x43:
        //printf("mulu\n");
        registers[i1].value(
            registers[i2].value() * registers[i3].value()
        );
        break;
    case 0x44:
        //printf("mulu\n");
        registers[i1].value(
            registers[i2].value() / registers[i3].value()
        );
        break;
    case 0x45:
        //printf("muls\n");
        registers[i1].value(static_cast<word_t>(
            static_cast<signed_word_t>(registers[i2].value())
            *
            static_cast<signed_word_t>(registers[i3].value())
        ));
        break;
    case 0x46:
        //printf("divs\n");
        registers[i1].value(static_cast<word_t>(
            static_cast<signed_word_t>(registers[i2].value())
            /
            static_cast<signed_word_t>(registers[i3].value())
        ));
        break;
    case 0xFF:
        fprintf(stderr, "halt\n");
        running = 0;
        break;
    //default:
        //printf("Unknown Operation\n");
    }
    registers[rcflags].value(next_cflags);
}
