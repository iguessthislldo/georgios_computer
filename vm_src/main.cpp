#include <stdio.h>
#include <stdlib.h>

#include "System.hpp"

int main(int argc, char * argv[]) {
    if (argc != 3) {
        fprintf(stderr, "usage: georgios FILEPATH MEMORY_SIZE\n");
        return 100;
    }

    System system(argv[1], atoi(argv[2]));

    return system.run();
}

