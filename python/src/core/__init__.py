"""
Core classes for ray tracing primitives and scene objects.

Usage:
    # Import specific classes/functions
    from core import sphere, hittable, hit_record

    # Or import everything
    from core import *

Examples:
    # Create a sphere
    sphere = Sphere(center=point3(0, 0, -1), radius=0.5)
"""

from .hittable import hittable, hit_record
from .sphere import Sphere
from .hittable_list import hittable_list
from .interval import interval
from .camera import camera
from .klein_bottle import KleinBottle
from .aabb import aabb
from .bvh_node import bvh_node
from .perlin import perlin
from .quad import quad
from .triangle import triangle
from .mesh import mesh

__all__ = [
    'hittable',
    'hit_record',
    'Sphere',
    'hittable_list',
    'interval',
    'camera',
    'KleinBottle',
    'aabb',
    'bvh_node',
    'perlin',
    'quad',
    'triangle',
    'mesh',
]
