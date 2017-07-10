#include "word.h"

void full_to_half(half_word * destination, word * source) {
    destination[0] = (*source) & 255; // Lower Byte
    destination[1] = (*source) >> 8; // Upper Byte
}

void half_to_full(word * destination, half_word * source) {
    *destination =
        (((word) source[1]) << 8) // Upper Byte
            |
        ((word) source[0]) // Lower Byte
    ;
}
