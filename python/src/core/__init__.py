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

__all__ = [
    'hittable',
    'hit_record',
    'Sphere',
    'hittable_list',
    'interval',
    'camera',
]
