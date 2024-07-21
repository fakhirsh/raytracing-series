#include <iostream>

int main(int, char**){
    
    const int WIDTH  = 1024;
    const int HEIGHT = 1024;

    std::cout << "P3" << std::endl;
    std::cout << WIDTH << " " << HEIGHT << std::endl;
    std::cout << "255" << std::endl;

    for(int h = 0; h < HEIGHT; h++){
        for(int w = 0; w < WIDTH; w++){
            std::cout << (h*w+w)%255 << " " << 0 << " " << 0 << " ";
        }
        std::cout << std::endl;
    }

    return 0;
}
