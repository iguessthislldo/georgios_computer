#include "System.hpp"

/*
 * TODO: shift ops
 * TODO: Overflow
 */

void System::execute(word_t i0, word_t i1, word_t i2, word_t i3) {
    word_t next_cflags = 0x00;
    /*printf(
        "Execute %u, %u, %u, %u\n", i0, i1, i2, i3
    );*/
    switch (i0) {
    case 0x00:
        //printf("nop\n");
        break;
    case 0x01:
        printf("%u\n", registers[i1].value());
        break;
    case 0x02:
        //printf("set\n");
        registers[i1].value(i2);
        break;
    case 0x03:
        //printf("copy\n");
        registers[i1].program_set_value(
            registers[i2].value()
        );
        break;
    case 0x04:
        //printf("savevv\n");
        memory[i1] = i2;
        break;
    case 0x05:
        //printf("savevr\n");
        memory[i1] = registers[i2].value();
        break;
    case 0x06:
        //printf("saverv\n");
        memory[registers[i1].value()] = i2;
        break;
    case 0x07:
        //printf("saverr\n");
        memory[registers[i1].value()] = registers[i2].value();
        break;
    case 0x08:
        //printf("loadv\n");
        registers[i1].program_set_value(i2);
        break;
    case 0x09:
        //printf("loadr\n");
        registers[i1].program_set_value(registers[i2].value());
        break;
    case 0x0C:
        //printf("gotov\n");
        registers[rpc].value(i1);
        next_cflags |= 0x01;
        break;
    case 0x0D:
        //printf("gotor\n");
        registers[rpc].value(registers[i1].value());
        next_cflags |= 0x01;
        break;
    case 0x0E:
        //printf("ifv\n");
        if(registers[i1].value()) {
            registers[rpc].value(i2);
            next_cflags |= 0x01;
        }
        break;
    case 0x0F:
        //printf("ifr\n");
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
        printf("halt\n");
        running = 0;
        break;
    //default:
        //printf("Unknown Operation\n");
    }
    registers[rcflags].value(next_cflags);
}
