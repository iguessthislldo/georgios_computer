/*
 * Memory Class Declaration
 * Load, save, and access memory.
 */
#ifndef MEMORY_HEADER
#define MEMORY_HEADER

#include "word.h"

class Memory {
public:
    /*
     * Create a Memory in size of half words (bytes)
     */
    Memory();
    Memory(word size);
    ~Memory();

    /*
     * Load Georgios Binary into the start of memory
     */
    word load(const char * file_path);

    /*
     * Save all of memory to a file
     */
    void save(const char * file_path);

    /*
     * Access Memory as Full Words
     */
    word full(word address);
    void full(word address, word value);

    /*
     * Access Memory as Half Words
     */
    half_word half(word address);
    void half(half_word address, half_word value);
private:
    half_word * contents = NULL;
    word size;
};

#endif
