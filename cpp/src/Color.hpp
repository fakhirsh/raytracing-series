#pragma once

#include "Vec3.hpp"

#include <iostream>

using color = Vec3;

void write_color(std::ostream & out, const color & pixel_color){
    auto r = pixel_color.x();
    auto g = pixel_color.y();
    auto b = pixel_color.z();

    auto rbyte = int(255.999 * r);
    auto gbyte = int(255.999 * g);
    auto bbyte = int(255.999 * b);

    out << rbyte << " "<< " "  << gbyte << " " << bbyte << std::endl;
}