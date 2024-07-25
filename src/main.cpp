#include "Vec3.hpp"
#include "Color.hpp"

#include <iostream>

int main(int, char**){
    
    const int WIDTH  = 512;
    const int HEIGHT = 512;

    std::cout << "P3" << std::endl;
    std::cout << WIDTH << " " << HEIGHT << std::endl;
    std::cout << "255" << std::endl;

    for(int h = 0; h < HEIGHT; h++){
        std::clog << "\rScanlines remaining: " << (HEIGHT - h*1.0) / HEIGHT * 100.0 << " %" << std::flush;
        for(int w = 0; w < WIDTH; w++){
            auto pixel_color = color(double(w)/(WIDTH-1), double(h)/(HEIGHT-1), 0);
            write_color(std::cout, pixel_color);
        }
    }

    return 0;
}