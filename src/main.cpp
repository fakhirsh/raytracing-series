#include "Vec3.hpp"
#include "Color.hpp"

#include <iostream>
#include <fstream>

int main(int, char**){
    
    // Write to file
    std::ofstream out_file("image.ppm");
    if(!out_file){
        std::cerr << "Failed to open file for writing" << std::endl;
        return 1;
    }
    
    const int WIDTH  = 512;
    const int HEIGHT = 512;

    out_file << "P3" << std::endl;
    out_file << WIDTH << " " << HEIGHT << std::endl;
    out_file << "255" << std::endl;

    for(int h = 0; h < HEIGHT; h++){
        std::clog << "\rScanlines remaining: " << (HEIGHT - h*1.0) / HEIGHT * 100.0 << " %" << std::flush;
        for(int w = 0; w < WIDTH; w++){
            auto pixel_color = color(double(w)/(WIDTH-1), double(h)/(HEIGHT-1), 0);
            write_color(out_file, pixel_color);
        }
    }

    out_file.close();

    return 0;
}