import math
from core.material import material
from util import point3, dot, Ray
from .hittable import hittable, hit_record
from .interval import interval

class Sphere(hittable):
    def __init__(self, center: point3, radius: float, mat: material):
        self.center = center
        self.radius = max(0.0, radius)
        self.material = mat

    def hit(self, r: Ray, ray_t: interval, rec: hit_record) -> bool:
        oc = self.center - r.origin
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
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.material = self.material
        
        return True
