#include <stdio.h>

#include "word.h"
#include "System.hpp"

/*
 * TODO: shift ops
 * TODO: Overflow
 */

void System::alu_rri_verbose(const char * op_str, bool first, bool second, word & i1, word & i2, word & i3, word & value) {
    fprintf(stderr, "        %%%s = ", registers[i1].name().c_str());
    if (first) {
        fprintf(stderr, "%%%s(%u)", registers[i2].name().c_str(), registers[i2].value());
    } else {
        fprintf(stderr, "%u", i2);
    }
    fprintf(stderr, " %s ", op_str);
    if (second) {
        fprintf(stderr, "%%%s(%u)", registers[i3].name().c_str(), registers[i3].value());
    } else {
        fprintf(stderr, "%u", i3);
    }
    fprintf(stderr, " = %u", value);
}

word System::execute(word i0, word i1, word i2, word i3) {

    if (verbose)
        fprintf(stderr, "%u", registers[rpc].value());

    word pc_change = 4;

    // Extract OP Code
    word op = i0 >> 2;
    // Extract Arugument Indirection
    word first = i0 & 2;
    word second = i0 & 1;

    word a, b, c;

    if (first && i2 < registers.size()) {
        b = registers[i2].value();
    } else {
        b = i2;
    }
    if (second && i3 < registers.size()) {
        c = registers[i3].value();
    } else {
        c = i3;
    }

    word next_cflags = 0x00;
//dec|hex|bin    |name |ALU OP|DESCRIPTION                          |ARGUMENTS      |
    word value;
    switch (op) {
//00 |00 |000000 |nop  |      |Do nothing                           |_ _ _ 00 0 000 |
    case 0x00:
        if (verbose)
            fprintf(stderr, "    nop");
        pc_change = 1;
        break;
//01 |01 |000001 |=    |      |Set %A to B                          |R I _ 10 1 100 |
    case 0x01: // = (set)
        if (verbose) {
            fprintf(stderr, "    =\n");
            fprintf(stderr, "        %%%s = ", registers[i1].name().c_str());
        }
        if (first) {
            value = registers[i2].value();
            if (verbose)
                fprintf(stderr, "%%%s = ", registers[i2].name().c_str());
        } else {
            value = i2;
        }
        if (verbose) fprintf(stderr, "%u", value);
        registers[i1].program_set_value(value);
        pc_change = 3;
        break;
//02 |02 |000010 |save |      |Set memory at A to B                 |I I _ 10 0 000 |
    case 0x02:
        if (verbose)
            fprintf(stderr, "    save\n");
        value = second ? registers[i2].value() : i2;
        if (first) {
            memory.full(registers[i1].value(), value);
            if (verbose)
                fprintf(stderr, "        M[%%%s(%u)] = ", registers[i1].name().c_str(), registers[i1].value());
        } else {
            memory.full(i1, value);
            if (verbose)
                fprintf(stderr, "        M[%u] = ", i1);
        }
        if (verbose) {
            if (second) {
                fprintf(stderr, "%%%s(%u)", registers[i2].name().c_str(), value);
            } else {
                fprintf(stderr, "%u", value);
            }
        }
        pc_change = 3;
        break;
//03 |03 |000011 |load |      |Set %A to memory at B                |R I _ 10 1 100 |
    case 0x03:
        if (verbose) {
            fprintf(stderr, "    load\n");
            fprintf(stderr, "        %%%s = M[", registers[i1].name().c_str());
        }
        value = first ? registers[i2].value() : i2;
        registers[i1].program_set_value(memory.full(value));
        if (verbose) {
            if (first) {
                fprintf(stderr, "%%%s(%u)", registers[i2].name().c_str(), value);
            } else {
                fprintf(stderr, "%u", value);
            }
            fprintf(stderr, "] = %u", memory.full(value));
        }
        pc_change = 3;
        break;
//04 |04 |000100 |if   |      |If %A go to B                        |R I _ 10 1 100 |
    case 0x04:
        if (verbose) {
            fprintf(stderr, "    if\n");
            fprintf(stderr, "        if %%%s(%u): %%pc = ",
                registers[i1].name().c_str(), registers[i1].value()
            );
            if (first)
                fprintf(stderr, "%%%s(%u) ", registers[i2].name().c_str(), registers[i2].value());
            else
                fprintf(stderr, "%u", i2);
        }

        if (registers[i1].value()) {
            if (verbose) fprintf(stderr, " (JUMPING)");
            registers[rpc].value(first ? registers[i2].value() : i2);
            next_cflags |= INCREMENT_PC;
            pc_change = 0;
        } else {
            if (verbose) fprintf(stderr, " (continuing)");
            pc_change = 3;
        }
        break;
//05 |05 |000101 |goto |      |Jump to A                            |I _ _ 01 0 000 |
    case 0x05:
        if (verbose) {
            fprintf(stderr, "    goto\n");
            fprintf(stderr, "        %%pc = ");
            if (first)
                fprintf(stderr, "%%%s(%u)", registers[i1].name().c_str(), registers[i1].value());
            else
                fprintf(stderr, "%u", i1);
        }
        registers[rpc].value(first ? registers[i1].value() : i1);
        next_cflags |= INCREMENT_PC;
        pc_change = 0;
        break;
//06 |06 |000110 |if!  |      |If not %A go to B                    |R I _ 10 1 100 |
    case 0x06:
        if (verbose) {
            fprintf(stderr, "    if!\n");
            fprintf(stderr, "        if !%%%s(%u): %%pc = ",
                registers[i1].name().c_str(), registers[i1].value()
            );
            if (first)
                fprintf(stderr, "%%%s(%u) ", registers[i2].name().c_str(), registers[i2].value());
            else
                fprintf(stderr, "%u", i2);
        }

        if (!registers[i1].value()) {
            if (verbose) fprintf(stderr, " (JUMPING)");
            registers[rpc].value(first ? registers[i2].value() : i2);
            next_cflags |= INCREMENT_PC;
            pc_change = 0;
        } else {
            if (verbose) fprintf(stderr, " (continuing)");
            pc_change = 3;
        }
        break;
//08 |08 |001000 |in   |      |Read Input(%B, %C) to %A             |R R R 11 0 111 |
    case 0x08:
        if (verbose)
            fprintf(stderr, "    in");
        a = fgetc(stdin);
        value = registers[i1].value();
        if (verbose)
            fprintf(stderr, "        %%%s = in() = %u", registers[i1].name().c_str(), value);
        break;
//09 |09 |001001 |out  |      |Write A to Output(%B, %C)            |I R R 11 0 011 |
    case 0x09:
        if (verbose)
            fprintf(stderr, "    out\n");
        a = first ? registers[i1].value() : i1;
        if (verbose) {
            if (first)
                fprintf(stderr, "        out(%%%s(%u))", registers[i1].name().c_str(), a);
            else
                fprintf(stderr, "        out(%u)", a);
        }
        fputc(a, stdout);
        fflush(stdout);
        break;
//32 |20 |100000 |+    |00000 |Set %A to B add C                    |R I I 11 1 100 |
    case 0x20:
        if (verbose)
            fprintf(stderr, "    +\n");
        value = b + c;
        if (verbose) alu_rri_verbose("+", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//33 |21 |100001 |-    |00001 |Set %A to B subtract C               |R I I 11 1 100 |
    case 0x21:
        if (verbose)
            fprintf(stderr, "    -\n");
        value = b - c;
        if (verbose) alu_rri_verbose("-", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//34 |22 |100010 |++   |00010 |Increment %A                         |R _ _ 01 0 100 |
    case 0x22:
        value = registers[i1].value();
        if (verbose)
            fprintf(stderr, "    ++\n", i1, value);
        value = registers[i1].value();
        registers[i1].value(value + 1);
        if (verbose)
            fprintf(stderr, "        %%%s++ = %u + 1 = %u", registers[i2].name().c_str(), value, value + 1);
        pc_change = 2;
        break;
//35 |23 |100011 |--   |00011 |Decrement %A                         |R _ _ 01 0 100 |
    case 0x23:
        if (verbose)
            fprintf(stderr, "    --\n");
        value = registers[i1].value();
        registers[i1].value(value - 1);
        if (verbose)
            fprintf(stderr, "        %%%s-- = %u - 1 = %u", registers[i2].name().c_str(), value, value - 1);
        pc_change = 2;
        break;
//36 |24 |100100 |*u   |00100 |Set %A to unsigned mult. of B and C  |R I I 11 1 100 |
    case 0x24:
        if (verbose)
            fprintf(stderr, "    *u\n");
        value = b * c;
        if (verbose) alu_rri_verbose("*u", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//37 |25 |100101 |/u   |00101 |Set %A to unsigned div. of B and C   |R I I 11 1 100 |
    case 0x25:
        if (verbose)
            fprintf(stderr, "    /u\n");
        value = b / c;
        if (verbose) alu_rri_verbose("/u", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//38 |26 |100110 |*s   |00110 |Set %A to signed mult. of B and C    |R I I 11 1 100 |
    case 0x26:
        if (verbose)
            fprintf(stderr, "    *s\n");
        value = static_cast<signed_word>(b) * static_cast<signed_word>(c);
        if (verbose) alu_rri_verbose("*s", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//39 |27 |100111 |/s   |00111 |Set %A to signed div. of B and C     |R I I 11 1 100 |
    case 0x27:
        if (verbose)
            fprintf(stderr, "    /s\n");
        value = static_cast<signed_word>(b) / static_cast<signed_word>(c);
        if (verbose) alu_rri_verbose("/s", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//40 |28 |101000 |&&   |01000 |Set %A to B logical and C            |R I I 11 1 100 |
    case 0x28:
        if (verbose)
            fprintf(stderr, "    &&\n");
        value = b && c;
        if (verbose) alu_rri_verbose("&&", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//41 |29 |101001 |||   |01001 |Set %A to B logical or C             |R I I 11 1 100 |
    case 0x29:
        if (verbose)
            fprintf(stderr, "    ||\n");
        value = b || c;
        if (verbose) alu_rri_verbose("||", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//42 |2A |101010 |<<   |01010 |Set %A to B logical shift left C     |R I I 11 1 100 |
    case 0x2A:
        if (verbose)
            fprintf(stderr, "    <<\n");
        value = b << c;
        if (verbose) alu_rri_verbose("<<", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//43 |2B |101011 |>>   |01011 |Set %A to B logical shift right C    |R I I 11 1 100 |
    case 0x2B:
        if (verbose)
            fprintf(stderr, "    >>\n");
        registers[i1].value(b >> c);
        value = b >> c;
        if (verbose) alu_rri_verbose(">>", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//44 |2C |101100 |>>>  |01100 |Set %A to B arithmatic shift right C |R I I 11 1 100 |
    case 0x2C:
        if (verbose)
            fprintf(stderr, "    >>>\n");
        fprintf(stderr, "ARITHMATIC SHIFT RIGHT NOT IMPLEMENTED\n");
        exit(100);
        break;
//45 |2D |101101 |&    |01101 |Set %A to B bitwise and C            |R I I 11 1 100 |
    case 0x2D:
        if (verbose)
            fprintf(stderr, "    &\n");
        value = b & c;
        if (verbose) alu_rri_verbose("&", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//46 |2E |101110 ||    |01110 |Set %A to B bitwise or C             |R I I 11 1 100 |
    case 0x2E:
        if (verbose)
            fprintf(stderr, "    |\n");
        value = b | c;
        if (verbose) alu_rri_verbose("|", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//47 |2F |101111 |^    |01111 |Set %A to B bitwise xor C            |R I I 11 1 100 |
    case 0x2F:
        if (verbose)
            fprintf(stderr, "    ^\n");
        value = b ^ c;
        if (verbose) alu_rri_verbose("^", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//48 |30 |110000 |==   |10000 |Set %A to B equals C                 |R I I 11 1 100 |
    case 0x30:
        if (verbose)
            fprintf(stderr, "    ==\n");
        value = b == c;
        if (verbose) alu_rri_verbose("==", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//49 |31 |110001 |!=   |10001 |Set %A to B not equals C             |R I I 11 1 100 |
    case 0x31:
        if (verbose)
            fprintf(stderr, "    !=\n");
        value = b != c;
        if (verbose) alu_rri_verbose("!=", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//50 |32 |110010 |>    |10010 |Set %A to B greater than C           |R I I 11 1 100 |
    case 0x32:
        if (verbose)
            fprintf(stderr, "    >\n");
        value = b > c;
        if (verbose) alu_rri_verbose(">", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//51 |33 |110011 |>=   |10011 |Set %A to B greater than equal to C  |R I I 11 1 100 |
    case 0x33:
        if (verbose)
            fprintf(stderr, "    >=\n");
        value = b >= c;
        if (verbose) alu_rri_verbose(">=", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//52 |34 |110110 |<    |10110 |Set %A to B less than C              |R I I 11 1 100 |
    case 0x34:
        if (verbose)
            fprintf(stderr, "    <\n");
        value = b < c;
        if (verbose) alu_rri_verbose("<", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//53 |35 |110111 |<=   |10111 |Set %A to B less than equal to C     |R I I 11 1 100 |
    case 0x35:
        if (verbose)
            fprintf(stderr, "    <=\n");
        value = b <= c;
        if (verbose) alu_rri_verbose("<=", first, second, i1, i2, i3, value);
        registers[i1].value(value);
        break;
//54 |36 |111000 |~    |11000 |Set %A to bitwise not B              |R I _ 10 1 100 |
    case 0x36:
        if (verbose)
            fprintf(stderr, "    ~\n");
        fprintf(stderr, "        %%%s = ~", registers[i1].name().c_str());
        if (first) {
            fprintf(stderr, "%%%s(%u)", registers[i2].name().c_str(), registers[i2].value());
        } else {
            fprintf(stderr, "%u", i2);
        }
        registers[i1].value(~(first ? registers[i2].value() : i2));
        pc_change = 2;
        break;
//55 |37 |111001 |!    |11001 |Set %A to logical not B              |R I _ 10 1 100 |
    case 0x37:
        if (verbose)
            fprintf(stderr, "    !\n");
        fprintf(stderr, "        %%%s = !", registers[i1].name().c_str());
        if (first) {
            fprintf(stderr, "%%%s(%u)", registers[i2].name().c_str(), registers[i2].value());
        } else {
            fprintf(stderr, "%u", i2);
        }
        registers[i1].value(!(first ? registers[i2].value() : i2));
        pc_change = 2;
        break;
//63 |3F |111111 |halt |      |Halt the computer                    |_ _ _ 00 0 000 |
    case 0x3F:
        if (verbose) fprintf(stderr, "    halt");
        running = 0;
        pc_change = 0;
        break;
    default:
        fprintf(stderr, "Error Unknown Operation\n");
        exit(100);
    }
    registers[rcflags].value(next_cflags);

    return pc_change;
}
