import math
from core.material import material
from util import point3, dot, Ray, vec3
from .hittable import hittable, hit_record
from .interval import interval

class Sphere(hittable):
    def __init__(self):
        raise Exception("Use Sphere.stationary() or Sphere.moving() to create a Sphere")
    
    @classmethod
    def stationary(cls, center: point3, radius: float, mat: material):
        """Create a stationary sphere."""
        instance = object.__new__(cls)
        instance.center = Ray(center, vec3(0, 0, 0))
        instance.radius = max(0.0, radius)
        instance.material = mat
        return instance
    
    @classmethod
    def moving(cls, center1: point3, center2: point3, radius: float, mat: material):
        """Create a moving sphere."""
        instance = object.__new__(cls)
        instance.center = Ray(center1, center2 - center1)
        instance.radius = max(0.0, radius)
        instance.material = mat
        return instance

    def hit(self, r: Ray, ray_t: interval, rec: hit_record) -> bool:
        current_center = self.center.at(r.time)
        oc = current_center - r.origin
        a = r.direction.length_squared()
        h = dot(r.direction, oc)
        c = oc.length_squared() - self.radius * self.radius

        discriminant = h * h - a * c
        if discriminant < 0:
            return False

        sqrtd = math.sqrt(discriminant)

        # Find the nearest root that lies in the acceptable range.
        root = (h - sqrtd) / a
        if not ray_t.surrounds(root):
            root = (h + sqrtd) / a
            if not ray_t.surrounds(root):
                return False

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - current_center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.material = self.material

        return True
