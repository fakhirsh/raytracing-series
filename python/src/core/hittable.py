from util import vec3, point3, dot, Ray
from .interval import interval
from abc import ABC, abstractmethod

class hit_record:
    def __init__(self, p: point3 = None, normal: vec3 = None, t: float = 0.0):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face: bool = True

    def set_face_normal(self, r: Ray, outward_normal: vec3):
        # Sets the hit record normal vector.
        # NOTE: the parameter `outward_normal` is assumed to have unit length.

        self.front_face = dot(r.direction, outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal

    def copy_from(self, other: 'hit_record'):
        self.p = other.p
        self.normal = other.normal
        self.t = other.t
        self.front_face = other.front_face

class hittable(ABC):
    @abstractmethod
    def hit(self, r: Ray, ray_t: interval, rec: hit_record) -> bool:
        pass
