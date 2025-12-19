"""
Color utilities for ray tracing.

Usage:
    from util.color import color, write_color
    
    pixel = color(0.5, 0.7, 1.0)
    write_color(file, pixel)
"""

from .vec3 import vec3

# Type alias for semantic clarity
color = vec3


def write_color(pixel_color: color) -> None:
    """
    Print a color in PPM format (R G B as integers 0-255).

    Args:
        pixel_color: RGB color with components in [0, 1]
    """
    from core.interval import interval

    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z

    # Translate [0,1] component values to byte range [0,255]
    intensity = interval(0.0, 0.999)
    rbyte = int(256 * intensity.clamp(r))
    gbyte = int(256 * intensity.clamp(g))
    bbyte = int(256 * intensity.clamp(b))
    
    print(f"{rbyte} {gbyte} {bbyte}")