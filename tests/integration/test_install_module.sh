alcor install lz4

module load lz4

# all the paths are set we can compile programs with lz4
tee lz4_main.c << END
#include "lz4.h"

int main(int argc, const char* argv[]){
    return 0;
}
END

gcc lz4_main.c -o lz4_main -llz4
