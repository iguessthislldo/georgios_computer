/*
 * Types for VM to use. 16 bit full word and 8 bit half word in unsigned and
 * signed versions. Also fuctions for inserting and extracting full little
 * endian encoded words from half word arrays.
 */
#ifndef WORD_HEADER
#define WORD_HEADER

#include <stdint.h>

typedef uint16_t word;
typedef int16_t signed_word;
typedef uint8_t half_word;
typedef int8_t signed_half_word;

const word WORD_MAX = UINT16_MAX;
const half_word HALF_WORD_MAX = UINT8_MAX;
const signed_word SIGNED_WORD_MAX = INT16_MAX;
const signed_half_word SIGNED_HALF_WORD_MAX = INT8_MAX;
const signed_word SIGNED_WORD_MIN = INT16_MIN;
const signed_half_word SIGNED_HALF_WORD_MIN = INT8_MIN;

/*
 * Given a half word array (such as the internal array of the Memory class,
 * insert (full_to_half) or extract (half_to_full) full words to and from it.
 */
void full_to_half(half_word * destination, word * source);
void half_to_full(word * destination, half_word * source);

#endif
