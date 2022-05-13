alcor aptinstall libeigen3-dev

module load libeigen3-dev

tee eigen_main.cpp << END
#include <eigen3/Eigen/Core>

int main(int argc, const char* argv[]){
    return 0;
}
END

g++ eigen_main.cpp -o eigen_main