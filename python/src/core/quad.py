
from util import ray
from .hittable import hittable, hit_record
from util import *
from .material import material
from .aabb import aabb
from util import point3, vec3
from .interval import interval


class quad(hittable):
    def __init__(self, Q: point3, u: vec3, v: vec3, mat: material):
        self.Q = Q
        self.u = u
        self.v = v
        self.mat = mat

        n = vec3.cross(u, v)
        self.normal = n.unit_vector()
        self.D = vec3.dot(self.normal, Q)
        self.w = n / vec3.dot(n, n)

        self.set_bounding_box()

    def set_bounding_box(self):
        bbox_diag1 = aabb.from_points(self.Q, self.Q + self.u + self.v)
        bbox_diag2 = aabb.from_points(self.Q + self.u, self.Q + self.v)
        self.bbox = aabb.from_aabbs(bbox_diag1, bbox_diag2)
        self.bbox._pad_to_minimums()
        
    def bounding_box(self):
        return self.bbox
    
    def hit(self, r: ray, ray_t: interval, rec: hit_record) -> bool:
        denom = vec3.dot(self.normal, r.direction)
        
        if abs(denom) < 1e-8:
            return False  # Ray is parallel to the quad
        
        t = (self.D - vec3.dot(self.normal, r.origin)) / denom
        if not ray_t.contains(t):
            return False
        
        # Determine if the hit point lies within the planar shape using its plane coordinates.
        intersection = r.at(t)
        planar_hitpt_vector = intersection - self.Q
        alpha = vec3.dot(self.w, vec3.cross(planar_hitpt_vector, self.v))
        beta = vec3.dot(self.w, vec3.cross(self.u, planar_hitpt_vector))

        if not self.is_interior(alpha, beta, rec):
            return False
        
        # Ray hits the 2D shape; set the rest of the hit record and return true.
        rec.t = t
        rec.p = intersection
        rec.set_face_normal(r, self.normal)
        rec.material = self.mat

        return True
    
    def is_interior(self, a: float, b: float, rec: hit_record) -> bool:
        unit_interval = interval.from_floats(0.0, 1.0)

        if not unit_interval.contains(a) or not unit_interval.contains(b):
            return False
        
        rec.u = a
        rec.v = b
        return True