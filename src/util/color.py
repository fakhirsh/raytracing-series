"""
Color utilities for ray tracing.

Usage:
    from util.color import color, write_color
    
    pixel = color(0.5, 0.7, 1.0)
    write_color(file, pixel)
"""

from .vec3 import vec3
import math

# Type alias for semantic clarity
color = vec3

def linear_to_gamma(linear_component: float) -> float:
    
    if linear_component > 0:
        return math.sqrt(linear_component)
    else:
        return 0.0

def write_color(file, pixel_color: color) -> None:
    """
    Write a color in PPM format (R G B as integers 0-255) to a file.

    Args:
        file: File object to write to
        pixel_color: RGB color with components in [0, 1]
    """
    from core.interval import interval

    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z

    # Apply a linear to gamma transform for gamma 2
    r = linear_to_gamma(r)
    g = linear_to_gamma(g)
    b = linear_to_gamma(b)

    # Translate [0,1] component values to byte range [0,255]
    intensity = interval.from_floats(0.0, 0.999)
    rbyte = int(256 * intensity.clamp(r))
    gbyte = int(256 * intensity.clamp(g))
    bbyte = int(256 * intensity.clamp(b))

    file.write(f"{rbyte} {gbyte} {bbyte}\n")