#include <stdio.h>
#include <stdlib.h>

#include <string>

#include "System.hpp"

void print_help() {
    fprintf(stderr, "usage: georgios [-v|-h] FILEPATH MEMORY_SIZE\n");
}

int main(int argc, char * argv[]) {
    if (argc == 1 || argc >= 5) {
        print_help();
        return 100;
    }

    bool verbose = false;
    char * file;
    int size;

    if (argc == 2) {
        print_help();
        if (argv[1][0] == '-' && argv[1][1] == 'h')
            return 0;
        return 100;
    } else if (argc == 3) {
        file = argv[1];
        size = atoi(argv[2]);
    } else if (argc == 4) {
        if (argv[1][0] == '-' && argv[1][1] == 'v')
            verbose = true;
        else {
            print_help();
            return 100;
        }
        file = argv[2];
        size = atoi(argv[3]);
    }

    if (verbose)
        fprintf(stderr, "Verbose Mode\n");
    
    System system(file, size, verbose);

    return system.run();
}

