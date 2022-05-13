source /home/runner/.config/mocli/bashrc
alcor aptinstall libsdl2-dev

module load libsdl2-dev

tee sdl2_main.c << END
#include "SDL2/SDL.h"

int main(int argc, const char* argv[]){
    return 0;
}
END

gcc sdl2_main.c -o sdl2_main -lSDL2